from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse

import urllib.parse


def index(request):
    if request.session.get('access_token', None):
        return render(request, 'index.html')
    else:
        return redirect('login')

def login(request):
    error = request.GET.get('error', None)
    code = request.GET.get('code', None)
    if not error and not code:
        base_url = 'https://www.facebook.com/v3.2/dialog/oauth?{}'

        args = {"client_id": settings.FACEBOOK_KEY,
                "response_type": "code",
                "redirect_uri": "http://localhost:8000/login/",
                "scope": "email"}
        
        url = base_url.format(urllib.parse.urlencode(args))

        return render(request, 'login.html', {'url': url})
    elif error:
        args = {'error': error}
        return render(request, 'error.html', args)
    else:
        login_request()
        # return HttpResponse('code') ~ for testing

def login_request():
    pass

def logout(request):
    pass

def deauth(request):
    pass