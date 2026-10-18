import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from PIL import Image, ImageTk, ImageDraw, ImageFont

# ================== AYARLAR ==================
# Boş bırakırsan açılışta klasör seçtirir. İstersen varsayılan yolu yazabilirsin:
VARSAYILAN_KLASOR = ""   # örn: r"C:\Users\KULLANICI\Desktop\veri_seti"
# =============================================

RESIM_UZANTILARI = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
RENKLER = [
    "#ff3b30", "#34c759", "#0a84ff", "#ffcc00", "#ff2d92",
    "#00c7be", "#ff9500", "#af52de", "#a2845e", "#5ac8fa",
]


def sinif_isimlerini_oku(ana: Path):
    """data.yaml veya classes.txt varsa sınıf isimlerini okur."""
    isimler = []
    classes_txt = ana / "classes.txt"
    if classes_txt.exists():
        isimler = [s.strip() for s in classes_txt.read_text(encoding="utf-8").splitlines() if s.strip()]
        return isimler

    yaml_yolu = ana / "data.yaml"
    if yaml_yolu.exists():
        try:
            import yaml  # pip install pyyaml (opsiyonel)
            veri = yaml.safe_load(yaml_yolu.read_text(encoding="utf-8"))
            n = veri.get("names", [])
            if isinstance(n, dict):
                isimler = [n[k] for k in sorted(n)]
            else:
                isimler = list(n)
        except Exception:
            pass
    return isimler


def etiket_oku(txt_yolu: Path):
    """YOLO formatı: sinif x_merkez y_merkez genislik yukseklik (0-1 arası).
    Poligon (segmentasyon) satırı gelirse bbox'a çevirir."""
    kutular = []
    if not txt_yolu.exists():
        return kutular
    for satir in txt_yolu.read_text(encoding="utf-8").splitlines():
        p = satir.split()
        if len(p) < 5:
            continue
        try:
            sinif = int(float(p[0]))
            degerler = list(map(float, p[1:]))
        except ValueError:
            continue
        if len(degerler) == 4:
            xc, yc, w, h = degerler
        else:
            xs, ys = degerler[0::2], degerler[1::2]
            xc, yc = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
            w, h = max(xs) - min(xs), max(ys) - min(ys)
        kutular.append((sinif, xc, yc, w, h))
    return kutular


