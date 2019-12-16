from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth import login
from User.backends.AuthenticationBackend import AuthenticationBackend
from django.contrib import messages 
# Create your views here.

def nip(request):
    if (request.method=="GET"):
        return render(request, "nip.html")
    elif (request.method=="POST"):
        try:
            request.session["nip"] = request.POST["username"]
            print(request.session["nip"])
        except Exception as error:
            print("error")
            return HttpResponseBadRequest(error)
        return redirect('User:password')
    else:
        return HttpResponseBadRequest("IDK")

def password(request):
    if (request.method=="GET"):
        return render(request, "password.html")
    elif (request.method=="POST"):
        #return HttpResponse(request.session["nip"] + " " + request.POST["password"])
        username = request.session["nip"]
        password = request.POST["password"]
        user = AuthenticationBackend().authenticate(request=request, username=username, password = password) 
        if user is not None: 
            
            form = login(request, user, backend='User.backends.AuthenticationBackend.AuthenticationBackend') 
            request.session["login"] = True
            print(request.session.__dict__)
            print("Success Login")      
            print(request.user.is_authenticated)
            return redirect('SCOM_APP:dataguru')
        else:
            messages.success(request, f' Password Incorrect!') 
            print("failed login")
            return render(request, "password.html")
    else:
        return HttpResponseBadRequest()    
    