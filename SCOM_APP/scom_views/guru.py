from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from SCOM_APP.models import *
from SCOM_APP.scom_form.GuruForm import GuruForm
from django.contrib import messages 
from django.db.utils import IntegrityError

class GurAttr(str):    
    data0 = ""
    def set_data(self, data):
        self.data0 = data
        return self

class GuruObj(list):

    def __init__(self, data, id):
        super().__init__(data)
        self.id = id

    columns = ["nip", "nama", "nuptk", "tgl_lah", "tmpt_lah", "alamat", "status"]
    
    def __getitem__(self, index):
        return GurAttr(super().__getitem__(index)).set_data(self.columns[index])

    def __iter__(self):
        toreturn = []
        for i in range(len(self)):
            dat = super().__getitem__(i)
            toreturn.append(GurAttr(dat).set_data(self.columns[i]))
        return iter(toreturn)

def guru_edit(request):
    if (request.method=="POST"):
        form = GuruForm(request.POST or None)
        if (form.is_valid()):
            print("valid")
            if ("action-edit" in request.POST):
                print("action-edit")
                #check existed nip
                if not (len(InfoGuru.objects.filter(nip=form.cleaned_data["nip"]))):
                        messages.error(request, "NIP Not Exist")

                else:
                    
                    if (request.POST["action-edit"]=="edit"):
                        print("edit")
                        info_guru = InfoGuru.objects.filter(nip=form.cleaned_data["nip"])[0]
                        for key in form.cleaned_data:
                            info_guru.__dict__[key] = form.cleaned_data[key]
                        info_guru.save()
                        
                    else:
                        print("delete")
                        info_guru = InfoGuru.objects.filter(nip=form.cleaned_data["nip"])
                        info_guru.delete()
        
    return redirect("SCOM_APP:dataguru")

def guru_list(request, template_name='guru.html'):
    def default_page(data=InfoGuru.objects.all()):        
        # fields = list(guru[0].__dict__.values())[1:]
        # print(fields)
        columns = ["NIP", "Nama", "NUPTK",  "Tanggal Lahir", "Tempat Lahir", "Alamat", "Status Aktif"]
        raw_columns = ["nip", "nama", "nuptk", "tgl_lah", "tmpt_lah", "alamat", "status"]
        if (len(data)>0):
            contoh  = GuruObj(data[0].get_data(), 0).__iter__()
            print(contoh)
        guru_list = [GuruObj(data[i].get_data(), i) for i in range(len(data))]
        data = {"columns": columns, "guru":  guru_list, "raw_col": raw_columns}
        return render(request, template_name, data)

    get_data = request.GET
    if ("filter" in get_data.keys()):
        filter_columns = {"NIP": "nip", "Nama Guru": "nama", "NUPTK": "nuptk", "Tempat Lahir": "tempat_lahir", "Tanggal Lahir": "tanggal_lahir", "Alamat": "alamat", "Status Aktif": "status_aktif"}
        filter_column = "nip"
        filter_data = get_data["filter"]
        if ("Tidak ada filter" in get_data.keys()):
            return redirect("scom:dataguru")
        if ("to-filter" in get_data.keys()):
            #if to-filter not exist then use the default one
            # print("get_data: ", get_data, "get_data['to-filter']: ", get_data["to-filter"])
            try:
                filter_column = filter_columns[get_data["to-filter"]]
            except KeyError:
                print("Guru Filter Error: ", get_data["to-filter"])
                return default_page()

        to_filter = {filter_column:filter_data}
        print(filter_column, filter_data)
        guru = InfoGuru.objects.filter(**to_filter)        

        return default_page(guru)
        
    else:
        return default_page()

def new_guru(request):
    if (request.method=="POST"):
        form = GuruForm(request.POST or None)
        
        if (form.is_valid()):
            #check existed nip
            if (len(InfoGuru.objects.filter(nip=form.cleaned_data["nip"]))):
                print("NIP EXIST")
                messages.error(request, "NIP Already Exist")
            else:
                print("valid")
                info_guru = InfoGuru()
                for key in form.cleaned_data:
                    info_guru.__dict__[key] = form.cleaned_data[key]
                info_guru.save()
        else:
            return HttpResponse(messages.error(form.errors))
            
    return redirect("SCOM_APP:dataguru")
