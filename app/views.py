from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from app.forms import *
# Create your views here.

def home(request):
    if request.session.get('username'):
        d={'username':request.session.get('username')}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registration(request):
    d={'EUFO':UserForm(),'EPFO':ProfileForm()}
    if request.POST and request.FILES:
        nmufdo=UserForm(request.POST)
        nmpfdo=ProfileForm(request.POST,request.FILES)
        if nmufdo.is_valid() and nmpfdo.is_valid():
            mufdo=nmufdo.save(commit=False)
            pw=nmufdo.cleaned_data['password']
            mufdo.set_password(pw)
            mufdo.save()

            mpfdo=nmpfdo.save(commit=False)
            mpfdo.username=mufdo
            mpfdo.save()

            send_mail('registration','u have registered sucessfully','kv966653@gmail.com',[mufdo.email],fail_silently=False)
            
            return HttpResponse('data is entered into database')
        else:
            return HttpResponse('try to enter valid data')
    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid data')
    return render(request,'login.html')
@login_required
def user_logout(request):
    if request.session.get('username'):
        logout(request)
    return HttpResponseRedirect(reverse('home'))