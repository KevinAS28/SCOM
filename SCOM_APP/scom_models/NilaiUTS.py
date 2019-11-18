
from django.db import models
from SCOM_APP.scom_models.Mapel import Mapel
from SCOM_APP.scom_models.InfoSiswa import InfoSiswa

class NilaiUTS(models.Model):
    nis = models.ForeignKey(InfoSiswa, on_delete=models.CASCADE, default=1)
    nilai = models.DecimalField(max_length=11, decimal_places=3, max_digits=5)
    #id_mapel = models.IntegerField(default=0)
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE, default=1)

