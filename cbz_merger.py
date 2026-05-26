#!/usr/bin/env python3
"""
Yor CBZ Merger v3.0 — Comic Book Archive Merger Tool
Combines CBZ, CBR, ZIP, RAR files and image folders into a single CBZ or PDF.
Modern Clean UI · Light/Dark theme · PyQt6
"""

import os
import re
import zipfile
import tempfile
from pathlib import Path
from typing import Optional

# Optional dependency detection
try:
    import rarfile
    RAR_SUPPORT = True
except ImportError:
    RAR_SUPPORT = False

try:
    import img2pdf
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False


class CBZMerger:
    """Core logic for merging comic book archives."""

    SUPPORTED_EXTENSIONS = {'.cbz', '.cbr', '.zip', '.rar'}
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}

    def __init__(self, progress_callback=None, log_callback=None):
        self.progress_callback = progress_callback
        self.log_callback = log_callback

    def log(self, message: str):
        if self.log_callback:
            self.log_callback(message)
        print(message)

    def update_progress(self, value: float, status: str = ""):
        if self.progress_callback:
            self.progress_callback(value, status)

    def is_supported_file(self, filepath: str) -> bool:
        return Path(filepath).suffix.lower() in self.SUPPORTED_EXTENSIONS

    def is_image_file(self, filename: str) -> bool:
        return Path(filename).suffix.lower() in self.IMAGE_EXTENSIONS

    def is_image_folder(self, folderpath: str) -> bool:
        if not os.path.isdir(folderpath):
            return False
        for root, dirs, files in os.walk(folderpath):
            for f in files:
                if self.is_image_file(f):
                    return True
        return False

    def extract_archive(self, archive_path: str, extract_to: str) -> bool:
        ext = Path(archive_path).suffix.lower()
        archive_name = Path(archive_path).stem
        try:
            if ext in {'.cbz', '.zip'}:
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    zf.extractall(extract_to)
                return True
            elif ext in {'.cbr', '.rar'}:
                if not RAR_SUPPORT:
                    self.log("⚠️ RAR support not available. Install 'rarfile'.")
                    return False
                with rarfile.RarFile(archive_path, 'r') as rf:
                    rf.extractall(extract_to)
                return True
            else:
                self.log(f"⚠️ Unsupported archive format: {ext}")
        except Exception as e:
            self.log(f"❌ Error extracting {archive_name}: {e}")
        return False

    def natural_sort_key(self, path: str):
        name = Path(path).name if isinstance(path, str) else str(path)
        parts = re.split(r'(\d+)', name)
        return [int(p) if p.isdigit() else p.lower() for p in parts]

    def collect_images_by_subfolder(self, directory: str):
        subfolder_images: dict[str, list[str]] = {}
        for root, dirs, files in os.walk(directory):
            rel_path = os.path.relpath(root, directory)
            subfolder_name = "" if rel_path == "." else rel_path.split(os.sep)[0]
            for file in files:
                if self.is_image_file(file):
                    full_path = os.path.join(root, file)
                    subfolder_images.setdefault(subfolder_name, []).append(full_path)

        result = []
        for subfolder in sorted(subfolder_images.keys(), key=self.natural_sort_key):
            images = sorted(subfolder_images[subfolder], key=self.natural_sort_key)
            for img in images:
                result.append((subfolder, img))
        return result

    def merge_archives(self, input_items: list, output_path: str, output_pdf: bool = False) -> bool:
        if not input_items:
            self.log("❌ No input files/folders provided.")
            return False

        if output_pdf:
            if not PDF_SUPPORT:
                self.log("❌ PDF support not available. Install 'img2pdf'.")
                return False
            if not output_path.lower().endswith('.pdf'):
                output_path = output_path.rsplit('.', 1)[0] + '.pdf'
        else:
            if not output_path.lower().endswith('.cbz'):
                output_path = output_path.rsplit('.', 1)[0] + '.cbz'

        with tempfile.TemporaryDirectory() as temp_dir:
            all_images = []
            total = len(input_items)
            self.log(f"📚 Processing {total} item(s)...")
            self.update_progress(0, "Starting...")

            for idx, item_path in enumerate(input_items):
                item_name = Path(item_path).stem if os.path.isfile(item_path) else Path(item_path).name
                is_folder = os.path.isdir(item_path)

                if is_folder:
                    self.log(f"📁 [{idx + 1}/{total}] {Path(item_path).name}")
                    self.update_progress((idx / total) * 50, f"Processing {idx + 1}/{total}")
                    images = self.collect_images_by_subfolder(item_path)
                else:
                    ext = Path(item_path).suffix.lower()
                    icon = "📘" if ext == ".cbz" else "📕" if ext == ".cbr" else "📦"
                    self.log(f"{icon} [{idx + 1}/{total}] {Path(item_path).name}")
                    self.update_progress((idx / total) * 50, f"Extracting {idx + 1}/{total}")
                    extract_dir = os.path.join(temp_dir, f"{idx:04d}_{item_name}")
                    os.makedirs(extract_dir, exist_ok=True)
                    if not self.extract_archive(item_path, extract_dir):
                        continue
                    images = self.collect_images_by_subfolder(extract_dir)

                for subfolder, img_path in images:
                    all_images.append((idx, item_name, subfolder, img_path))
                self.log(f"   ✓ {len(images)} images")

            if not all_images:
                self.log("❌ No images found.")
                return False

            fmt = "PDF" if output_pdf else "CBZ"
            self.log(f"\n📦 Creating {fmt} ({len(all_images)} images)...")
            self.update_progress(50, f"Creating {fmt}...")

            try:
                if output_pdf:
                    image_paths = []
                    for i, (_, _, _, img_path) in enumerate(all_images):
                        ext = Path(img_path).suffix.lower()
                        if ext in {'.jpg', '.jpeg', '.png'}:
                            image_paths.append(img_path)
                        else:
                            try:
                                from PIL import Image
                                img = Image.open(img_path)
                                converted = os.path.join(temp_dir, f"{i:05d}.png")
                                img.save(converted, 'PNG')
                                image_paths.append(converted)
                            except ImportError:
                                self.log(f"   ⚠️ Skipping {Path(img_path).name} (install Pillow for conversion)")
                        self.update_progress(50 + ((i + 1) / len(all_images)) * 40, f"Preparing {i + 1}/{len(all_images)}")
                    self.update_progress(90, "Writing PDF...")
                    with open(output_path, "wb") as f:
                        f.write(img2pdf.convert(image_paths))
                else:
                    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for i, (_, _, _, img_path) in enumerate(all_images):
                            ext = Path(img_path).suffix
                            zf.write(img_path, f"{i + 1:05d}{ext}")
                            self.update_progress(50 + ((i + 1) / len(all_images)) * 50, f"Adding {i + 1}/{len(all_images)}")

                size_mb = os.path.getsize(output_path) / (1024 * 1024)
                self.log(f"\n✅ Created: {Path(output_path).name}")
                self.log(f"   📄 {len(all_images)} pages • {size_mb:.1f} MB")
                self.update_progress(100, "Complete!")
                return True
            except Exception as e:
                self.log(f"❌ Error: {e}")
                return False


