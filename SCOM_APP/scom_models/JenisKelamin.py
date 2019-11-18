from django.db import models

class JenisKelamin(models.Model):
    jenis = models.CharField(max_length=15)
    