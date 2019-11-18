from django.db import models
from SCOM_APP.scom_models.InfoSiswa import InfoSiswa
from SCOM_APP.scom_models.InfoGuru import InfoGuru

class Kelas(models.Model):
    nip_wali_kelas = models.ForeignKey(InfoGuru, on_delete=models.CASCADE, default=1)
    nis_ketua_kelas = models.ForeignKey(InfoSiswa, on_delete=models.CASCADE, default=1)
    nis_wakil_ketua_kelas = models.ForeignKey(InfoSiswa, on_delete=models.CASCADE, default=1)