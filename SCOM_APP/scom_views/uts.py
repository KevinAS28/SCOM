from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from SCOM_APP.models import *
from SCOM_APP.scom_form.NutsForm import NutsForm
from django.contrib import messages 
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required as django_login
from django.contrib.auth.decorators import REDIRECT_FIELD_NAME

def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="/login"):
    return django_login(function, redirect_field_name, login_url)


class NutsAttr(str):
    data0 = ""
    def set_data(self, data):
        self.data0 = data
        return self

class NutsObj(list):

    def __init__(self, data, id):
        super().__init__(data)
        self.id = id

    columns = ["nis", "nama", "kelas", "jurusan", "mapel", "nilai"]
    
    def __getitem__(self, index):
        return NutsAttr(super().__getitem__(index)).set_data(self.columns[index])

    def __iter__(self):
        toreturn = []
        for i in range(len(self.columns)):
            dat = super().__getitem__(i)
            toreturn.append(NutsAttr(dat).set_data(self.columns[i]))
        return iter(toreturn)
        

#@login_required
def nilaiuts_edit(request):
    if (not "login" in request.session):
        return redirect('User:login')    
    if (not request.session["login"]):
        return redirect('User:login') 
    if (request.method=="POST"):
        form = NutsForm(request.POST or None)
        valid = form.is_valid()
        print(form.cleaned_data)
        print(request.POST)
        if (valid):
            print("valid")
            if ("action-edit" in request.POST):
                print("action-edit")
                #check existed nis
                mapel = Mapel.objects.filter(nama=form.cleaned_data["mapel"])
                siswa = InfoSiswa.objects.filter(nis=form.cleaned_data["nis"])
                if ((len(mapel)!=0) and (len(siswa)!=0)):
                    data = NilaiUTS.objects.filter(pk=request.POST["toedit"])
                    if (len(data)==0):
                            messages.error(request, "Data not exist")
                    else:
                        info_nilaiuts = data[0]
                        if (request.POST["action-edit"]=="edit"):
                            print("edit")
                            mapel = mapel[0]
                            siswa = siswa[0]
                            info_nilaiuts.mapel = mapel
                            info_nilaiuts.nilai = int(form.cleaned_data["nilai"])
                            info_nilaiuts.save()
                            
                        else:
                            print("delete")
                            info_nilaiuts.delete()
                            

    return redirect("SCOM_APP:datauts")

#@login_required
def nilaiuts_list(request, template_name='uts.html'):
    if (not "login" in request.session):
        return redirect('User:login')    
    if (not request.session["login"]):
        return redirect('User:login') 
    def default_page(data=NilaiUTS.objects.all()):        
        #print("data: ", data)
        # fields = list(nilaiuts[0].__dict__.values())[1:]
        # print(fields)
        columns = ["NIS", "Nama", "Kelas", "Jurusan", "Mapel", "Nilai"]
        raw_columns = ["nis", "nilai"]
        
        if (len((data))>0):
            contoh  = NutsObj(data[0].get_data(), 0).__iter__()
            print(contoh)
        nilaiuts_list = [NutsObj(data[i].get_data(), data[i].id) for i in range(len(data))]
        data = {"columns": columns, "nilaiuts":  nilaiuts_list, "raw_col": raw_columns, "mapel": [i.nama for i in Mapel.objects.all()]}
        return render(request, template_name, data)

    get_data = request.GET

    if ("filter" in get_data.keys()):
        filter_columns = {"NIS": "nis", "Nama Siswa": "nama", "Jurusan": "jurusan", "Mapel": "mapel", "Nilai": "nilai"}
        filter_column = "nis"
        filter_data = get_data["filter"]
        if ("Tidak ada filter" in get_data.keys()):
            return redirect("SCOM_APP:datauts")
        if ("to-filter" in get_data.keys()):
            #if to-filter not exist then use the default one
            # print("get_data: ", get_data, "get_data['to-filter']: ", get_data["to-filter"])
            try:
                filter_column = filter_columns[get_data["to-filter"]]
            except KeyError:
                print("Nuts Filter Error: ", get_data["to-filter"])
                return default_page()

            if (filter_columns[get_data["to-filter"]]=="nis"):
                #special handler if the user filter by Jurusan
                siswa = InfoSiswa.objects.filter(nis=get_data["filter"])[0]
                filter_data = NilaiUTS.objects.filter(nis=siswa)
                return default_page(filter_data)


            if (filter_columns[get_data["to-filter"]]=="jurusan"):
                #special handler if the user filter by Jurusan
                jurusan = Jurusan.objects.filter(nama_singkatan_jurusan=get_data["filter"])[0]
                filter_data = []
                for i in NilaiUTS.objects.all():
                    if (i.nis.jurusan==jurusan):
                        filter_data.append(i)
                return default_page(filter_data)

            if (filter_columns[get_data["to-filter"]]=="mapel"):
                #special handler if the user filter by Jurusan
                mapel = Mapel.objects.filter(nama=get_data["filter"])[0]
                filter_data = NilaiUTS.objects.filter(mapel=mapel)
                return default_page(filter_data)


        to_filter = {filter_column:filter_data}
        #print(filter_column, filter_data)
        
        nilaiuts = NilaiUTS.objects.filter(**to_filter)        
        
        return default_page(nilaiuts)
        
    else:
        return default_page()

#@login_required
def new_nilaiuts(request):
    if (not "login" in request.session):
        return redirect('User:login')    
    if (not request.session["login"]):
        return redirect('User:login') 
    if (request.method=="POST"):
        form = NutsForm(request.POST or None)
        print(request.POST)
        if (form.is_valid()):
            print("valid")
            print(form.cleaned_data)
            #check existed nis
            
            siswa = InfoSiswa.objects.filter(nis=form.cleaned_data["nis"])
            if (len(siswa)):
                siswa = siswa[0]
                if not (len(list(NilaiUTS.objects.filter(nis=siswa)))):
                    messages.error(request, "NIS Not Exist")
                else:
                    info_nilaiuts = NilaiUTS()
                    for key in form.cleaned_data:
                        info_nilaiuts.__dict__[key] = form.cleaned_data[key]
                    info_nilaiuts.nis = siswa
                    info_nilaiuts.mapel = Mapel.objects.filter(nama=form.cleaned_data["mapel"])[0]
                    info_nilaiuts.save()
            else:
                print("NIS NOT EXIST!!")
        else:
            print(form.errors)
            print("NOT VALID")
            return redirect("SCOM_APP:datauts")
    return redirect("SCOM_APP:datauts")
