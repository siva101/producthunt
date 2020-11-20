from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

def login(request):
    if request.method=='POST':
        user=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html',{'error': 'username or password is incorrect'})

    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('home')

def signup(request):
    if request.method=='POST':
            if request.POST['password1'] and request.POST['password2'] and request.POST['username']:
                if request.POST['password1']==request.POST['password2']:
                    try:
                        user=User.objects.get(username=request.POST['username'])
                        return render(request,'accounts/signup.html',{'error':'username is already taken'})
                    except User.DoesNotExist:
                        user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                        auth.login(request,user)
                        return redirect('home')
                else:
                    return render(request, 'accounts/signup.html', {'error': 'passwords not matching'})
            else:
                return render(request, 'accounts/signup.html', {'error': 'please fill username, password , confirm password'})
    else:
        return render(request, 'accounts/signup.html')






