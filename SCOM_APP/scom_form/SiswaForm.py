from django import forms
from SCOM_APP.models import InfoSiswa

class SiswaForm(forms.Form):
    nis = forms.IntegerField()
    nama = forms.CharField(max_length=100)
    #kelas = forms.ChoiceField(choices=(("10", "10"), ("11", "11"), ("12", "12")))
    jurusan = forms.ChoiceField(choices=(("RPL", "RPL"), ("TP", "TP")))
    tanggal_lahir = forms.DateField()
    tempat_lahir = forms.CharField(max_length=100)
    alamat = forms.CharField(max_length=100)
    status_aktif = forms.ChoiceField(choices=(("1", "Aktif"), ("0", "Tidak Aktif")))
    jk = forms.ChoiceField(choices=(("1", "Laki-laki"), ("0", "Perempuan")))
    