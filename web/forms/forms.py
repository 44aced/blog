from django import forms
from django.forms import fields
from django.forms import widgets
from repository import models
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):

    def __init__(self,request,*args,**kwargs ):
        self.request = request
        super(RegisterForm, self).__init__(*args,**kwargs)

    username = fields.CharField(min_length=5,max_length=20,error_messages={'required':'用户名不能为空'})
    password = fields.CharField(error_messages={'required':'密码不能为空'},min_length=6,max_length=20)
    confirm_password = fields.CharField(error_messages={'required':'密码不能为空'},min_length=6,max_length=20)
    email = fields.EmailField(error_messages={'required':'邮箱不能为空','invalid':'邮箱格式不正确'})
    check_code = fields.CharField(error_messages={'required': '验证码不能为空.'})

    def clean_username(self):
        user = models.UserInfo.objects.filter(username=self.cleaned_data['username']).count()
        if not user:
            return self.cleaned_data['username']
        else:
            raise ValidationError(message='用户名已经存在',code='请重新输入用户名')

    def clean_email(self):
        email = models.UserInfo.objects.filter(email=self.cleaned_data['email']).count()
        if not email:
            return self.cleaned_data['email']
        else:
            raise ValidationError(message='邮箱已存在',code='请重新输入邮箱')

    def clean_check_code(self):
        # print(self.request.session.get('checkcode'))
        # print(self.request.POST.get('check_code'))
        if self.request.session.get('checkcode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误',code='请重新输入验证码')

    def clean(self):
        if self.request.POST.get('password') != self.request.POST.get('confirm_password'):
            raise ValidationError(message='两次输入的密码不一致')

class LoginForm(forms.Form):
    def __init__(self,request,*args,**kwargs ):
        self.request = request
        super(LoginForm, self).__init__(*args,**kwargs)

    username = fields.CharField(error_messages={'required':'用户名不能为空'})
    password = fields.CharField(error_messages={'required':'密码不能为空'})
    check_code = fields.CharField(error_messages={'required': '验证码不能为空.'})
    rmb = fields.IntegerField(required=False)

    def clean_username(self):
        u = models.UserInfo.objects.filter(username=self.request.POST.get('username')).count()
        if not u:
            raise ValidationError(message='用户名不存在')
        else:
            return self.cleaned_data['username']

    def clean_check_code(self):
        if self.request.session.get('checkcode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误',code='请重新输入验证码')

    # def clean(self):
    #     v = models.UserInfo.objects.filter(username=self.request.POST.get('username'),password=
    #         self.request.POST.get('password')).count()
    #     if not v:
    #         raise ValidationError(message='用户名或密码错误')
    #     else:
    #         return self.cleaned_data






