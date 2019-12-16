from django.urls import path
from django.urls import include
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from . import views

app_name='SCOM_APP'
urlpatterns = [
    path('logout/', views.logout_view, name="logout"),
    path('/', lambda request: redirect('SCOM_APP:dataguru'), name='scom'),
    path('test/', lambda request: render(request, 'data.html')),

    path('datasiswa-edit/', views.siswa_edit, name='datasiswa-edit'),    
    path('datasiswa/', views.siswa_list, name='datasiswa'),
    path('newsiswa/', views.new_siswa, name="create-siswa"),

    path('dataguru-edit/', views.guru_edit, name='dataguru-edit'),
    path('dataguru/', views.guru_list, name='dataguru'),
    path('newguru/', views.new_guru, name="create-guru"),

    path('nilaiuas/', views.nilaiuas_list, name='datauas'),
    path('nilaiuas-edit/', views.nilaiuas_edit, name='uas-edit'),
    path('newnilaiuas/', views.new_nilaiuas, name='create-uas'),

    path('nilaiuts/', views.nilaiuts_list, name='datauts'),
    path('nilaiuts-edit/', views.nilaiuts_edit, name='uts-edit'),
    path('newnilaiuts/', views.new_nilaiuts, name='create-uts'),

    path('jadwal/', views.jadwal_list, name="datajadwal"),
    path('jadwal-edit/', views.jadwal_edit, name='datajadwal-edit'),
    path('newjadwal/', views.new_jadwal, name='create-jadwal'),    
    
]