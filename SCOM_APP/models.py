from django.db import models


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
    
class Mapel(models.Model):
    nama = models.CharField(max_length = 25)
    kkm = models.IntegerField(default=0)

class MapelGuru(models.Model):
    nip = models.IntegerField(default=0)    
    #id_mapel = models.IntegerField(default=0)
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE, default=1)

class JadwalGuru(models.Model):
    #id_mapel_guru = models.IntegerField(default=0)
    #id_kelas = models.IntegerField(default=0)
    mapel_guru = models.ForeignKey(MapelGuru, on_delete=models.CASCADE, default=1)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, default=1)
    mulai_belajar = models.TimeField()
    berhenti_belajar = models.TimeField()



class NilaiUAS(models.Model):
    nis = models.ForeignKey(InfoSiswa, on_delete=models.CASCADE, default=1)
    nilai = models.DecimalField(max_length=11, decimal_places=3, max_digits=5)
    #id_mapel = models.IntegerField(default=0)
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE, default=1)
    def get_data(self):
        return [nis.nis, nis.nama, nis.tingkat_kelas, nis.tingkat_kelas, nis.jurusan.nama_singkatan_jurusan, self.mapel.nama, self.nilai]


class NilaiUTS(NilaiUAS):
    nis = models.ForeignKey(InfoSiswa, on_delete=models.CASCADE, default=1)
    nilai = models.DecimalField(max_length=11, decimal_places=3, max_digits=5)
    #id_mapel = models.IntegerField(default=0)
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE, default=1)


