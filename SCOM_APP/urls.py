from django.urls import path
from django.urls import include
from . import views
app_name='SCOM_APP'
urlpatterns = [
    path('datasiswa-edit/', views.siswa_edit, name='datasiswa-edit'),    
    path('datasiswa/', views.siswa_list, name='datasiswa'),
    path('newsiswa/', views.new_siswa, name="create-siswa"),

    path('dataguru-edit/', views.guru_edit, name='dataguru-edit'),    
    path('dataguru/', views.guru_list, name='dataguru'),
    path('newguru/', views.new_guru, name="create-guru")    
]