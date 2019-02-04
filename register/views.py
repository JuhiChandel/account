from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from register.models import Register, User_ver


def start(request):
    return HttpResponse("<h1>Welcome</h1>")


def home(request):
    return HttpResponse("<h1>Welcome</h1>")


@csrf_exempt
def register_form(request):
    if request.method == 'GET':
        return render_to_response('register/register_form.html', {'message': "success"})
    elif request.method == 'POST':
        user = request.POST['name']
        print(user)
        email = request.POST['email']
        print(email)
        password = request.POST['pass']
        print(password)
        confirm_password = request.POST['con']
        print(confirm_password)
        otp = random.randint(1000, 9999)
        print(otp)
        reg = Register.objects.filter(email=email).exists()
        if reg:
            print("Error: E-mail Id already exist")
            return render_to_response('register/register_form.html', {'message': "success"})
        else:
            p = Register.objects.create(user=user, email=email, password=password, confirm_password=confirm_password)
            request.session['email'] = email
            otp_instance = User_ver.objects.create(user=p, otp=otp, is_verified=False)
            otp_instance1 = User_ver.objects.get(otp=otp)
            otp_instance2 = otp_instance1.otp
            print(otp_instance2)
            send_mail("Your one time password", otp_instance2, 'nentertainmentbahar@gmail.com', [email], fail_silently=False)
            return redirect('/register/register/otp_ver/')

@csrf_exempt
def otp_ver(request):
    if request.method == 'GET':
        return render_to_response('register/otp_ver.html', {'message': "success"})
    elif request.method == 'POST':
        otp = request.POST['otp']
        print(otp)
        is_verified = True
        user_verify = User_ver.objects.filter(otp=otp).update(is_verified=is_verified)
        if user_verify:
            return redirect('/register/register/login/')


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render_to_response('register/login.html', {'message': "success"})
    elif request.method == 'POST':
        email = request.POST['email']
        print(email)
        password = request.POST['pass']
        print(password)
        register_instance1 = Register.objects.get(email=email)
        user_verified = User_ver.objects.get(user=register_instance1)
        if user_verified.is_verified == True:
            print("User is verified")
            register_instance = Register.objects.get(email=email)
            print(register_instance.password)
            print(register_instance.email)
            password1 = register_instance.password
            if password1 == password:
                return redirect('/register/register/home/')
            else:
                print("Invalid login Email Id and password")
                return render_to_response('register/login.html', {'message': "success"})
        else:
            print("User is not verified")
            return render_to_response('register/login.html', {'message': "success"})

@csrf_exempt
def forget_password(request):
    if request.method == 'GET':
        return render_to_response('register/forget_password.html', {'message': "success"})
    elif request.method == 'POST':
        email = request.POST['email']
        print(email)
        user_instance = Register.objects.filter(email=email).exists()
        print(user_instance)
        try:
            if user_instance:
                otp = random.randint(1000, 9999)
                print(otp)
                send_mail("Your one time password", str(otp), 'nentertainmentbahar@gmail.com', [email], fail_silently=False)
                return redirect('/register/register/reset_password/')
        except AttributeError as e:
            print(e)
            return redirect('/register/register/reset_password/')


@csrf_exempt
def reset_password(request):
    if request.method == 'GET':
        return render_to_response('register/reset_password.html', {'message': "success"})
    elif request.method == 'POST':
        if request.session.has_key('email'):
            email = request.session['email']
            print(email)
            otp = request.POST['otp']
            print(otp)
            password = request.POST['pass']
            print(password)
            confirm_password = request.POST['con']
            print(confirm_password)
            reset_password = Register.objects.filter(email=email).update(password=password, confirm_password=confirm_password)
            return redirect('/register/register/login/')
