"""UserAccess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('index/', views.index, name='index'),
    path('',views.loginPage,name ='login'),
    path('register/',views.registerPage,name='register'),
    path('aboutus/',views.aboutus,name ='aboutus'),
    path('diabetesprediction/',views.diabetesprediction, name='diabetesprediction'),
    path('familyhistory/',views.familyhistory, name='familyhitory'),
    path('labresult/', views.labresult, name='labresult'),
    path('malariadetection/', views.malariadetection, name='malariadetection'),
    path('preexistingcondition/', views.preexistingcondition, name='preexistingcondition'),
    path('retinascan/', views.retinascan, name = 'retinascan'),
    path('specchrecognition/', views.specchrecognition, name='specchrecognition'),
    path('videoassessment/', views.videoassessment, name='videoassessment'),
    path('medication', views.medication, name='medication'),
    path('diabetes_pre/', views.diabetes_pre,name='diabetesprediction'),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('handl/', views.hnd_load, name='handl'),






]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
