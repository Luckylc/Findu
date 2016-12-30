# coding=utf-8
from django.http import HttpResponse

def Hello(request):
    return HttpResponse("111")
