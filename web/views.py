#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from web.models import UserInfo, Note,NoteComment,TBicture,NoteCollection
import random
import sendemail
from PIL import Image
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from travelsharer import settings
from . import user_decorator


URL_TMP = 'http://127.0.0.1:8000/verifycode/'

def index(request):
    sample = random.sample(xrange(Note.objects.count()),3)
    notes = [Note.objects.all()[i] for i in sample]
    return render(request, 'web/index.html', {'notes':notes})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = UserInfo.objects.filter(email=email)
        if len(user)==0:
            return render(request, 'web/login.html',{'error':'account or password error'})
        if user[0].pwd != password:
            return render(request, 'web/login.html',{'error':'account or password error'})
        elif user[0].verify == 1:
            return render(request, 'web/login.html',{'error':'email not verify'})
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

def loginout(request):
    request.session.flush()
    return redirect('/')

def travelNote(request):
    notes = Note.objects.all().order_by("-createTime")
    return render(request, 'web/travelNote.html',{'notes':notes})

def pics(request):
    tbictures = TBicture.objects.all().order_by("-createTime")
    return render(request, 'web/pics.html',{'tbictures':tbictures})

def discover(request):
    tbictures = TBicture.objects.order_by("-createTime").all()
    return render(request, 'web/discover.html',{'tbictures':tbictures})

def travelType(request, type):
    notes = Note.objects.filter(type=type).order_by("-createTime")
    return render(request, 'web/travelNote.html',{'notes':notes})

def picType(request, type):
    tbictures = TBicture.objects.filter(type=type).order_by("-createTime")
    return render(request, 'web/pics.html',{'tbictures':tbictures})

def discoverType(request, type):
    tbictures = TBicture.objects.filter(discover_type=type).order_by("-createTime")
    return render(request, 'web/discover.html',{'tbictures':tbictures})

def about(request):
    return render(request, 'web/about.html')

@user_decorator.login
def members(request):
    if not request.session['userId']:
        return render(request, 'web/members.html')
    else:
        user = UserInfo.objects.get(id=request.session['userId'])
        noteComments = NoteComment.objects.filter(noteId__userId = user).order_by("-createTime")
        return render(request, 'web/myMembers.html',{'noteComments':noteComments})
@user_decorator.login
def collection(request):
    user = UserInfo.objects.get(id=request.session['userId'])
    noteCollections = NoteCollection.objects.filter(userId = user).order_by("-createTime")
    return render(request, 'web/collection.html',{'noteCollections':noteCollections})

@user_decorator.login
def delcollection(request, id):
    NoteCollection.objects.get(id=id).delete()
    return redirect('/collection')

@user_decorator.login
def delTraveNoteComment(request, id):
    NoteComment.objects.get(id=id).delete()
    return redirect('/members')

@user_decorator.login
def post_artcle(request):
    error = ''
    if request.method == 'POST' and request.FILES['file']:
        title = request.POST['title']
        user = UserInfo.objects.get(id=request.session['userId'])
        author = request.POST['author']
        type = request.POST['type']
        content = request.POST['content']
        content = content.replace('"../static', '"/static')
        remark = request.POST['remark']
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        note = Note()
        note.title = title
        note.userId = user
        note.author = author
        note.type = type
        note.remark = remark
        note.content = content
        note.picUrl = uploaded_file_url
        note.views = 0
        note.likes = 0
        note.save()
        return redirect('/travelNote')
    return render(request, 'web/post_artcle.html')

@user_decorator.login
def post_pic(request):
    error = ''
    if request.method == 'POST' and request.FILES['file']:
        if request.POST['title']:
            error = 'title null'
        title = request.POST['title']
        address = request.POST['address']
        user = UserInfo.objects.get(id=request.session['userId'])
        type = request.POST['type']
        remark = request.POST['remark']
        file = request.FILES['file']
        discover_type = request.POST['discover_type']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)

        pic = TBicture()
        pic.title = title
        pic.userId = user
        pic.address = address
        pic.type = type
        pic.discover_type = discover_type
        pic.remark = remark
        pic.picUrl = uploaded_file_url
        pic.save()
        return redirect('/pics')
    return render(request, 'web/post_pic.html')

def detailPage(request, id):
    note = Note.objects.get(id=id)
    note.views = note.views + 1
    note.save()
    noteComments = NoteComment.objects.filter(noteId=note).order_by("-createTime")
    notes = Note.objects.order_by("createTime").all()[0:3]
    return render(request, 'web/detailPage.html',{'note' : note, 'noteComments': noteComments, 'notes':notes})

@user_decorator.login
def travelLike(request, id):
    note = Note.objects.get(id=id)
    note.likes = note.likes + 1
    note.save()
    return redirect('/detailPage/'+id)

@user_decorator.login
def traveComment(request,id):
    note = Note.objects.get(id=id)
    user = UserInfo.objects.get(id=request.session['userId'])
    notComment = NoteComment()
    notComment.userId = user
    notComment.noteId = note
    notComment.comment = request.POST['comment']
    notComment.save()
    return redirect('/detailPage/'+id)

@user_decorator.login
def noteCollection(request,id):
    note = Note.objects.get(id=id)
    user = UserInfo.objects.get(id=request.session['userId'])
    count = NoteCollection.objects.filter(noteId = note, userId = user).count()
    if count == 0:
        noteCollection = NoteCollection()
        noteCollection.noteId = note
        noteCollection.userId = user
        noteCollection.save()
    return redirect('/travelNote')


def test(request):
    return  render(request, 'web/test.html')

@csrf_exempt
def upload(request):
    try:
        file = request.FILES['image']
        img = Image.open(file)
        img.thumbnail((500, 500), Image.ANTIALIAS)
        img.save(settings.MEDIA_ROOT + file.name, img.format)
    except Exception,e:
        return HttpResponse('error %s' % e)
    print(settings.MEDIA_ROOT)
    path = settings.MEDIA_URL +file.name
    return HttpResponse("<script>top.$('.mce-btn.mce-open').parent().find('.mce-textbox').val('%s').closest('.mce-window').find('.mce-primary').click();</script>" % path)

















