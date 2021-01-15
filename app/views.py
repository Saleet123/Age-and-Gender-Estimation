import os
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from AGE_GENDER_PREDICTION.settings import BASE_DIR,STATICFILES_DIRS
from .model.demo import main
import time
import requests

@csrf_exempt
def work(request):
    timestamp1 = time.time()  #Start Time
    img = request.FILES['img'] # getting input image
    picname = request.FILES['img'].name # getting filename
    path = "input" #path to save the uploaded image to directory
    filename=os.path.join(STATICFILES_DIRS[0], path, picname) #joined path with filename
    fs = FileSystemStorage()  #filestorage system to save the image
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        os.remove(filename) # delete the frile if the same file already exist
    fs.save(filename, img) #saving the file
    age,gender=main(filename,picname) #calling main script for age and gebnder estimation
    timestamp2 = time.time() #ending time
    total=timestamp2-timestamp1 #time difference
    #creating a dictionary to return
    data = {}
    data['age'] = age
    data['gender'] = gender
    data['response_time']=total
    response = HttpResponse(json.dumps(data))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["cache - control"] = "no - cache"
    response["Access-Control-Allow-Headers"] = "*"
    return response

@csrf_exempt
def imgurl(request):
    imagegurl=request.POST['url']
    timestamp1 = time.time()
    name=imagegurl.split("/")
    name=name[-1]
    path = "input"  # path to save the uploaded image to directory
    filename = os.path.join(STATICFILES_DIRS[0], path, name)  # joined path with filename
    response=requests.get(imagegurl)
    file=open(filename,'wb')
    file.write(response.content)
    file.close()
    age, gender = main(filename, name)  # calling main script for age and gebnder estimation
    timestamp2 = time.time()  # ending time
    total = timestamp2 - timestamp1  # time difference
    # creating a dictionary to return
    data = {}
    data['age'] = age
    data['gender'] = gender
    data['response_time'] = total
    response = HttpResponse(json.dumps(data))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["cache - control"] = "no - cache"
    response["Access-Control-Allow-Headers"] = "*"
    return response