from ast import literal_eval
import json
import random

from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.staticfiles.templatetags.staticfiles import static
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from main_app.contamination_detection import *
import random


def index(request):
    return render(request, 'main_app/index.html')


def run_car(request):
    data = 'fail'
    if request.is_ajax() and request.method == 'POST':
        request.session['coordinates'] = literal_eval(request.POST['coordinates'])
        request.session['current_location'] = (None, None, None)
        data = 'done'
    mimeype = 'application/json'
    return HttpResponse(json.dumps(data), mimeype)


def get_car_status(request):
    data = 'fail'
    size = 40
    if request.is_ajax() and request.method == 'GET':
        coordinates = request.session['coordinates']
        max_y = max(coordinates, key=lambda item: item['y'])['y']
        min_y = min(coordinates, key=lambda item: item['y'])['y']
        polygon = Polygon([(dct['x'], dct['y']) for dct in coordinates])
        x, y, dir = request.session['current_location']
        if x is None:
            min_x_point = min(coordinates, key=lambda item: item['x'])
            x, y = (min_x_point['x'], min_x_point['y'])
            if polygon.intersects(Point(x, y + size)):
                dir = 'up'
            elif polygon.intersects(Point(x, y - size)):
                dir = 'down'
            else:
                dir = None
        elif not polygon.intersects(Point(x, y)) and (not dir or not polygon.intersects(Point(x, y + (size if dir == 'up' else -size)))):
            data = 'done'
        else:
            if dir is None:
                x += size
                if polygon.intersects(Point(x, y + size)):
                    dir = 'up'
                elif polygon.intersects(Point(x, y - size)):
                    dir = 'down'
                else:
                    dir = None
            elif dir == 'up' and polygon.intersects(Point(x, y + size)):
                y += size
            elif dir == 'down' and polygon.intersects(Point(x, y - size)):
                y -= size
            else:
                x += size
                brk = False
                if dir == 'down':
                    while y < max_y:
                        if polygon.intersects(Point(x, y)):
                            brk = True
                            break
                        y += size
                    dir = 'up'
                elif dir == 'up':
                    while y > min_y:
                        if polygon.intersects(Point(x, y)):
                            brk = True
                            break
                        y -= size
                    dir = 'down'
                if not brk:
                    data = 'done'
        request.session['current_location'] = (x, y, dir)
        if not data == 'done':
            origin = '/home/natalija/Documents/HackZurich/server/thecombiners/main_app/static/main_app/img/'
            image_list = ['contamination1.jpg', 'contamination3.jpg', 'no_contamination1.jpg','no_contamination2.jpg','no_contamination3.jpg']
            image_path = image_list[random.randint(0,4)]
            
            quality = (contamination(origin + image_path))/100
            grains = predict_grains(origin + image_path).split('\n')

            data = {'x': x, 'y': y, 'quality': quality, 'img_url': static('main_app/img/' + image_path), 'data': [('quality', quality), ('grains', grains)]}
    mimeype = 'application/json'
    return HttpResponse(json.dumps(data), mimeype)
