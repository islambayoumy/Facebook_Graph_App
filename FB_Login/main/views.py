from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse

import urllib.parse
import requests
import json

from .models import UserProfile
from django.contrib.auth.models import User


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
        long_token = login_request(settings.FACEBOOK_KEY, settings.FACEBOOK_SECRET, code)

        request.session['access_token'] = long_token
        return redirect('index')


def login_request(app_id, app_secret, code):
    short_token = get_short_access_token(app_id, app_secret, code)
    long_token = exchange_access_token_len(app_id, app_secret, short_token)

    if UserProfile.objects.filter(access_token=long_token):
        print("get data from db")
    else:
        print("save to db")

    return long_token


def get_short_access_token(app_id, app_secret, code):
    base_url = 'https://graph.facebook.com/v3.2/oauth/access_token?{}'

    args = {
        "client_id": app_id,
        "client_secret": app_secret,
        "redirect_uri": "http://localhost:8000/login/",
        "code": code
    }
    code_url = base_url.format(urllib.parse.urlencode(args))

    return json.loads(requests.get(code_url).content)

def exchange_access_token_len(app_id, app_secret, user_short_token):
    base_url = "https://graph.facebook.com/oauth/access_token?{}"

    args = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": user_short_token['access_token']
    }
    access_token_url = base_url.format(urllib.parse.urlencode(args))
    result = requests.get(access_token_url).content

    access_token_info = json.loads(result.decode("utf-8"))
    return access_token_info['access_token']

def logout(request):
    pass

def deauth(request):
    pass