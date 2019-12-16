from django.db import models
from django.contrib.auth.models import AbstractUser

class Mapel(models.Model):
    nama = models.CharField(max_length = 25)
    kkm = models.IntegerField(default=0)

class InfoGuru(models.Model):
    nip = models.CharField(max_length=15, unique=True)
    nama = models.CharField(max_length = 50, unique=True)
    #id_jurusan = models.IntegerField(default=0)
    nuptk = models.CharField(max_length=15)
    tanggal_lahir = models.DateField()
    tempat_lahir = models.CharField(max_length = 50)
    alamat = models.CharField(max_length = 50)
    status_aktif = models.BooleanField()
    def get_data(self):
        return [self.nip, self.nama, self.nuptk, self.tanggal_lahir, self.tempat_lahir, self.alamat, "Aktif" if self.status_aktif else "Tidak Aktif"]
    

class Jurusan(models.Model):
    nama_jurusan = models.CharField(max_length=50)
    nama_singkatan_jurusan = models.CharField(max_length=10, default="-")
    kepala_program = models.ForeignKey(InfoGuru, on_delete=models.CASCADE, default=1)
    status_aktif = models.IntegerField(default=1)

class InfoSiswa(models.Model):
    nis = models.CharField(max_length=15, unique=True)
    nama = models.CharField(max_length = 50)
    #id_kelas = models.IntegerField(default=0)
    tingkat_kelas = models.IntegerField(default=10)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, default=1)
    tanggal_lahir = models.DateField()
    tempat_lahir = models.CharField(max_length = 50)
    alamat = models.CharField(max_length = 50)
    status_aktif = models.BooleanField()
    #id_jk = models.IntegerField(default=0)
    jk = models.BooleanField(default=True)
    def get_data(self):
        return [self.nis, self.nama, self.tingkat_kelas, self.jurusan.nama_singkatan_jurusan, self.tanggal_lahir, self.tempat_lahir, self.alamat, "Aktif" if self.status_aktif else "Tidak Aktif", "Laki-laki" if self.jk else "Perempuan"]



class Kelas(models.Model):
    tingkat = models.IntegerField(default=10)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, default=1)
    nip_wali_kelas = models.ForeignKey(InfoGuru, on_delete=models.CASCADE, default=1)
    nis_ketua_kelas = models.ForeignKey(InfoSiswa, on_delete=models.CASCADE, default=1, related_name="ketua_kelas")
    nis_wakil_ketua_kelas = models.ForeignKey(InfoSiswa, on_delete=models.CASCADE, default=1, related_name="wakil_ketua_kelas")

    @property
    def nama(self):
        return "{tingkat} {jurusan}".format(tingkat=str(self.tingkat), jurusan=self.jurusan.nama_jurusan)

    @nama.setter
    def nama(self, val):
        val = val.split(" ")
        if (len(val)!=2):
            raise ValueError("Kelas.nama should be in format 'tingkat_kelas nama_jurusan'")
        else:
            tingkat, jurusan = val
            jurusan_data = Jurusan.objects.filter(nama_singkatan_jurusan=jurusan)
            if (len(jurusan_data)!=1):
                raise ValueError("There is {} Jurusan data".format(len(jurusan_data)))
            jurusan = jurusan_data[0]
            self.tingkat = int(tingkat)
            self.jurusan = jurusan
            
class JadwalGuru(models.Model):
    # class Meta:
    #     unique_together = (('nip', 'mapel', 'kelas', 'jurusan', 'mulai_belajar', 'berhenti_belajar'))
    nip = models.ForeignKey(InfoGuru, on_delete=models.SET_NULL, default=1, null=True)
    mapel = models.ForeignKey(Mapel, on_delete=models.SET_NULL, default=1, null=True)
    kelas = models.IntegerField(default=10)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, default=1)
    mulai_belajar = models.TimeField()
    berhenti_belajar = models.TimeField()
    def get_data(self):
        return [self.nip.nip, self.nip.nama ,self.mapel.nama, str(self.kelas), self.jurusan.nama_jurusan, str(self.mulai_belajar), str(self.berhenti_belajar)]

class NilaiUAS(models.Model):
    nis = models.ForeignKey(InfoSiswa, on_delete=models.CASCADE, default=1)
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE, default=1)
    nilai = models.IntegerField()#models.DecimalField(max_length=11, decimal_places=3, max_digits=5)
    #id_mapel = models.IntegerField(default=0)    
    def get_data(self):
        return [self.nis.nis, self.nis.nama, self.nis.tingkat_kelas, self.nis.jurusan.nama_singkatan_jurusan, self.mapel.nama, self.nilai]

class NilaiUTS(models.Model):
    nis = models.ForeignKey(InfoSiswa, on_delete=models.CASCADE, default=1)
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE, default=1)
    nilai = models.IntegerField()#models.DecimalField(max_length=11, decimal_places=3, max_digits=5)
    #id_mapel = models.IntegerField(default=0)    
    def get_data(self):
        return [self.nis.nis, self.nis.nama, self.nis.tingkat_kelas, self.nis.jurusan.nama_singkatan_jurusan, self.mapel.nama, self.nilai]


