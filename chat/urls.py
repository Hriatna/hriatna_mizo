from django.urls import path

from .views import *
urlpatterns = [
    path('',openai_response,name="chat"),
    path('mizo/',mizo_ai,name="mizo ai"),
    path('messages/',messages,name="message list"),


    # path('getmyprofile/',getMyProfile,name="my profile"),


   



    # allauth oauth2
    # path('account/facebook/', FacebookLogin.as_view(), name='fb_login'),
    # path('account/google/', GoogleLogin.as_view(), name='google_login'),
     






]
