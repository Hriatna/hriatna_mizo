from django.shortcuts import render
import requests
from rest_framework.response import Response
from google.oauth2 import id_token


from rest_framework import status, serializers
from rest_framework.views import APIView

from google.auth.transport import requests as req

# Create your views here.


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import IsAuthenticated,AllowAny



class GoogleLoginI(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter


class GoogleLogin(SocialLoginView):
    """Google login endpoint"""
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:8000/accounts/google/login/callback/'

MY_CLIENT_ID ='289661815591-bhpu0sj4ppfe2ob6a0q4mu5d5r4ag95u.apps.googleusercontent.com'
request = req.Request()

class GoogleVerify(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        print("STARTING")

        token = {'id_token': request.data.get('id_token'),'email':request.data.get('email')}
        print(token)

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            # idinfo = id_token.verify_oauth2_token(token['id_token'], request, MY_CLIENT_ID)
            idinfo = requests.post('https://oauth2.googleapis.com/tokeninfo?id_token='+token['id_token']).json()
            print(idinfo)
            
            res=[]
            if idinfo['iss']  in ['accounts.google.com', 'https://accounts.google.com'] and idinfo['email'] == token['email']:
                c =createUserToken(idinfo['name'],idinfo['email'])
                res={'token':c}

            elif idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            # if mail passed along token is same as idinfo['email']



# call create user function

# and return the token here
            return Response(res)
        except ValueError as err:
            # Invalid token
            print(err)
            content = {'message': 'Invalid token'}
            return Response(content)

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


def createUserToken(name,email):
    try:
        u,created = User.objects.get_or_create(username=name, email=email)
        print( "USER ", u , "Created" , created)
        if created:
            print("created" , created)
            u1 = User.objects.get(email=email)
            t = Token.objects.create(user=u1)
            return str(t)
        else:
            print('existing' , u)
            t = Token.objects.get(user=u)
            print(t)
            return str(t)
    except ValueError as err:
        print(err)
        return err
