#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from web.models import UserInfo
import random
import sendemail

URL_TMP = 'http://127.0.0.1:8000/verifycode/'

def index(request):
    return render(request, 'web/index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = UserInfo.objects.filter(email=email)
        if len(user)==0:
            return render(request, 'web/login.html',{'error':'account or password error'})
        if user[0].pwd != password:
            return render(request, 'web/login.html',{'error':'account or password error'})
        else:
            red = HttpResponseRedirect("/")
            request.session['userId'] = user[0].id
            request.session['email'] = user[0].email
            return red
    return render(request, 'web/login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if password != repassword:
            return render(request, 'web/register.html',{'error':'Two passwords do not match'})
        count = UserInfo.objects.filter(email=email).count()
        if count != 0:
            return render(request, 'web/register.html',{'error':'Username already exists'})
        code = random.randint(1000,99999)
        ret = sendemail.mail(email,URL_TMP + str(code))
        if not ret:
            return render(request, 'web/register.html',{'error':'Send email error!'})
        user = UserInfo()
        user.email = email
        user.pwd = password
        user.code = code
        user.verify = 0
        user.save()
    return render(request, 'web/register.html')

def verifycode(request,code):
    users = UserInfo.objects.filter(code=code,verify=0)
    if not users:
        return render(request, 'web/register.html',{'error':'verify error'})
    users.update(verify=1)
    return redirect('/login/')