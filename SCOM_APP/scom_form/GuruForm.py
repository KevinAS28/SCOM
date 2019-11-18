from django import forms
from SCOM_APP.models import InfoSiswa

class GuruForm(forms.Form):
    nip = forms.IntegerField()
    nama = forms.CharField(max_length=100)
    #kelas = forms.ChoiceField(choices=(("10", "10"), ("11", "11"), ("12", "12")))
    nuptk = forms.CharField(max_length=15)
    tanggal_lahir = forms.DateField()
    tempat_lahir = forms.CharField(max_length=100)
    alamat = forms.CharField(max_length=100)
    status_aktif = forms.ChoiceField(choices=(("1", "Aktif"), ("0", "Tidak Aktif")))
    
    