import os
import uuid
# from ..Ecommerce.settings import EMAIL_HOST_USER
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
# import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Ecommerce.settings import EMAIL_HOST_USER

from .forms import *
from .models import*


# Create your views here.



def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')


def registration(request):
    if request.method=='POST':
        a= registrationform(request.POST)
        if a.is_valid():
            fn = a.cleaned_data["firstname"]
            ln = a.cleaned_data["lastname"]
            un = a.cleaned_data["username"]
            em = a.cleaned_data["email"]
            pas = a.cleaned_data["password"]
            cpas=a.cleaned_data["cpassword"]
            if pas==cpas:
                b = registrationmodel(firstname=fn, lastname=ln, username=un, email=em, password=pas)
                b.save()
                return redirect(login)
        else:
                return HttpResponse("registraion failed ")
    return render(request, 'registration.html')

def login(request):
    if request.method=='POST':
        a=loginform(request.POST)
        if a.is_valid():
            un=a.cleaned_data["username"]
            request.session['username'] = un
            pas=a.cleaned_data["password"]
            b=registrationmodel.objects.all()
            for i in b:
                request.session['usernme']=i.username
                if un==i.username and pas==i.password:
                    return redirect(f'/shop/{un}')
            else:

                return redirect(login)
    return render(request,'login.html')

def shop(request,username):

 return render(request,'shop.html',{'username':username})

def upload(request,username):

    if request.method=='POST':
        registrationmodel.objects.get(username=username)
        # request.session['username'] = username
        a=uploadform(request.POST,request.FILES)
        if a.is_valid():
            nm=a.cleaned_data["name"]
            pr=a.cleaned_data["price"]
            de=a.cleaned_data["description"]
            im=a.cleaned_data["image"]
            b=uploadmodel(name=nm,price=pr,description=de,image=im)
            b.save()
            return redirect(f'/shop/{username}')
        else:
            return HttpResponse("item adding failed")
    return render(request,'upload.html',{'username':username})

def uploaddisplay(request):


    y = request.session['username']

    x=uploadmodel.objects.all()
    li=[]
    nm=[]
    pr=[]
    de=[]
    id=[]
    for i in x:
        a=i.image
        li.append(str(a).split('/')[-1])
        b=i.name
        nm.append(b)
        c=i.price
        pr.append(c)
        d=i.description
        de.append(d)
        e=i.id
        id.append(e)
    mylist=zip(li,nm,pr,de,id)

    return render(request,'display.html',{'mylist':mylist,'username':y})


def uploaddelete(request,id):
    a=uploadmodel.objects.get(id=id)
    if len(a.image)>0:
        os.remove(a.image.path)
    a.delete()
    return redirect(uploaddisplay)

def uploadedit(request,id):
    a=uploadmodel.objects.get(id=id)
    im=str(a.image).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES)>0:
            if len(a.image)>0:
                os.remove(a.image.path)
            a.image=request.FILES['image']
        a.name=request.POST.get('name')
        a.price=request.POST.get('price')
        a.description=request.POST.get('description')
        a.save()
        return redirect(uploaddisplay)
    return render(request,'uploadedit.html',{'a':a,'im':im})

def profileedit(request,username):
    a=registrationmodel.objects.get(username=username)
    if request.method=='POST':
        a.firstname=request.POST.get('firstname')
        a.lastname=request.POST.get('lastname')
        a.username=request.POST.get('username')
        a.email=request.POST.get('email')
        a.password=request.POST.get('password')
        a.save()
        return redirect(f'/shop/{a.username}')
    return render(request,'profileedit.html',{'a':a,'username':username})

def userreg(request):
    if request.method=='POST':
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username= request.POST.get('username')
        email= request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')

        if User.objects.filter(username=username).first():
            messages.success(request,'username already taken')
            return redirect(userreg)

        if User.objects.filter(email=email).first():

            messages.success(request,'email already exist')
            return redirect(userreg)

        user_obj=User(first_name=first_name,last_name=last_name,username=username,email=email)
        if password==cpassword:
            user_obj.set_password(password)
            user_obj.save()
        auth_token=str(uuid.uuid4())
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_mail_regis(email,auth_token)
        return render(request,'sucess.html')
    return render(request,'userregistration.html')

