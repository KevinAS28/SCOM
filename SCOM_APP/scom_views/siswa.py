from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from SCOM_APP.models import *
from SCOM_APP.scom_form.SiswaForm import SiswaForm
from django.contrib import messages 
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required as django_login
from django.contrib.auth.decorators import REDIRECT_FIELD_NAME

def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="/login"):
    return django_login(function, redirect_field_name, login_url)


class SisAttr(str):
    
    data0 = ""
    def set_data(self, data):
        self.data0 = data
        return self


class SiswaObj(list):

    def __init__(self, data, id):
        super().__init__(data)
        self.id = id

    columns = ["nis", "nama", "kelas", "jurusan", "tgl_lah", "tmpt_lah", "alamat", "status", "jk"]
    
    def __getitem__(self, index):
        return SisAttr(super().__getitem__(index)).set_data(self.columns[index])

    def __iter__(self):
        toreturn = []
        for i in range(len(self)):
            dat = super().__getitem__(i)
            toreturn.append(SisAttr(dat).set_data(self.columns[i]))
        return iter(toreturn)
        
#@login_required
def siswa_edit(request):
    if (not "login" in request.session):
        return redirect('User:login')    
    if (not request.session["login"]):
        return redirect('User:login') 
    if (request.method=="POST"):
        form = SiswaForm(request.POST or None)
        print(form.errors)
        print(request.POST)
        if (form.is_valid()):
            print("valid")
            if ("action-edit" in request.POST):
                print("action-edit")
                #check existed nis
                if not (len(InfoSiswa.objects.filter(nis=form.cleaned_data["nis"]))):
                        messages.error(request, "NIS Not Exist")
                else:
                    if (request.POST["action-edit"]=="edit"):
                        print("edit")
                        info_siswa = InfoSiswa.objects.filter(nis=form.cleaned_data["nis"])[0]
                        for key in form.cleaned_data:
                            info_siswa.__dict__[key] = form.cleaned_data[key]
                        print(info_siswa.__dict__)
                        jurusan = Jurusan.objects.filter(nama_singkatan_jurusan=form.cleaned_data["jurusan"])[0]
                        info_siswa.jurusan = jurusan
                        info_siswa.status_aktif = True if form.cleaned_data["status_aktif"]=="Aktif" else False
                        info_siswa.save()
                        
                    else:
                        print("delete")
                        info_siswa = InfoSiswa.objects.filter(nis=form.cleaned_data["nis"])
                        info_siswa.delete()
        
    return redirect("SCOM_APP:datasiswa")
    
#@login_required
def siswa_list(request, template_name='siswa.html'):
    if (not "login" in request.session):
        return redirect('User:login')    
    if (not request.session["login"]):
        return redirect('User:login') 
    def default_page(data=InfoSiswa.objects.all()):        
        # fields = list(siswa[0].__dict__.values())[1:]
        # print(fields)
        columns = ["NIS", "Nama", "Kelas", "Jurusan", "Tanggal Lahir", "Tempat Lahir", "Alamat", "Status Aktif", "JK"]
        raw_columns = ["nis", "nama", "kelas", "jurusan", "tgl_lah", "tmpt_lah", "alamat", "status", "jk"]
        if (len(data)>0):
            contoh  = SiswaObj(data[0].get_data(), 0).__iter__()
            print(contoh)
        siswa_list = [SiswaObj(data[i].get_data(), i) for i in range(len(data))]
        majors = list(Jurusan.objects.all())
        data = {"columns": columns, "siswa":  siswa_list, "raw_col": raw_columns, "majors": majors}
        return render(request, template_name, data)

    get_data = request.GET
    if ("filter" in get_data.keys()):
        filter_columns = {"NIS": "nis", "Nama Siswa": "nama", "Tempat Lahir": "tempat_lahir", "Tanggal Lahir": "tanggal_lahir", "Alamat": "alamat", "Status Aktif": "status_aktif", "Jenis Kelamin": "jk", "Jurusan": "jurusan"}
        filter_column = "nis"
        filter_data = get_data["filter"]
        if ("Tidak ada filter" in get_data.keys()):
            return redirect("scom:datasiswa")
        if ("to-filter" in get_data.keys()):
            #if to-filter not exist then use the default one
            # print("get_data: ", get_data, "get_data['to-filter']: ", get_data["to-filter"])
            try:
                filter_column = filter_columns[get_data["to-filter"]]
            except KeyError:
                print("Siswa Filter Error: ", get_data["to-filter"])
                return default_page()
                              
                
            if (filter_columns[get_data["to-filter"]]=="jurusan"):
                #special handler if the user filter by Jurusan
                filter_data = Jurusan.objects.filter(nama_singkatan_jurusan=get_data["filter"])
                if (len(filter_data)==0):
                    return default_page()

        to_filter = {filter_column:filter_data}
        print(filter_column, filter_data)
        siswa = InfoSiswa.objects.filter(**to_filter)        

        return default_page(siswa)
        
    else:
        return default_page()



#@login_required
def new_siswa(request):
    if (not "login" in request.session):
        return redirect('User:login')    
    if (not request.session["login"]):
        return redirect('User:login') 
    if (request.method=="POST"):
        form = SiswaForm(request.POST or None)
        print(form.errors)
        print(request.POST)
        if (form.is_valid()):
            #check existed nis
            
            if (len(InfoSiswa.objects.filter(nis=form.cleaned_data["nis"]))):
                messages.error(request, "NIS Already Exist")
                print("NIS EXIST")
            else:
                print("valid")
                info_siswa = InfoSiswa()
                for key in form.cleaned_data:
                    info_siswa.__dict__[key] = form.cleaned_data[key]
                info_siswa.save()
        else:
            return redirect("SCOM_APP:datasiswa")

        print(form.errors)
    return redirect("SCOM_APP:datasiswa")
