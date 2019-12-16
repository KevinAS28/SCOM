
from SCOM_APP.scom_views.siswa import *
from SCOM_APP.scom_views.guru import *
from SCOM_APP.scom_views.uas import *
from SCOM_APP.scom_views.uts import *
from SCOM_APP.scom_views.jadwal import *
# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    #logout(request)
    request.session["login"] = False
    return redirect("User:login")



    
    
