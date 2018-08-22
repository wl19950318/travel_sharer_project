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
import jwt # PyJWT==0.4.1
import requests # requests==2.5.0
import json
import time
import re

URL_TMP = 'http://127.0.0.1:8000/verifycode/'

def index(request):
    notes = []
    if Note.objects.count() > 3:
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
        if email == '' or re.match(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z_.]{0,19}ac.uk',email) == None:
            return render(request, 'web/register.html',{'error':'Email error'})
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
        user.lanague = 0
        user.save()
    return render(request, 'web/register.html',{'error':'go mailbox verify code'})

def verifycode(request,code):
    users = UserInfo.objects.filter(code=code,verify=0)
    if not users:
        return render(request, 'web/register.html',{'error':'verify error'})
    users.update(verify=1)
    return redirect('/login/')

def loginout(request):
    request.session.flush()
    return redirect('/')

@user_decorator.login
def myPics(request):
    user = UserInfo.objects.get(id=request.session['userId'])
    tbictures = TBicture.objects.filter(userId=user).order_by("-createTime")
    return render(request, 'web/myPics.html',{'tbictures':tbictures})

@user_decorator.login
def myArticle(request):
    user = UserInfo.objects.get(id=request.session['userId'])
    notes = Note.objects.filter(userId=user).order_by("-createTime")
    return render(request, 'web/myArticle.html',{'notes':notes})


def travelNote(request):
    notes = Note.objects.all().order_by("-createTime")
    return render(request, 'web/travelNote.html',{'notes':notes})

def pics(request):
    tbictures = TBicture.objects.all().order_by("-createTime")
    return render(request, 'web/pics.html',{'tbictures':tbictures})

def sort_user(request, sort):
    users = []
    if sort == '0':
        users = UserInfo.objects.all().order_by("-createTime")
    else:
        users = UserInfo.objects.all().order_by("createTime")
    return render(request, 'web/myMembers.html',{'users':users})

def filter_user(request, label):
    users = UserInfo.objects.filter(label=label).order_by("-createTime")
    return render(request, 'web/myMembers.html',{'users':users})

def discover(request):
    tbictures = TBicture.objects.order_by("-createTime").all()
    return render(request, 'web/discover.html',{'tbictures':tbictures})

def travelType(request, type):
    notes = Note.objects.filter(type=type).order_by("-createTime")
    return render(request, 'web/travelNote.html',{'notes':notes})

def located(request):
    sample = random.sample(xrange(TBicture.objects.count()),1)
    randomPic = [TBicture.objects.all()[i] for i in sample]
    tbictures = TBicture.objects.filter(address=randomPic[0].address).order_by("-createTime")
    return render(request, 'web/pics.html',{'tbictures':tbictures})

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
        users = UserInfo.objects.all()
        #noteComments = NoteComment.objects.filter(noteId__userId = user).order_by("-createTime")
        return render(request, 'web/myMembers.html',{'users':users})


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
def delPic(request, id):
    TBicture.objects.get(id=id).delete()
    return redirect('/myPics')

@user_decorator.login
def delArticle(request, id):
    Note.objects.get(id=id).delete()
    return redirect('/myArticle')


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
def userinfo(request):
    user = UserInfo.objects.get(id=request.session['userId'])
    if request.method == 'POST':
        user.lanague = request.POST['lanague']
        user.firstname = request.POST['firstname']
        user.lastname = request.POST['lastname']
        user.phone = request.POST['phone']
        user.label = request.POST['label']
        user.save()
    return render(request, 'web/userinfo.html',{'user':user})


def user_pic(request):
    file = request.FILES['file']
    user = UserInfo.objects.get(id=request.session['userId'])
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)
    user.pic = uploaded_file_url
    user.save()
    return redirect('/userinfo')

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
def comment(request, commentId):
    noteComment = NoteComment.objects.get(id=commentId)
    noteComment.author_replyTime = time.time()
    noteComment.author_reply = request.POST['author_reply']
    noteComment.save()
    return redirect('/detailPage/'+str(noteComment.noteId.id))

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

def location(request,lat,long):
    result_dict = {}
    result_dict['r'] = False
    result = requests.get('http://maps.google.com/maps/api/geocode/json?latlng='+str(lat)+','+ str(long) +'&sensor=false&key=')
    if result.status_code == 200:
        result_json = result.json()
        if result_json.get('status') == 'OK':
            address = result_json.get('results')
            for addr in address:
                for type in addr.get('types'):
                    if type == 'administrative_area_level_1':
                        result_dict['r'] = True
                        result_dict['address'] = addr.get('formatted_address')
                        break
                if result_dict.get('address'):
                    break
    return HttpResponse(json.dumps(result_dict), content_type='application/json')

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

def oauth2callbackgoogle(request):
    # Get the code after a successful signing
    # Note: this does not cover the case when authentication fails
    CODE = request.GET['code']

    CLIENT_ID = '137249259650-q2vgft7r8hg4phhugiaj1gqco7iuqll8.apps.googleusercontent.com' # Edit this
    CLIENT_SECRET = 'RKzEPW0ek8HPGGKoCoZ3harg' # Edit this
    REDIRECT_URL = 'http://localhost:8000/oauth2callbackgoogle' # Edit this

    if CODE is not None:
        payload = {
            'grant_type': 'authorization_code',
            'code': CODE,
            'redirect_uri': REDIRECT_URL,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
            }

        token_details_request = requests.post('https://accounts.google.com/o/oauth2/token', data=payload)
        if token_details_request.status_code != 200:
            return render(request, 'web/login.html',{'error':'google login error'})
        token_details = token_details_request.json()
        id_token = token_details['id_token']
        access_token = token_details['access_token']

        # Retrieve the unique identifier for the social media account
        decoded = jwt.decode(id_token, verify=False)
        oauth_identifier = decoded['sub']

        # Retrieve  account details
        account_details_request = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + access_token)
        if account_details_request.status_code != 200:
            return render(request, 'web/login.html',{'error':'google oauth info error'})
        account_details = account_details_request.json()
        email = account_details['email']
        user = UserInfo.objects.filter(email=email)
        id = 0
        if not user:
            user = UserInfo()
            user.email = email
            user.pwd = email
            user.code = '0000'
            user.verify = 1
            user.lanague = 0
            user.save()
            id = user.id
        else:
            id = user[0].id

        red = HttpResponseRedirect("/")
        request.session['userId'] = id
        request.session['email'] = email
        return red














