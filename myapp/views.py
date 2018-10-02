import datetime
from django.contrib.auth import hashers
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django import db
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import *



@csrf_exempt
def create_Buyer(request):
    if request.method != 'POST':
        return error_response(request, "Error: must be POST request")
    if 'name' not in request.POST or 'phone_number' not in request.POST or 'email' not in request.POST:
        return error_response(request, "Error: missing required fields")

    buyer_obj = Buyer(name=request.POST['name'],
                     phone_number=request.POST['phone_number'],
                     email=request.POST['email'])
    try:
        buyer_obj.save()
    except db.Error:
        return error_response(request, "Error: database error")
    return success_response(request, model_to_dict(buyer_obj))


@csrf_exempt
def read_Buyer(request, Buyer_id):
    if request.method != 'GET':
        return error_response(request, "Error: must be GET request")
    try:
        buyer_obj = Buyer.objects.get(pk=Buyer_id)
    except Buyer.DoesNotExist:
        return error_response(request, "Buyer not found")
    return success_response(request, model_to_dict(buyer_obj))

@csrf_exempt
def delete_Buyer(request, Buyer_id):
    if request.method != 'DELETE':
        return error_response(request, "Error: must DELETE request")
    try:
        buyer_obj = Buyer.objects.get(pk=Buyer_id)
    except Buyer.DoesNotExist:
        return error_response(request, "Buyer not found")
    buyer_obj.delete()
    return success_response(request)

@csrf_exempt
def update_Buyer(request, Buyer_id):
    if request.method != 'POST':
        return error_response(request, "400 Bad Request - must make HTTP POST request")
    try:
        buyer_obj = Buyer.objects.get(pk=Buyer_id)
    except Buyer.DoesNotExist:
        return error_response(request, "Buyer not found")

    changed = False
    if 'name' in request.POST:
        buyer_obj.name = request.POST['name']
        changed = True
    if 'phone_number' in request.POST:
        buyer_obj.phone_number = request.POST['phone_number']
        changed = True
    if 'email' in request.POST:
        buyer_obj.email = request.POST['email']
        changed = True
    if not changed:
        return error_response(request, "No fields updated")

        buyer_obj.save()
    return success_response(request, model_to_dict(buyer_obj))


def error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})


def success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})
