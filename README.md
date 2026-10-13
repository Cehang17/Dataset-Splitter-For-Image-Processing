# Dataset Splitter & Pruner for Image Processing

A Python utility designed to randomly prune, split, or downsample image processing datasets (such as YOLO object detection datasets) while keeping corresponding annotation/label files (`.txt`) strictly synchronized.

---

## 🚀 Features

- **Synchronized Label Deletion / Moving:** When an image is moved or deleted, its corresponding YOLO-format `.txt` label in the `labels/` directory is automatically handled alongside it.
- **Safe Mode / Backup:** By default, files are moved into a `silinenler/` (deleted/backup) folder instead of permanent deletion.
- **Permanent Deletion Support:** Optional flag to directly purge files if disk space is needed.
- **Dry-Run Mode:** Test what files would be affected without touching or modifying any actual files.
- **Reproducible Results:** Seed support (`random.seed`) guarantees repeatable selections across multiple runs.
- **Broad Format Support:** Compatible with `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`, `.tif`, and `.tiff`.
- **Zero External Dependencies:** Built entirely with Python standard libraries (`pathlib`, `shutil`, `random`, `os`).

---

## 📁 Expected Directory Structure

```text
dataset/
├── images/
│   ├── 0001.jpg
│   ├── 0002.jpg
│   └── ...
└── labels/
    ├── 0001.txt
    ├── 0002.txt
    └── ...
```

---

## ⚙️ Configuration

Open `silici.py` and adjust the configuration block as needed:

```python
# ================== AYARLAR / SETTINGS ==================
# images ve labels klasörlerinin bulunduğu ana klasör
ANA_KLASOR = Path(".")       # Varsayılan: Çalıştırılan dizin (veya özel yol örn: Path(r"C:\veri_seti"))
IMAGES_KLASOR = ANA_KLASOR / "images"
LABELS_KLASOR = ANA_KLASOR / "labels"

SILME_ORANI = 0.65          # Silinecek / ayrılacak oran (%65)
SEED = 42                   # Tekrarlanabilir sonuç için sabit seed (rastgele için None)
DRY_RUN = False              # True ise sadece önizleme yapar, hiçbir dosya değiştirilmez
KALICI_SIL = False          # False: "silinenler" klasörüne yedekleyerek taşır (güvenli)
                            # True : dosyaları diskten kalıcı olarak siler
# ========================================================
```

---

## 💻 Usage

Run the script using Python 3:

```bash
python silici.py
```

### Example Output:

```text
Toplam resim       : 2000
Silinecek (%65)    : 1300
Kalacak            : 700
Mod                : TAŞI (yedekli)
--------------------------------------------------
İşlenen resim      : 1300
İşlenen etiket     : 1300
Etiketi olmayan    : 0

Bitti.
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