class Uygulama:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("YOLO BBox Visualizer")
        root.geometry("1100x760")

        self.resimler = []
        self.index = 0
        self.images_klasor = None
        self.labels_klasor = None
        self.sinif_isimleri = []
        self.tk_img = None

        # --- Üst bar ---
        ust = tk.Frame(root)
        ust.pack(fill="x", padx=6, pady=6)
        tk.Button(ust, text="Klasör Seç", command=self.klasor_sec).pack(side="left")
        tk.Button(ust, text="◀ Önceki", command=self.onceki).pack(side="left", padx=(12, 2))
        tk.Button(ust, text="Sonraki ▶", command=self.sonraki).pack(side="left", padx=2)

        tk.Label(ust, text="Git (no):").pack(side="left", padx=(12, 2))
        self.git_var = tk.StringVar()
        giris = tk.Entry(ust, textvariable=self.git_var, width=7)
        giris.pack(side="left")
        giris.bind("<Return>", lambda e: self.git())

        self.sadece_etiketsiz = tk.BooleanVar(value=False)
        self.kutu_yazi = tk.BooleanVar(value=True)
        tk.Checkbutton(ust, text="Sınıf adı göster", variable=self.kutu_yazi,
                       command=self.goster).pack(side="left", padx=(16, 0))

        self.bilgi = tk.Label(ust, text="", anchor="e")
        self.bilgi.pack(side="right")

        # --- Canvas ---
        self.canvas = tk.Canvas(root, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=6)
        self.canvas.bind("<Configure>", lambda e: self.goster())

        # --- Alt bar ---
        self.alt = tk.Label(root, text="", anchor="w", justify="left")
        self.alt.pack(fill="x", padx=8, pady=4)

        # --- Kısayollar ---
        root.bind("<Left>", lambda e: self.onceki())
        root.bind("<Right>", lambda e: self.sonraki())
        root.bind("a", lambda e: self.onceki())
        root.bind("d", lambda e: self.sonraki())
        root.bind("<Prior>", lambda e: self.atla(-50))   # PageUp
        root.bind("<Next>", lambda e: self.atla(50))     # PageDown
        root.bind("<Home>", lambda e: self.git_index(0))
        root.bind("<End>", lambda e: self.git_index(len(self.resimler) - 1))

        if VARSAYILAN_KLASOR:
            self.klasor_yukle(Path(VARSAYILAN_KLASOR))
        else:
            root.after(200, self.klasor_sec)

    # ---------- Klasör ----------
    def klasor_sec(self):
        yol = filedialog.askdirectory(title="images ve labels klasörlerinin bulunduğu ana klasörü seç")
        if yol:
            self.klasor_yukle(Path(yol))

    def klasor_yukle(self, ana: Path):
        img_k, lbl_k = ana / "images", ana / "labels"
        if not img_k.is_dir() or not lbl_k.is_dir():
            messagebox.showerror("Hata", "Seçilen klasörde 'images' ve 'labels' klasörleri bulunamadı.")
            return
        self.images_klasor, self.labels_klasor = img_k, lbl_k
        self.resimler = sorted(p for p in img_k.iterdir()
                               if p.is_file() and p.suffix.lower() in RESIM_UZANTILARI)
        if not self.resimler:
            messagebox.showerror("Hata", "images klasöründe resim yok.")
            return
        self.sinif_isimleri = sinif_isimlerini_oku(ana)
        self.index = 0
        self.goster()

    # ---------- Gezinme ----------
    def onceki(self):
        self.atla(-1)

    def sonraki(self):
        self.atla(1)

    def atla(self, n):
        if self.resimler:
            self.index = max(0, min(len(self.resimler) - 1, self.index + n))
            self.goster()

    def git_index(self, i):
        if self.resimler:
            self.index = max(0, min(len(self.resimler) - 1, i))
            self.goster()

    def git(self):
        try:
            self.git_index(int(self.git_var.get()) - 1)
        except ValueError:
            pass

    # ---------- Çizim ----------
    def goster(self):
        if not self.resimler:
            return
        resim_yolu = self.resimler[self.index]
        etiket_yolu = self.labels_klasor / (resim_yolu.stem + ".txt")

        img = Image.open(resim_yolu).convert("RGB")
        W, H = img.size

        cw = max(self.canvas.winfo_width(), 50)
        ch = max(self.canvas.winfo_height(), 50)
        oran = min(cw / W, ch / H)
        yw, yh = max(1, int(W * oran)), max(1, int(H * oran))
        img = img.resize((yw, yh), Image.LANCZOS)

        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except Exception:
            font = ImageFont.load_default()

        kutular = etiket_oku(etiket_yolu)
        for sinif, xc, yc, w, h in kutular:
            x1, y1 = (xc - w / 2) * yw, (yc - h / 2) * yh
            x2, y2 = (xc + w / 2) * yw, (yc + h / 2) * yh
            renk = RENKLER[sinif % len(RENKLER)]
            draw.rectangle([x1, y1, x2, y2], outline=renk, width=3)
            if self.kutu_yazi.get():
                ad = self.sinif_isimleri[sinif] if sinif < len(self.sinif_isimleri) else str(sinif)
                tb = draw.textbbox((x1, y1), ad, font=font)
                draw.rectangle([tb[0] - 2, tb[1] - 16, tb[2] + 2, tb[1]], fill=renk)
                draw.text((x1, y1 - 16), ad, fill="white", font=font)

        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(cw // 2, ch // 2, image=self.tk_img, anchor="center")

        self.bilgi.config(text=f"{self.index + 1} / {len(self.resimler)}")
        etiket_durum = f"{len(kutular)} kutu" if etiket_yolu.exists() else "ETİKET DOSYASI YOK"
        self.alt.config(text=f"{resim_yolu.name}   |   {W}x{H}   |   {etiket_durum}   |   "
                             f"Kısayollar: ← → (veya A/D), PgUp/PgDn = 50 atla, Home/End")


if __name__ == "__main__":
    root = tk.Tk()
    Uygulama(root)
    root.mainloop()
