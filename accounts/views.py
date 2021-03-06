from django.db import reset_queries
from django.shortcuts import render ,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username already exist')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'email already exist')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                    user.save()
                    messages.success(request,'account created')
                    return redirect('login')
        else:
            messages.error(request,'password do not match')
            return redirect('register')
    else:
        return render(request,'accounts/register.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'login succesfull')
            return redirect('dashboard')
        else:
            messages.error(request,'invalid username and password')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def dashboard(request):
    contact_list = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts' : contact_list
    }
    return render(request,'accounts/dashboard.html',context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'logout')
        return redirect('index')
