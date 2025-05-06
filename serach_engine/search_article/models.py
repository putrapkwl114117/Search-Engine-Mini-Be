from django.db import models

class Article(models.Model):
    url = models.URLField()
    judul = models.CharField(max_length=255)
    gambar = models.URLField(blank=True, null=True)
    content = models.TextField()  
    cleaned_isi = models.TextField(blank=True, null=True) 
    tanggal = models.DateField()

    def __str__(self):
        return self.judul
