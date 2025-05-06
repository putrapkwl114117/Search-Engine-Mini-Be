from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serach_engine.settings")
django.setup()

from search_article.models import Article

index_dir = "index"

# Schema: tambahkan ID dari DB untuk digunakan di pencarian
schema = Schema(
    id=ID(stored=True),  # id artikel dari database
    judul=TEXT(stored=True),
    konten=TEXT(stored=True),
    url=TEXT(stored=True),
    gambar=TEXT(stored=True)
)

# Buat index jika belum ada
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

ix = create_in(index_dir, schema)
writer = ix.writer()

articles = Article.objects.all()

for article in articles:
    writer.add_document(
        id=str(article.id),
        judul=article.judul,
        konten=article.cleaned_isi,
        url=article.url,
        gambar=article.gambar
    )

writer.commit()
print("? Indexing selesai!")
