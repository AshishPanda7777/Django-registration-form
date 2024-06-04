from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from app.models import *
from  app.forms import *
from django.core.mail import send_mail 
from django.urls import reverse

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def registration(request):
    EUFO=Userform()
    EPFO=Profileform()
    d={'EUFO':EUFO,'EPFO':EPFO}
    
    if request.method=='POST' and request.FILES:
        NMUFDO=Userform(request.POST)
        NMPFDO=Profileform(request.POST,request.FILES)
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            MUFDO=NMUFDO.save(commit=False)
            pw=NMUFDO.cleaned_data['password'] 
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO=NMPFDO.save(commit=False)  
            MPFDO.username=MUFDO
            MPFDO.save()
            send_mail('Regsitration',
                        'thank u for regsitration',
                        'pandaashish910@gmail.com',
                        [MUFDO.email],
                        fail_silently=False,)
            return  HttpResponse('Data inserted succesfully')
        else:
            return  HttpResponse('Invalid data')    
        
    return render (request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')



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
            return HttpResponse('Invalid Credentials')







    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))