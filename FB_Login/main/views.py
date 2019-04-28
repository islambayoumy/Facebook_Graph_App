from django.shortcuts import render, redirect, reverse
from django.conf import settings

import urllib.parse
import requests
import json
import base64
import hmac
import hashlib
import facebook

from .models import UserProfile
from django.contrib.auth.models import User


def index(request):
    token = request.session.get('access_token', None)
    if token:
        data = get_primary_data_from_profile(token)
        return render(request, 'index.html', data)
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
        return redirect('/error?error={}'.format(error))
    else:
        long_token, msg = login_request(settings.FACEBOOK_KEY,settings.FACEBOOK_SECRET,code)
        if long_token:
            request.session['access_token'] = long_token
            
            return redirect('index')
        else:
            return redirect('/error?error={}'.format(msg))

def login_request(app_id, app_secret, code):
    short_token = get_short_access_token(app_id, app_secret, code)
    long_token = exchange_access_token_len(app_id, app_secret, short_token)

    data = get_primary_data_from_profile(long_token)
    user = UserProfile.objects.filter(fb_id=data['id'])

    if user:
        try:
            user.update(access_token=long_token)
        except:
            return False, "updating failed"
    else:
        result, msg = save_user_data_to_db(data, long_token)
        if not result:
            return False, msg

    return long_token, None

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

def get_primary_data_from_profile(user_long_token):
    fields = "id,email,name,picture{url},first_name,last_name"
    graph = facebook.GraphAPI(access_token=user_long_token, version="3.1")
    return graph.get_object(id='me', fields=fields)

def save_user_data_to_db(data, user_long_token):
    try:
        user = User.objects.create(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'])
        user_obj = UserProfile.objects.create(
            user=user,
            access_token=user_long_token,
            picture=data['picture']['data']['url'],
            fb_id=data['id'])
        return True, 'added successfully'
    except:
        return False, 'error saving'

def logout(request):
    request.session['access_token'] = None
    return redirect('login')

def error(request):
    msg = request.GET.get('error', '')
    args = {'error': msg}
    return render(request, 'error.html', args)

def deauth(request):
    try:
        signed_request = request.POST['signed_request']
        encoded_sig, payload = signed_request.split('.')
    except (ValueError, KeyError):
        print('Invalid request')

    try:
        decoded_payload = base64.urlsafe_b64decode(payload + "==").decode('utf-8')
        decoded_payload = json.loads(decoded_payload)

        if type(decoded_payload) is not dict or 'user_id' not in decoded_payload.keys():
            print('Invalid payload data')

    except (ValueError, json.JSONDecodeError):
        print('Could not decode payload')

    try:
        secret = settings.FACEBOOK_SECRET

        sig = base64.urlsafe_b64decode(encoded_sig + "==")
        expected_sig = hmac.new(bytes(secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256)
    except:
        print('Could not decode signature')

    if not hmac.compare_digest(expected_sig.digest(), sig):
        print('Invalid request')

    user_id = decoded_payload['user_id']

    try:
        user = UserProfile.objects.get(fb_id=user_id).update(is_active=False)
    except UserProfile.DoesNotExist:
        print('succeeded')
