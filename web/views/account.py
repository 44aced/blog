from django.shortcuts import render,HttpResponse,redirect
from utils.check_code import create_validate_code
from utils.JsonCustomEncoder import JsonCustomEncoder
from io import BytesIO
from web.forms.forms import RegisterForm,LoginForm
from repository import models
import json

# Create your views here.

def check_code(request):

    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream,'PNG')
    request.session['checkcode'] = code
    return HttpResponse(stream.getvalue())

def register(request):
    result = {'status':False,'errors':None,'data':None}
    if request.method == 'GET':
        return render(request,'register.html')

    elif request.method == 'POST':
        obj = RegisterForm(request,request.POST)
        if obj.is_valid():
            user = obj.cleaned_data.get('username')
            pwd = obj.cleaned_data.get('password')
            e = obj.cleaned_data.get('email')
            models.UserInfo.objects.create(username=user,password=pwd,email=e)
            user_info = models.UserInfo.objects.filter(username=user,password=pwd).values(
                        'nid','nickname','username','email','avatar','blog__nid','blog__site').first()
            if user_info:
                result['status'] = True
                request.session['user_info'] = user_info
                request.session.set_expiry(7 * 24 * 60 * 60)
            return HttpResponse(json.dumps(result))
        else:
            print(obj.errors)
            result['errors'] = obj.errors.as_data()
            return HttpResponse(json.dumps(result,cls=JsonCustomEncoder))

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')

    if request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        obj = LoginForm(request,request.POST)
        if obj.is_valid():
            u = obj.cleaned_data.get('username')
            p = obj.cleaned_data.get('password')
            print('user',u)
            print('pwd',p)
            user_info = models.UserInfo.objects.filter(username=u,password=p).values(
                        'nid','nickname','username','email','avatar','blog__nid','blog__site').first()
            if user_info:
                result['status'] = True
                request.session['user_info'] = user_info
                if obj.cleaned_data.get('rmb'):
                    request.session.set_expiry(7*24*60*60)
            print(user_info)
        else:
            print(obj.errors)
            if 'username' in obj.errors:
                result['errors'] = '用户名不存在'
            else:
                result['errors'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))

def logout(request):
    request.session.clear()
    return redirect('/')






