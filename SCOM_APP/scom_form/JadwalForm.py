from django import forms
from SCOM_APP.models import InfoSiswa

class JadwalForm(forms.Form):
    nip = forms.IntegerField()
    mapel = forms.CharField(max_length=100)    
    kelas = forms.CharField(max_length=100)    
    jurusan = forms.CharField(max_length=100)
    mulai_belajar = forms.TimeField()
    berhenti_belajar = forms.TimeField()