from django.core.mail import send_mail
from django.contrib import auth
import random
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from register.models import Register, User_ver, Student

def start(request):
    return HttpResponse("<h1>Welcome</h1>")

@csrf_exempt
def create_student(request):
    response = {}
    if request.method == 'GET':
        return render_to_response('register/create_student.html')
    elif request.method == 'POST':
        enroll = request.POST['enroll']
        print(enroll)
        name = request.POST['name']
        print(name)
        class1 = request.POST['class1']
        print(class1)
        stream = request.POST['stream']
        print(stream)
        father = request.POST['father']
        print(father)
        dob = request.POST['dob']
        print(dob)
        add = request.POST['add']
        print(add)
        enroll1 = Student.objects.filter(enroll=enroll).exists()
        if enroll1:
            print("already exist")
            context = {
                'message': 'Enrollment number already exist'

            }
            return render_to_response('register/create_student.html', context)
        else:
            p = Student.objects.create(enroll=enroll, name=name, class1=class1, stream=stream, father=father, dob=dob, add=add)
            return render_to_response('register/create_student.html')

@csrf_exempt
def logout(request):
    try:
        del request.session['email']
    except KeyError:
        pass
    return redirect('/register/register/register_form/')

@csrf_exempt
def home(request):
    if request.method == 'GET':
        data = Student.objects.all().order_by('-enroll')
        context = {'data': data}
        return render_to_response('register/home.html', context)


@csrf_exempt
def register_form(request):
    response = {}
    if request.method == 'GET':
        return render_to_response('register/register_form.html')
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
            #response = JsonResponse("E-mail Id already exist", safe=False)
            #response['success'] = False
            #response['message'] = "E-mail Id already exist"
            # return JsonResponse(response)<span>{{message}}</span>
            context = {
                'message': 'E-mail Id already exist'

            }
            return render_to_response('register/register_form.html', context)
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
        return render_to_response('register/otp_ver.html')
    elif request.method == 'POST':
        otp = request.POST['otp']
        print(otp)
        is_verified = True
        user_verify = User_ver.objects.filter(otp=otp).update(is_verified=is_verified)
        if user_verify:
            context = {
                'message': 'Successfully OTP verified'

            }
            return redirect('/register/register/login/', context)
        else:
            context = {
                'message': 'Invalid OTP'

            }
            return render_to_response('register/otp_ver.html', context)


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render_to_response('register/login.html')
    elif request.method == 'POST':
        email = request.POST['email']
        print(email)
        password = request.POST['pass']
        print(password)
        register_instance1 = Register.objects.get(email=email)
        user_verified = User_ver.objects.get(user=register_instance1)
        request.session['email'] = email
        if user_verified.is_verified == True:
            print("User is verified")
            #register_instance = Register.objects.get(email=email)
            print(register_instance1.password)
            print(register_instance1.email)
            password1 = register_instance1.password
            if password1 == password:
                return redirect('/register/register/home/')
            else:
                context = {
                    'message': 'Invalid password'

                }
                return render_to_response('register/login.html', context)
        else:
            context = {
                'message': 'User is not verified'

            }
            return render_to_response('register/login.html', context)

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
        return render_to_response('register/reset_password.html')
    elif request.method == 'POST':
        email = request.session['email']
        print(email)
        if email:
            otp = request.POST['otp']
            print(otp)
            password = request.POST['pass']
            print(password)
            confirm_password = request.POST['con']
            print(confirm_password)
            if otp != "" and password == confirm_password:
                reset_password = Register.objects.filter(email=email).update(password=password, confirm_password=confirm_password)
                return redirect('/register/register/login/')
            else:
                return render_to_response('register/reset_password.html')