#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

def verifycode(request,code):
    print('code : ' + code)
    return render(request, 'verifycode.html',{'result': True,'msg':'verify success!'})