class SmartNamer:
    """Suggests a merged output filename from a list of input file stems."""

    def suggest(self, stems: list, extension: str) -> str:
        if not stems:
            return f"Merged{extension}"
        if len(stems) == 1:
            return f"{stems[0]}{extension}"

        numbers = [self._last_number(s) for s in stems]
        if any(n is None for n in numbers):
            return f"{stems[0]}_Merged{extension}"

        prefixes = [self._prefix_before_last_number(s) for s in stems]
        common = self._common_prefix(prefixes).rstrip(" -_.")

        min_n, max_n = min(numbers), max(numbers)
        if min_n == max_n:
            return f"{stems[0]}{extension}"

        if common:
            return f"{common} {min_n}-{max_n}{extension}"
        return f"{min_n}-{max_n}{extension}"

    def _last_number(self, stem: str) -> Optional[int]:
        parts = re.split(r'(\d+)', stem)
        for part in reversed(parts):
            if part.isdigit():
                return int(part)
        return None

    def _prefix_before_last_number(self, stem: str) -> str:
        parts = re.split(r'(\d+)', stem)
        last_digit_idx = -1
        for i, p in enumerate(parts):
            if p.isdigit():
                last_digit_idx = i
        if last_digit_idx == -1:
            return stem
        return ''.join(parts[:last_digit_idx])

    def _common_prefix(self, strings: list) -> str:
        if not strings:
            return ''
        prefix = strings[0]
        for s in strings[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ''
        return prefix


if __name__ == "__main__":
    print("CBZMerger core loaded OK")