def send_mail_regis(email,auth_token):
    subject="your account has been verified"
    message=f'paste the link verify your account http://127.0.0.1:8000/verify/{auth_token}'
    email_form=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_form,recipient)

def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(userlogin)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(userlogin)
    else:
        messages.success(request,"user.html not found")
        return redirect(userlogin)

def userlogin(request):
    if request.method=='POST':
        # email =request.POST.get('email')
        # request.session['email'] = email
        username = request.POST.get('username')
        request.session['user'] = username
        password=request.POST.get('password')

        a=User.objects.all()
        for i in a:
            if i.password==password and i.username==username:
                email=i.email
                request.session['email']=email


        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:   #if user.html doesn't exist
            messages.success(request,'User not found')
            return redirect(userlogin)

        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your mail')
            return redirect(userlogin)
        user=authenticate(username=username,password=password)


        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(userlogin)
        return redirect(f'/user/{username}')
    return render(request,'userlogin.html')

def user(request,username):
    x = uploadmodel.objects.all()
    li = []
    nm = []
    pr = []
    de = []
    id = []
    for i in x:
        a = i.image
        li.append(str(a).split('/')[-1])
        b = i.name
        nm.append(b)
        c = i.price
        pr.append(c)
        d = i.description
        de.append(d)
        e = i.id
        id.append(e)
    mylist = zip(li, nm, pr, de, id)
    return render(request, 'user.html',{'mylist':mylist,'username':username})

def cart(request,username,id):
    a=uploadmodel.objects.get(id=id)
    b=cartmodel(cartimage=a.image,cartname=a.name,cartprice=a.price,cartdescription=a.description)
    b.save()
    return render(request,'cartsuccess.html',{'username':username})

def cartdisplay(request,username):
    x=cartmodel.objects.all()
    image = []
    name = []
    price = []
    des = []
    id = []
    for i in x:
        a = i.cartimage
        image.append(str(a).split('/')[-1])
        b = i.cartname
        name.append(b)
        c = i.cartprice
        price.append(c)
        d = i.cartdescription
        des.append(d)
        e = i.id
        id.append(e)
    mylist = zip(image, name, price, des, id)

    return render(request,'cartdisplay.html',{'mylist':mylist,'username':username})

def cartdelete(request,username,id):
    a=cartmodel.objects.get(id=id)
    # if len(a.cartimage)>0:
    #     os.remove(a.cartimage.path)
    a.delete()
    return redirect(f'/cartdisplay/{username}')

def useredit(request,username):
    a=User.objects.get(username=username)
    if request.method=='POST':
        a.firstname=request.POST.get('firstname')
        a.lastname=request.POST.get('lastname')
        a.username=request.POST.get('username')
        a.email=request.POST.get('email')
        a.password=request.POST.get('password')
        a.save()
        return redirect(f'/user/{a.username}')
    return render(request,'useredit.html',{'a':a,'username':username})

def buy(request,username,id):
    a=cartmodel.objects.get(id=id)
    if request.method=='POST':
        cartname=request.POST.get("name")
        cartprice = request.POST.get("price")
        cartquantity = request.POST.get("quantity")
        total=int(cartprice)*int(cartquantity)
        request.session['total'] = total
        request.session['name'] = cartname
        request.session['price'] = cartprice
        em=request.session['email']
        send_mail(str() + "||" + "Final bill", "ordered success", EMAIL_HOST_USER, [em])
        return render(request,'bill.html',{'n':cartname,'p':cartprice,'q':cartquantity,'t':total,'username':username})

    return render(request,'buy.html',{'a':a,'username':username})



def email_send(request):
    a=Contactusform()
    user= request.session['user']
    b=request.session['total']
    c=request.session['name']

    d=request.session['email']
    if request.method=='POST':
        sub=Contactusform(request.POST)
        if sub.is_valid():
            nm=sub.cleaned_data['name']
            em=sub.cleaned_data['email']
            ms=sub.cleaned_data['message']
            send_mail(str(nm)+"||"+"Final bill",ms,EMAIL_HOST_USER,[em])
            return HttpResponse("email send successfully")
    return render(request, 'email.html', {'form': a, 'b': b, 'c': c, 'd': d,'username':user})










