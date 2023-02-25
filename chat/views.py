from django.shortcuts import render
# from googletrans import Translator
# Create your views here.
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import Chat
from django.utils import timezone
import requests
import openai
from django.contrib.auth.models import User
from dotenv import load_dotenv
from rest_framework.authtoken.models import Token
from .serializers import ChatSerializer



# translator = Translator()
load_dotenv()

openai.api_key = str(os.getenv("OPENAI_API_KEY"))
gkey=str(os.getenv('GOOGLE_TRANSLATE_API'))

@api_view(['GET','POST'])
def openai_response(request):
    if request.method == 'POST':
        print("ENTERED " , request.POST.get('query'))
        response = openai.Completion.create(model="text-davinci-003",
         prompt=str(request.POST.get('query')),
          temperature=0.9,
           max_tokens=300)
        print(response)
        return Response(response['choices'][0].text)

    if request.method == 'GET':
        return Response("GETTED")

import time

davinci = "text-davinci-003"
currie = "text-curie-001"
@api_view(['GET','POST'])
def mizo_ai(request):

    print("GKEY" , gkey , os.environ['HOME'])
    if request.method == 'POST' and request.user.is_authenticated:
        mizo_final ={'ytes': str(request.user)}

        print("Start" , request.user)
       
        start_time = time.time()
        uid = request.user.id
        user= User.objects.get(id=uid)
        print("OK")
        try:

            individualUser = User.objects.get(email=user.email)
        except user.DoesNotExist:
            # individualUser = User.objects.create(email=user.email)
            # individualUser.save()
            raise ValueError('Wrong issuer.')


        print(individualUser)
        mizo1 = request.POST.get('query')
        chat = Chat.objects.create(user=individualUser)
        chat.query=mizo1
        print(chat)

        chat.query_timestamp=timezone.now()
        

        print(mizo1)
        English_response = requests.post('https://translation.googleapis.com/language/translate/v2',data={'q':mizo1,'key':gkey,'target':'en'})
        translated_english = English_response.json()['data']['translations'][0]['translatedText']
        chat.translated_query=translated_english

        print(translated_english)
        openai_response = openai.Completion.create(model=davinci,
         prompt=str(translated_english),
          temperature=0.3,
           max_tokens=500)
        print("openai response" ,openai_response)
        result_in_english = openai_response['choices'][0].text
        chat.original_response=result_in_english

        language_detect= requests.post('https://translation.googleapis.com/language/translate/v2/detect',data={'q':result_in_english,'key':gkey})
        language =language_detect.json()['data']['detections'][0][0]['language']
        confidence =language_detect.json()['data']['detections'][0][0]['confidence']
        print("Translator Detected lang: " ,language_detect.json()['data']['detections'][0][0]['language'])

        if language == 'lus' and confidence >= 0.7:
            mizo_final = result_in_english
            print('Mizo a nih chuan leh Confidence 0.7 chunglam a nih chuan a let lo' , language,confidence)
        elif language != 'en' and language != 'lus' and confidence >= 0.7:

            mizo_response = requests.post('https://translation.googleapis.com/language/translate/v2',data={'q':result_in_english,'key':gkey,'target':language})
            print(mizo_response.json()['data']['translations'][0]['translatedText'])
            mizo_final = mizo_response.json()['data']['translations'][0]['translatedText']
            print('English a nih loh chuan leh Confidence 0.7 chunglam a nih chuan chumi tawngah chuan a let ang' , language,confidence)
        elif language == 'en' :

            mizo_response = requests.post('https://translation.googleapis.com/language/translate/v2',data={'q':result_in_english,'key':gkey,'target':'lus','format':'text'})
            print(mizo_response.json()['data']['translations'][0]['translatedText'])
            mizo_final = mizo_response.json()['data']['translations'][0]['translatedText']
            print('Mizo in kan let ang' , language,confidence)

        chat.final_language = language
        chat.language_confidence = confidence
        chat.response=mizo_final
        chat.response_timestamp=timezone.now()
        chat.created = openai_response['created']
        chat.duration = (time.time() - start_time)
        chat.save()

        # return Response({'mizo':mizo_final})
        print("--- %s seconds ---" % (time.time() - start_time))
        return Response(mizo_final)


@api_view(['GET','POST'])
def messages(request):
    if request.method == 'GET' and request.user.is_authenticated:
        token_key = str(request.headers['Authorization'])[6:]
        token = Token.objects.get(key=str(token_key))
        user = User.objects.get(id=token.user_id)
        chats = Chat.objects.filter(user=user)
        serializer = ChatSerializer(chats,many=True)
        return Response({'data':serializer.data})



