from django.shortcuts import render, redirect

def index(request):
    if request.session.get('access_token', None):
        return render(request, 'index.html')
    else:
        return redirect('login')

def login(request):
    return render(request, 'login.html')

def logout(request):
    pass

def deauth(request):
    pass