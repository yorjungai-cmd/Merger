# CBZ Merger 2.1.1

**Crafted by Yor Anupong**

> รวมไฟล์การ์ตูน CBZ / CBR / ZIP / RAR และโฟลเดอร์รูปภาพหลายไฟล์เข้าเป็นไฟล์เดียว
> ออกแบบมาสำหรับ Windows · PyQt6 · Operational Clean UI · Light/Dark theme

---

## ฟีเจอร์หลัก

| ฟีเจอร์ | รายละเอียด |
|---|---|
| **Merge archives** | รวม CBZ, CBR, ZIP, RAR และโฟลเดอร์รูปภาพเข้าเป็นไฟล์เดียว |
| **Smart Auto-naming** | วิเคราะห์ชื่อไฟล์อัตโนมัติ เช่น `Title (1).cbz + (2).cbz` → `Title (1-2).cbz` |
| **Add Folder** | รองรับโฟลเดอร์ที่มีไฟล์ archive หรือรูปภาพข้างใน |
| **PDF Export** | ส่งออกเป็น PDF ได้ (ต้องติดตั้ง `img2pdf`) |
| **Drag & Drop** | ลากไฟล์/โฟลเดอร์วางลงได้ทันที |
| **Drag reorder** | ลากรายการใน list เพื่อเปลี่ยนลำดับการ merge ได้โดยตรง |
| **Image counts** | แสดงจำนวนรูปในแต่ละไฟล์ และจำนวนรูปทั้งหมดตามรายการที่จะ merge |
| **Operational Clean UI** | UI แบบเรียบ คม อ่านรายการไฟล์และ metadata ได้ง่ายขึ้น |
| **Light / Dark Theme** | สลับธีมด้วยปุ่มเดียว บันทึกค่าอัตโนมัติ |
| **Natural Sort** | เรียง img1 → img2 → img10 ถูกต้อง (ไม่ใช่ img1 → img10 → img2) |
| **Background Thread** | ประมวลผลใน background UI ไม่ค้าง |
| **Auto-clear** | ล้าง list อัตโนมัติหลัง merge สำเร็จ |

---

## ดาวน์โหลด

**[CBZ-Merger.exe](dist/CBZ-Merger.exe)** — ไฟล์เดียว ไม่ต้องติดตั้ง Python

---

## วิธีใช้งาน

1. **เพิ่มไฟล์** — กด **＋ Add Files** หรือ **📁 Add Folder** หรือลากไฟล์วางลงใน list
2. **จัดลำดับ** — ลากรายการใน list เพื่อเรียงลำดับ หรือใช้ปุ่ม ▲ ▼ ก็ได้
3. **ตั้งค่า** — เปิด *Auto-name with smart range* และ/หรือ *Export as PDF*
4. **Merge** — กด **🔀 Merge to CBZ** (หรือ Merge to PDF) เลือกที่บันทึก
5. List และ Log จะล้างอัตโนมัติหลัง merge สำเร็จ

จำนวนรูปจะแสดงหลังขนาดไฟล์ เช่น `72.6 MB · 184 images` และ smart name bar จะแสดงจำนวนรูปทั้งหมดหลังรวมไฟล์

---

## Smart Auto-naming

ระบบวิเคราะห์ชื่อไฟล์ทั้งหมดแล้วเสนอชื่อ output อัตโนมัติ:

| Input files | ผลลัพธ์ที่เสนอ |
|---|---|
| `[Author] Title (1).cbz`, `(2).cbz`, `(3).cbz` | `[Author] Title (1-3).cbz` |
| `Manga Vol 1.cbz`, `Manga Vol 2.cbz` | `Manga Vol 1-2.cbz` |
| `A 1.cbz`, `A asdfasdf 3.cbz` | `A 1-3.cbz` (min-max) |
| `Alpha.cbz`, `Beta.cbz` (ไม่มีตัวเลข) | `Alpha_Merged.cbz` |
| ไฟล์เดียว | ชื่อเดิม |

ชื่อที่เสนอยังแก้ไขได้ในหน้า Save dialog

---

## รูปแบบที่รองรับ

### Input

| รูปแบบ | นามสกุล | หมายเหตุ |
|---|---|---|
| Comic Book ZIP | `.cbz` | Built-in |
| Comic Book RAR | `.cbr` | ต้องติดตั้ง `rarfile` |
| ZIP archive | `.zip` | Built-in |
| RAR archive | `.rar` | ต้องติดตั้ง `rarfile` |
| โฟลเดอร์รูปภาพ | directory | JPG, PNG, GIF, WebP, BMP, TIFF |
| โฟลเดอร์ archive | directory | โฟลเดอร์ที่มีไฟล์ .cbz/.zip/.cbr/.rar |

### Output

| รูปแบบ | นามสกุล | หมายเหตุ |
|---|---|---|
| Comic Book ZIP | `.cbz` | Default |
| PDF | `.pdf` | ต้องติดตั้ง `img2pdf` |

---

## ติดตั้งและรัน (Developer)

### Requirements

| Package | Required | หน้าที่ |
|---|---|---|
| Python 3.10+ | Required | Runtime |
| PyQt6 >= 6.6 | Required | UI framework |
| rarfile >= 4.0 | Optional | CBR/RAR extraction |
| img2pdf >= 0.4 | Optional | PDF export |
| Pillow >= 10.0 | Optional | Image conversion for PDF |

### ติดตั้ง

```bash
git clone https://github.com/yorjungai-cmd/Merger.git
cd Merger
pip install -r requirements.txt
python cbz_merger.py
```

### Minimal install (CBZ เท่านั้น)

```bash
pip install PyQt6
python cbz_merger.py
```

---

## Build .exe

```bash
pip install pyinstaller
build.bat
```

Output: `dist/CBZ-Merger.exe` — single file, ไม่ต้องติดตั้ง Python บนเครื่องปลายทาง

---

## โครงสร้างโปรเจกต์

```
Merger/
├── cbz_merger.py           ← Single-file application (ทุก class อยู่ที่นี่)
├── requirements.txt        ← Python dependencies
├── build.bat               ← PyInstaller build script
├── tests/
│   ├── test_core.py             ← CBZMerger unit tests (15 tests)
│   ├── test_file_list_widget.py ← FileListWidget unit tests (4 tests)
│   ├── test_main_window_layout.py ← MainWindow layout tests (1 test)
│   └── test_smart_namer.py      ← SmartNamer unit tests (12 tests)
└── docs/
    └── superpowers/
        ├── specs/          ← Design specification
        └── plans/          ← Implementation plan
```

---

## Architecture

`cbz_merger.py` ประกอบด้วย 5 classes:

| Class | หน้าที่ |
|---|---|
| `CBZMerger` | Core logic — extract archive, collect images, create CBZ/PDF |
| `SmartNamer` | วิเคราะห์ชื่อไฟล์ — เสนอชื่อ output จาก pattern |
| `MergeWorker(QThread)` | Background thread — รัน merge ผ่าน Qt signals |
| `FileListWidget(QWidget)` | File list panel — drag & drop, add/remove/reorder |
| `MainWindow(QMainWindow)` | Application window — layout, theme, orchestration |

---

## Tests

```bash
pytest tests/ -v
```

Expected: **32 tests passed**

---

## Changelog

ดู [CHANGELOG.md](CHANGELOG.md) สำหรับประวัติการเปลี่ยนแปลง

---

## License

MIT — free to use, modify, and distribute.

---

*CBZ Merger 2.1.1 · Crafted by Yor Anupong*
