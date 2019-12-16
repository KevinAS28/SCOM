from django import forms

class NuasForm(forms.Form):
    nis = forms.CharField(max_length = 20)
    nilai = forms.IntegerField()#forms.DecimalField(decimal_places=3, max_digits=6)
    mapel = forms.CharField(max_length = 25)
    
    