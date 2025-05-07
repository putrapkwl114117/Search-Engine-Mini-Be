Berikut adalah isi file `README.md` untuk proyek Django kamu (Search Engine Mini) agar orang lain bisa menjalankannya setelah clone. Saya sesuaikan dengan penggunaan `venv`, dua file CSV di folder `data`, dan migrasi data ke database.

---

```markdown
# Search Engine Mini (Django + Whoosh)

Proyek ini adalah backend Search Engine Mini yang dibangun dengan **Django** dan menggunakan **Whoosh** sebagai engine pencarian teks full-text. Project ini membaca dua file CSV dari folder `data/` dan memasukkan datanya ke database.

## Struktur Folder

```

search-engine-be-app/
?
??? data/
?   ??? halodoc\_articles\_cleaned\_stage1.csv
?   ??? halodoc\_articles\_cleaned\_stage2.csv
?
??? manage.py
??? search\_engine/          # Aplikasi Django kamu
??? ...

````

## Cara Menjalankan Proyek

### 1. Clone Repository

```bash
git clone https://github.com/putrapkwl114117/Search-Engine-Mini-Be.git
cd Search-Engine-Mini-Be
````

### 2. Buat dan Aktifkan Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# atau
source venv/bin/activate  # Mac/Linux
```

### 3. Install Dependency

```bash
pip install -r requirements.txt
```

> Pastikan file `requirements.txt` sudah tersedia. Jika belum, buat dengan:
>
> ```bash
> pip freeze > requirements.txt
> ```

### 4. Jalankan Migrasi Database

```bash
python manage.py migrate
```

### 5. Masukkan Data dari CSV ke Database

Jalankan perintah custom Django management (pastikan kamu sudah buat script-nya):

```bash
python manage.py import_csv_stage1
python manage.py import_csv_stage2
```

> Kedua perintah di atas adalah contoh **custom command** Django untuk mengimpor `halodoc_articles_cleaned_stage1.csv` dan `halodoc_articles_cleaned_stage2.csv`. Pastikan kamu sudah menyiapkan file `import_csv_stage1.py` dan `import_csv_stage2.py` di dalam folder:
>
> ```
> search_engine/management/commands/
> ```

### 6. Jalankan Server Django

```bash
python manage.py runserver
```

Server akan berjalan di: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Catatan Tambahan

* Gunakan Whoosh untuk indexing dan pencarian.
* Jangan lupa untuk meng-**exclude** folder `venv/` dan file tidak penting lainnya dengan `.gitignore`.

```

