from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Availability, Facility, Hospital, State, City,Image
from django.views import generic
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse

from keras.applications.vgg16 import preprocess_input

from tensorflow.keras.preprocessing import image
import json
from django.core.files.storage import FileSystemStorage
import datetime
from .models import *
from .tfmodel import *
from django.core.files.storage import FileSystemStorage

import numpy as np
import random

model=model_loader()
disease={0: 'COVID +VE', 1: 'COVID -VE'}

class HospitalDetailView(generic.DetailView):
    model = Hospital


def Home(request):
    context={'a':1}
    return render(request,'app/Homepage.html',context)

def service(request):
    return render(request,'app/')
def predictImage(request):
    if request.method =="GET":

        return render(request, 'Predict.html')
    else :
        fileObj=request.FILES.get('filePath')
        path=Image.objects.create(file=fileObj)
        path.save()

        img = image.load_img(path.file.path,target_size=(224, 224))
        x = image.img_to_array(img)
        x = x / 255
        x = np.expand_dims(x, axis=0)
        #img_data = preprocess_input(x)
        #print(model.predict(x))
        a = np.argmax(model.predict(x), axis=1)
        #print({'prediction':disease[a[0]]})
        return render(request,'Predict.html',context={'Disease':disease[a[0]],'url':"http://127.0.0.1:8000"+path.file.url})

def home(request):
    selected_state_id = request.GET.get('state')
    selected_city_id = request.GET.get('city')
    selected_facility_id = request.GET.get('facility')
    facilities = Facility.objects.all().order_by('pk')
    if selected_state_id:
        cities = City.objects.filter(state=selected_state_id)
    else:
        cities = City.objects.all()

    states = State.objects.all()
    hospitals = Hospital.objects.all()

    if selected_city_id:
        hospitals = hospitals.filter(city=City(pk=selected_city_id))

    if selected_facility_id:
        availities = Availability.objects.all()
        if selected_city_id:
            availities = availities.filter(
                hospital__city=City(pk=selected_city_id))

        availities = availities.filter(
            facility=Facility(pk=selected_facility_id), available__gt=0)

        hospitals = []
        for avl in availities:
            hospitals.append(avl.hospital)

        print("Hosipitals", hospitals)

    context = {
        'facilities': facilities,
        'cities': cities,
        'states': states,
        'hospitals': hospitals,
        'selected_state_id': selected_state_id,
        'selected_city_id': selected_city_id,
        'selected_facility_id': selected_facility_id,

    }
    return render(request, template_name='app/index.html', context=context)
