from idlelib.autocomplete import FILES
from sys import stdout
import tkinter as tk
from django.contrib.auth import authenticate
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
import mysql.connector
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import pickle
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
import  MySQLdb
import os
from .models import SharedImage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CreateUserForm
# Create your views here.

@login_required(login_url='login')
def index(request):
    template= loader.get_template('index.html')
    return HttpResponse(template.render())

def loginPage(request):

    if request.user.is_authenticated:
        return render(request,'index.html')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return render(request,'index.html')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


@csrf_exempt
def registerPage(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return render(request,'login.html')

        context = {'form': form}
        return render(request, 'register.html', context)



def aboutus(request):
    template = loader.get_template('aboutus.html')
    return  HttpResponse(template.render())

@csrf_exempt
def familyhistory(request):
    template = loader.get_template('familyhistory.html')
    return HttpResponse(template.render())
@csrf_exempt
def labresult(request):
    template = loader.get_template('labresult.html')
    return HttpResponse(template.render())

@csrf_exempt
def malariadetection(request):
   # template = loader.get_template('malariadetection.html')



    if request.method == 'POST' and request.FILES.get('malariaimg', False):
        model_malaria = load_model('malaria_detector.h5')

        malariaimg = request.FILES['malariaimg']
        fs = FileSystemStorage()
        filename = fs.save(malariaimg.name, malariaimg)
        uploaded_file_url = fs.url(filename)

        #test_image1 = image.load_img(malariaimg, target_size=(64, 64))
        test_image = image.img_to_array(malariaimg)
        test_image = np.expand_dims(test_image, axis=0)
        result = model_malaria.predict(test_image)
        if result[0][0] >= 0.5:
            prediction = 'Not infected'
        else:
            prediction = 'Infected **'
        return render(request, 'malariadetection.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'malariadetection.html')



@csrf_exempt
def hnd_load(request):
    shr = SharedImage()
    shr.image = request.FILES['file']
    shr.title = request.POST['title']
    shr.description = request.POST['description']
    shr.save()
    return redirect('malariadetection')


'''
    template = loader.get_template('malariadetection.html')
    context = {}
    class_malaria = {'Infected': 0,
                  'Uninfected' : 1 }

    class_names = list(class_malaria.keys())
    model_malaria = load_model('malaria_detector.h5')
    graph = tf.compat.v1.get_default_graph()


    if request.method == 'POST':
        uploaded_file = request.FILES['myfile']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        name = image.load_img(uploaded_file)
        name = image.img_to_array(name)
        name = np.expand_dims(name, axis=0)
        name = name / 255
        with graph.as_default():
            preds = model_malaria.predict(name)
        preds = preds.flatten()
        m = max(preds)
        for index, item in enumerate(preds):
            if item == m:
                malaria_result = class_names[index]

        return render(request, "malariadetection.html", {
        'malaria_result': malaria_result})
    else:
        return render(request, "malariadetection.html")

    return HttpResponse(template.render({'malaria_result ':malaria_result }))

'''
def preexistingcondition(request):
    template = loader.get_template('preexistingcondition.html')
    return HttpResponse(template.render())

def retinascan(request):
    template = loader.get_template('retinascan.html')
    return HttpResponse(template.render())

def specchrecognition(request):
    template = loader.get_template('specchrecognition.html')
    return HttpResponse(template.render())

def videoassessment(request):
    template = loader.get_template('videoassessment.html')
    return HttpResponse(template.render())

def medication(request):
    template = loader.get_template('medication.html')
    return  HttpResponse(template.render())

def symptoms(request):
    template = loader.get_template('smytoms.html')
    return  HttpResponse(template.render())










@csrf_exempt
def diabetesprediction(request):
    template = loader.get_template('diabetesprediction.html')
    return HttpResponse(template.render())

@csrf_exempt
def diabetes_pre(request):
    template = loader.get_template('diabetesprediction.html')
    pregnancies = request.POST.get("Pregnancies")
    glucose = request.POST.get("Glucose")
    bloodpressure = request.POST.get("BloodPressure")
    skinthickness = request.POST.get("SkinThickness")
    insulin = request.POST.get("Insulin")
    BMI = request.POST.get("BMI")
    DiabetesPedigreeFunction = request.POST.get("DiabetesPedigreeFunction")
    age = request.POST.get("Age")

    diabetes_data = [
        [pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age]]
    diabetes_model = pickle.load(open('diabetes_model.pickle', 'rb'))
    # diabetes_model = pd.read_pickle('r',"diabetes_model.pickle")
    prediction = diabetes_model.predict(
        [[pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age]])
    outcome = prediction
    '''
    mydb = mysql.connector.connect(host='172.31.39.232', user="d3evil4", passwd="Devil@54645", db="kareai")
    mycursor = mydb.cursor()
    mycursor = mydb.cursor()
    res = 'INSERT INTO diabetes (Pregnancies, Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome) VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}");'.format(
        pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age, outcome)
    mycursor.execute(res)
    mydb.commit()
    '''

    result1 = "Infected"
    reslut2 = "Uninfected"
    if outcome == 1:
        result = "Infected"
    elif outcome == 0:
        result = "Uninfected"


    return HttpResponse(template.render({'result':result}))

    #return render('diabetesprediction.html',prediction)

'''
   if outcome == 1:
        return print("Innfected")
    elif outcome == 0:
        return  print("Uninnfected")
'''

'''
class MalariaImage(TemplateView):
    form = Malaria
    template_name = 'malariadetection.html'

    def post(self, request, *args, **kwargs):
        form = Malaria(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('index'))
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


    class EmpImageDisplay(DetailView):
    model = Malaria
     template_name = ('malariadetection.html')
'''