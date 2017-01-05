#coding=utf-8
import datetime
from django.contrib.auth.models import User
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

#表单
class UserForm(forms.Form): 
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.CharField(label='邮箱')


#注册
@csrf_exempt
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            #添加到数据库
            user = User.objects.create_user(username=username,password=password)
            user.email = email
            user.is_superuser = 0
            user.is_staff = 0
            user.is_active = 1
            user.date_joined = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
            user.save()
            request.session['loginUser'] = username
            serverMsg="user registered successed"
            flag='True'
            return HttpResponseRedirect('../login')
    else:
        uf = UserForm()
    return render_to_response('online/regist.html',{'uf':uf}, context_instance=RequestContext(request))

#登陆
@csrf_exempt
def login(request):
    if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')
            print username
            #获取的表单数据与数据库进行比较
            user_pass = authenticate(username=username, password=password)
            print "user"
            print user_pass
            if user_pass:
                #比较成功，跳转index
                response = HttpResponseRedirect('/online/index/')
                #将username写入浏览器cookie,失效时间为3600
                request.session['username'] = username
                return response
            else:
                #比较失败，还在login
                return HttpResponse("比较失败，还在login")
                # return HttpResponseRedirect('/online/login/')
    else:
        uf = UserForm()
    return render(request,'online/login.html',{'uf':uf})

#判断是否登录
@csrf_exempt
def is_login(request):
    username = request.session.get('username',False)
    if username:
        loginUsers=User.objects.filter(username=username)
        if loginUsers.count()>0:
            loginUser=loginUsers[0]
        else:
            print("error!loginUser's count is [%d]" % (loginUsers.count()))
            loginUser=User()
    else:
        loginUser=User()
    return (username,loginUser)
#登陆成功
@csrf_exempt
def index(request):
    username = request.COOKIES.get('username','')
    return render(request,'online/index.html' ,{'username':username})

#退出
@csrf_exempt
def logout(request):
    response = HttpResponse('logout !!')
    #清理cookie里保存username
    response.delete_cookie('username')
    return render(request,'online/login.html')