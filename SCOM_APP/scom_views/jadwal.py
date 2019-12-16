from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from SCOM_APP.models import *
from SCOM_APP.scom_form.JadwalForm import JadwalForm
from django.contrib import messages 
from django.db.utils import IntegrityError
import datetime

class JadAttr(str):
    
    data0 = ""
    def set_data(self, data):
        self.data0 = data
        return self


class JadwalObj(list):

    def __init__(self, data, id):
        super().__init__(data)
        self.id = id
        
    columns = ["nip", "nama", "mapel", "kelas", 'jurusan', "mulai_belajar", "berhenti_belajar"]
    
    def __getitem__(self, index):
        return JadAttr(super().__getitem__(index)).set_data(self.columns[index])

    def __iter__(self):
        toreturn = []
        for i in range(len(self)):
            dat = super().__getitem__(i)
            toreturn.append(JadAttr(dat).set_data(self.columns[i]))
        return iter(toreturn)
        
def jadwal_edit(request):
    if (request.method=="POST"):
        form = JadwalForm(request.POST or None)
        print(request.POST)
        if (form.is_valid()):
            print("valid")
            print(form.cleaned_data)
            if ("action-edit" in request.POST):
                print("action-edit")
                
                #check existed nis
                data = JadwalGuru.objects.filter(pk=request.POST["toedit"])
                if not (len(data)):
                        messages.error(request, "Data Not Exist")
                else:
                    if (request.POST["action-edit"]=="edit"):
                        print("edit")
                        #data = data[0]
                        data.update(
                            nip = InfoGuru.objects.filter(nip=form.cleaned_data["nip"])[0],
                            mapel = Mapel.objects.filter(nama=form.cleaned_data["mapel"])[0],
                            kelas = int(form.cleaned_data["kelas"]),
                            jurusan = Jurusan.objects.filter(nama_singkatan_jurusan=form.cleaned_data["jurusan"])[0],
                            mulai_belajar = form.cleaned_data["mulai_belajar"],
                            berhenti_belajar = form.cleaned_data["berhenti_belajar"]
                            )
                        # data.nip = InfoGuru.objects.filter(nip=form.cleaned_data["nip"])[0]
                        # data.mapel = Mapel.objects.filter(nama=form.cleaned_data["mapel"])[0]
                        # data.kelas = int(form.cleaned_data["kelas"])
                        # data.jurusan = Jurusan.objects.filter(nama_singkatan_jurusan=form.cleaned_data["jurusan"])[0]
                        # data.mulai_belajar = form.cleaned_data["mulai_belajar"]
                        # data.berhenti_belajar = form.cleaned_data["berhenti_belajar"]
                        # data.save() 
                        
                        
                    else:
                        print("delete")
                        data = data[0]
                        print(data.__dict__)
                        data.delete()
                        
        else:
            print("edit form not valid")
            print(form.errors)
    return redirect("SCOM_APP:datajadwal")
    

def default_page(request, data=JadwalGuru.objects.all()):        
    # fields = list(jadwal[0].__dict__.values())[1:]
    # print(fields)
    data=JadwalGuru.objects.all()
    template_name='jadwal.html'
    columns = ["NIP", "Nama", "Mapel", "Kelas", "Jurusan", "Mulai Belajar", "Berhenti Belajar"]
    raw_columns = ["nip", "nama", "mapel", "kelas", "mulai_belajar", "berhenti_belajar"]
    if (len(data)>0):
        contoh  = JadwalObj(data[0].get_data(), 0).__iter__()
        print(contoh)
    jadwal_list = [JadwalObj(i.get_data(), i.id) for i in data]
    
    guru = [[guru.nip, guru.nama] for guru in InfoGuru.objects.all()]
    mapel = Mapel.objects.all()
    jurusan = Jurusan.objects.all()
    [print(i.__dict__) for i in data]
    print('\n\n')
    data = {"columns": columns, "jadwal":  jadwal_list, "raw_col": raw_columns, "teachers": guru, "mapels": mapel, "majors": jurusan}
    
    print(jadwal_list, "\n\n")
    print(data["jadwal"])
    return render(request, template_name, data)

