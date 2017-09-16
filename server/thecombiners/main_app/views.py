import json
import random

from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'main_app/index.html')


def run_car(request):
    data = 'fail'
    if request.is_ajax() and request.method == 'POST':
        print(request.POST.items())
        data = 'done'
    mimeype = 'application/json'
    return HttpResponse(json.dumps(data), mimeype)


def get_car_status(request):
    data = 'fail'
    if request.is_ajax() and request.method == 'GET':
        x = random.randint(1, 500)
        y = random.randint(1, 500)
        quality = random.uniform(0, 1)
        data = {'x': x, 'y': y, 'quality': quality, }
    mimeype = 'application/json'
    return HttpResponse(json.dumps(data), mimeype)