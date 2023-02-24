from django.urls import path
from django.urls.conf import include
from .views import *


urlpatterns = [
    
    path('google_token/', GoogleLogin.as_view(), name='google_token'),
    path('google_verify/', GoogleVerify.as_view(), name='google_verify')

]