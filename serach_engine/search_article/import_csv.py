import csv
import os
import sys
import re
from datetime import datetime
import django
import locale

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serach_engine.settings")
django.setup()

from django.conf import settings
from search_article.models import Article

# Path file CSV
csv_original = os.path.join(settings.BASE_DIR, "data/halodoc_articles_cleaned_stage1.csv")
csv_cleaned = os.path.join(settings.BASE_DIR, "data/halodoc_articles_cleaned_stage2.csv")

locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

def convert_to_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %B %Y").date()
    except ValueError:
        print(f"Format tanggal salah: {date_str}")
        return None

# Fungsi untuk membersihkan konten (hapus tanda baca dan angka, huruf kecil semua)
def clean_content(text):
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
    cleaned_text = cleaned_text.lower()
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def import_csv_to_db():
    total_data = 0  

    try:
        with open(csv_cleaned, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            cleaned_data = list(reader)  # Simpan data CSV stage 2 dalam bentuk list of dict

        with open(csv_original, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                Tanggal = row["Tanggal"].strip()  
                Tanggal = convert_to_date(Tanggal)

                # Ambil Konten langsung dari CSV stage 2 untuk kolom cleaned_isi berdasarkan urutan baris
                cleaned_isi = cleaned_data[index]["Konten"]

                article = Article(
                    url=row["URL"],
                    judul=row["Judul"],
                    gambar=row.get("Gambar", ""),  
                    content=row["Konten"],
                    cleaned_isi=cleaned_isi,  # Ambil dari CSV stage 2
                    tanggal=Tanggal
                )
                article.save()
                total_data += 1  

        print(f"? Data berhasil diproses dan disimpan ke database! Total data: {total_data} artikel.")
    except Exception as e:
        print(f"? Terjadi kesalahan: {e}")

if __name__ == "__main__":
    import_csv_to_db()
