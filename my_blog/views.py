from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>This is home</h1>")

def about(request):
    return HttpResponse("<h1>This is about</h1>")
