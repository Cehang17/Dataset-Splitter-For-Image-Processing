# Dataset Splitter & Visualizer for Image Processing

A practical Python toolkit for computer vision and object detection workflows (such as YOLO). It provides tools to inspect, prune, downsample, and visualize datasets while keeping images and annotation/label files (`.txt`) strictly synchronized.

---

## 📦 Included Tools

| Script | Description | Requirements |
| :--- | :--- | :--- |
| **`silici.py`** | Randomly prunes or splits datasets by ratio while keeping labels in sync | Standard Python libraries |
| **`bbox_goruntuleyici.py`** | Lightweight desktop GUI to visualize & inspect YOLO bounding boxes & labels | Pillow, PyYAML (optional) |

---

## 📁 Expected Dataset Structure

The tools are designed to work seamlessly with the standard YOLO dataset format:

```text
dataset/
├── classes.txt        # (Optional) Class names, one per line
├── data.yaml          # (Optional) YOLO data configuration file
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

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Cehang17/Dataset-Splitter-For-Image-Processing.git
   cd Dataset-Splitter-For-Image-Processing
   ```

2. (Optional, required for visualizer GUI) Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 1️⃣ Dataset Splitter & Pruner (`silici.py`)

A script to downsample or split large image datasets without leaving orphaned label files.

### ✨ Features
- **Synchronized Label Moving/Deletion:** When an image is moved or deleted, its corresponding YOLO `.txt` label is automatically moved or deleted too.
- **Safe Mode / Backup:** By default, files are moved into a `silinenler/` folder instead of permanently deleting them.
- **Permanent Deletion Support:** Optional flag (`KALICI_SIL = True`) to directly purge files if disk space is needed.
- **Dry-Run Mode:** Preview how many images/labels will be affected without modifying any files.
- **Reproducible Seed:** Guarantees repeatable selections across runs with `SEED = 42`.
- **Zero External Dependencies:** Built with pure Python standard library (`pathlib`, `shutil`, `random`, `os`).

### ⚙️ Configuration
Edit the settings in `silici.py`:

```python
ANA_KLASOR = Path(".")       # Root folder containing images/ and labels/
SILME_ORANI = 0.65          # Fraction of dataset to remove/split (e.g., 65%)
SEED = 42                   # Fixed seed for reproducibility
DRY_RUN = False              # Set True for preview without modifying files
KALICI_SIL = False          # False: safely backup to 'silinenler', True: permanently delete
```

### 💻 Run
```bash
python silici.py
```

---

## 2️⃣ YOLO BBox & Annotation Visualizer (`bbox_goruntuleyici.py`)

An interactive desktop application built with Tkinter and Pillow to quickly verify annotations, inspect bounding boxes, and find unlabeled images.

### ✨ Features
- **Fast & Responsive GUI:** Renders images dynamically as the window resizes.
- **Bounding Box & Polygon Support:** Parses normalized YOLO format (`class x_center y_center width height`) and automatically handles segmentation polygon points.
- **Auto Class Names:** Automatically reads class names from `classes.txt` or `data.yaml`.
- **High-Contrast Colors:** Distinct color coding for each class ID.
- **Interactive Navigation:**
  - `←` / `A`: Previous image
  - `→` / `D`: Next image
  - `PageUp`: Jump back 50 images
  - `PageDown`: Jump forward 50 images
  - `Home` / `End`: Jump to first / last image
  - `Git (no)` input box: Direct jump to a specific image index
  - Toggle class label display checkbox

### 💻 Run
```bash
python bbox_goruntuleyici.py
```
Click **"Klasör Seç"** to select your dataset folder containing `images/` and `labels/`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
