from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

# Create your views here.
def testview(request):
    return render(request, 'test.html')