def jadwal_list(request):
    get_data = request.GET
    if ("filter" in get_data.keys()):
        filter_columns = {"NIP": "nip", "Nama":"nama", "Mapel": "mapel", "Kelas": "kelas", "Jurusan":"jurusan", "Mulai Belajar": "mulai_belajar", "Berhenti Belajar": "berhenti_belajar"}
        filter_column = "nip"
        filter_data = get_data["filter"]
        if ("Tidak ada filter" in get_data.keys()):
            return redirect("scom:datajadwal")
        if ("to-filter" in get_data.keys()):
            #if to-filter not exist then use the default one
            # print("get_data: ", get_data, "get_data['to-filter']: ", get_data["to-filter"])
            try:
                filter_column = filter_columns[get_data["to-filter"]]
            except KeyError:
                print("Jadwal Filter Error: ", get_data["to-filter"])
                return default_page()
                                              
            if (filter_columns[get_data["to-filter"]]=="nip"):
                #special handler if the user filter by Jurusan
                filter_data = InfoGuru.objects.get(nip=get_data["filter"])
                if (len(filter_data)==0):
                    return default_page()

            if (filter_columns[get_data["to-filter"]]=="mapel"):
                #special handler if the user filter by Jurusan
                filter_data = Mapel.objects.get(nama=get_data["filter"])
                if (len(filter_data)==0):
                    return default_page()

            if (filter_columns[get_data["to-filter"]]=="jurusan"):
                #special handler if the user filter by Jurusan
                filter_data = Jurusan.objects.get(nama_singkatan_jurusan=get_data["filter"])
                if (len(filter_data)==0):
                    return default_page()

        to_filter = {filter_column:filter_data}
        print(filter_column, filter_data)
        
        jadwal = JadwalGuru.objects.filter(**to_filter)

        return default_page(jadwal)
        
    else:
        return default_page(request)

def new_jadwal(request):
    if (request.method=="POST"):
        form = JadwalForm(request.POST or None)
        print(request.POST)
        msg = ""
        if (form.is_valid()):
            print("valid")
            print(form.cleaned_data)
            
            mulai = form.cleaned_data["mulai_belajar"]
            stop = form.cleaned_data["berhenti_belajar"]
            kelas = int(form.cleaned_data["kelas"])
            #nip = InfoGuru.objects.filter(nip=form.cleaned_data["nip"])[0]
            mapel = Mapel.objects.filter(nama=form.cleaned_data["mapel"])[0]
            jurusan = Jurusan.objects.filter(nama_singkatan_jurusan=form.cleaned_data["jurusan"])[0]
            check0 = JadwalGuru.objects.filter(mulai_belajar__range=(form.cleaned_data["mulai_belajar"], form.cleaned_data["berhenti_belajar"]), kelas=kelas, jurusan=jurusan) 
            if (len(check0)):
                msg += "Data already exist with:"
                for i in check0:
                    msg+="\n{}\n".format(str(i.get_data()))
                #messages.error(request, msg)
                messages.error(request, msg.replace("\n", "\\n"))
                print(msg)
            else:
                print("valid")
                data = JadwalGuru()
                data.nip = InfoGuru.objects.filter(nip=form.cleaned_data["nip"])[0]
                data.mapel = Mapel.objects.filter(nama=form.cleaned_data["mapel"])[0]
                data.kelas = int(form.cleaned_data["kelas"])
                data.jurusan = Jurusan.objects.filter(nama_singkatan_jurusan=form.cleaned_data["jurusan"])[0]
                data.mulai_belajar = form.cleaned_data["mulai_belajar"]
                data.berhenti_belajar = form.cleaned_data["berhenti_belajar"]
                data.save() 
                return redirect("SCOM_APP:datajadwal")
        
    print(form.errors)
    return redirect("SCOM_APP:datajadwal")
    
