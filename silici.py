import os
import random
import shutil
from pathlib import Path

# ================== AYARLAR / SETTINGS ==================
# images ve labels klasörlerinin bulunduğu ana klasör.
# Varsayılan olarak scriptin çalıştığı dizindir (veya özel yol girebilirsiniz: örn. Path(r"C:\veri_seti"))
ANA_KLASOR = Path(".")
IMAGES_KLASOR = ANA_KLASOR / "images"
LABELS_KLASOR = ANA_KLASOR / "labels"

SILME_ORANI = 0.65          # veri setinin %65'i silinecek / ayrılacak
SEED = 42                   # aynı sonucu tekrar almak için (None yaparsan her seferinde farklı)
DRY_RUN = False              # True: sadece ne yapacağını gösterir, HİÇBİR ŞEY SİLMEZ
KALICI_SIL = False          # False: silinecekleri "silinenler" klasörüne taşır (güvenli)
                            # True : kalıcı olarak siler
# ========================================================

RESIM_UZANTILARI = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def main():
    if not IMAGES_KLASOR.is_dir() or not LABELS_KLASOR.is_dir():
        print(f"HATA: '{IMAGES_KLASOR}' veya '{LABELS_KLASOR}' klasörü bulunamadı.")
        print("Lütfen ANA_KLASOR ayarını veya images/labels klasörlerinin konumunu kontrol edin.")
        return

    # Resimleri topla
    resimler = [p for p in IMAGES_KLASOR.iterdir()
                if p.is_file() and p.suffix.lower() in RESIM_UZANTILARI]

    if not resimler:
        print(f"HATA: '{IMAGES_KLASOR}' klasöründe resim bulunamadı.")
        return

    toplam = len(resimler)
    silinecek_sayi = round(toplam * SILME_ORANI)

    if SEED is not None:
        random.seed(SEED)
    silinecekler = random.sample(resimler, silinecek_sayi)

    print(f"Toplam resim       : {toplam}")
    print(f"Silinecek (%{int(SILME_ORANI*100)})    : {silinecek_sayi}")
    print(f"Kalacak            : {toplam - silinecek_sayi}")
    print(f"Mod                : {'DRY-RUN (silme yok)' if DRY_RUN else ('KALICI SİL' if KALICI_SIL else 'TAŞI (yedekli)')}")
    print("-" * 50)

    yedek_img = ANA_KLASOR / "silinenler" / "images"
    yedek_lbl = ANA_KLASOR / "silinenler" / "labels"
    if not DRY_RUN and not KALICI_SIL:
        yedek_img.mkdir(parents=True, exist_ok=True)
        yedek_lbl.mkdir(parents=True, exist_ok=True)

    silinen_resim = 0
    silinen_etiket = 0
    etiketsiz = 0

    for resim in silinecekler:
        etiket = LABELS_KLASOR / (resim.stem + ".txt")

        if DRY_RUN:
            silinen_resim += 1
            if etiket.exists():
                silinen_etiket += 1
            else:
                etiketsiz += 1
            continue

        # Resim
        if KALICI_SIL:
            resim.unlink()
        else:
            shutil.move(str(resim), str(yedek_img / resim.name))
        silinen_resim += 1

        # Etiket
        if etiket.exists():
            if KALICI_SIL:
                etiket.unlink()
            else:
                shutil.move(str(etiket), str(yedek_lbl / etiket.name))
            silinen_etiket += 1
        else:
            etiketsiz += 1

    print(f"İşlenen resim      : {silinen_resim}")
    print(f"İşlenen etiket     : {silinen_etiket}")
    print(f"Etiketi olmayan    : {etiketsiz}")
    if DRY_RUN:
        print("\nBu bir deneme çalıştırmasıydı. Gerçekten uygulamak için DRY_RUN = False yap.")
    else:
        print("\nBitti.")


if __name__ == "__main__":
    main()
