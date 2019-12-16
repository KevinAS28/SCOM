from django.urls import path
from django.urls import include
from django.shortcuts import render, redirect
from . import views
app_name='User'
urlpatterns = [
    path('login/', lambda request: redirect('User:username'), name='login'),
    path('login/nip/', views.nip, name="username"),
    path('login/password/', views.password, name="password"),
]