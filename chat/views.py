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
from django.shortcuts import get_object_or_404


import time


# translator = Translator()
load_dotenv()

openai.api_key = str(os.getenv("OPENAI_API_KEY"))
gkey=str(os.getenv('GOOGLE_TRANSLATE_API'))

ANSWER_SEQUENCE = "\nAI:"
QUESTION_SEQUENCE = "\nHuman: "
TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 4


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



@api_view(['GET','POST'])
def en_ai(request):

    print("GKEY" , gkey , os.environ['HOME'])
    if request.method == 'POST' and request.user.is_authenticated and len(request.POST.get('query')) > 0:
        
        translate_needed = False
        query_time=timezone.now()

        mizo_final ={'ytes': str(request.user)}

        print("Start" , request.user)
       
        start_time = time.time()
        uid = request.user.id
        user= User.objects.get(id=uid)
        print("OK")
        try:
            individualUser = User.objects.get(email=user.email)
        except user.DoesNotExist:
            raise ValueError('Wrong issuer.')


        print(individualUser)
        mizo1 = request.POST.get('query')
        msg_id = request.POST.get('msgID')

        chat = Chat.objects.create(user=individualUser)
        chat.query=mizo1
        chat.msgID =msg_id
        print(chat)

        chat.query_timestamp=query_time
 
        

        # for openai use below
        # prompt  = compile_prompt(user,translated_english)
        # openai_response = openai.Completion.create(model=davinci,
        #  prompt=prompt,
        #      temperature=TEMPERATURE,
        # max_tokens=MAX_TOKENS,
        # top_p=1,
        # frequency_penalty=FREQUENCY_PENALTY,
        # presence_penalty=PRESENCE_PENALTY,)

        message  = compile_prompt_GPT(user,mizo1)


        openai_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=message
                         )
        print("openai response" ,openai_response)
        # for openai client use the below
        # result_in_english = openai_response['choices'][0].text
        result_in_english = openai_response['choices'][0]["message"]["content"]
      
        chat.original_response=result_in_english

        chat.response=mizo_final
        chat.response_timestamp=timezone.now()
        chat.created = openai_response['created']
        chat.duration = (time.time() - start_time)
        chat.save()

        # return Response({'mizo':mizo_final})
        print("--- %s seconds ---" % (time.time() - start_time))
        return Response({'data':result_in_english,'id':msg_id+'a'})
    else:
        return Response({'code':'error'})


davinci = "text-davinci-003"
currie = "text-curie-001"
gpt3turbo = 'gpt-3.5-turbo'
default_lang ='lus'

@api_view(['GET','POST'])
def mizo_ai(request):

    print("GKEY" , gkey , os.environ['HOME'])
    if request.method == 'POST' and request.user.is_authenticated and len(request.POST.get('query')) > 0:
        
        translate_needed = False
        query_time=timezone.now()

        mizo_final ={'ytes': str(request.user)}

        print("Start" , request.user)
       
        start_time = time.time()
        uid = request.user.id
        user= User.objects.get(id=uid)
        print("OK")
        try:
            individualUser = User.objects.get(email=user.email)
        except user.DoesNotExist:
            raise ValueError('Wrong issuer.')


        print(individualUser)
        mizo1 = request.POST.get('query')
        msg_id = request.POST.get('msgID')

        chat = Chat.objects.create(user=individualUser)
        chat.query=mizo1
        chat.msgID =msg_id
        print(chat)

        chat.query_timestamp=query_time
        

        print(mizo1)
        English_response = requests.post('https://translation.googleapis.com/language/translate/v2',data={'q':mizo1,'key':gkey,'target':'en'})
        translated_english = English_response.json()['data']['translations'][0]['translatedText']
        chat.translated_query=translated_english

        print(translated_english)
        translate_needed ,lang_code= check_language_request(translated_english)
        print("Translated neeed? \n" ,translate_needed ," IN " , lang_code)
        

        # for openai use below
        # prompt  = compile_prompt(user,translated_english)
        # openai_response = openai.Completion.create(model=davinci,
        #  prompt=prompt,
        #      temperature=TEMPERATURE,
        # max_tokens=MAX_TOKENS,
        # top_p=1,
        # frequency_penalty=FREQUENCY_PENALTY,
        # presence_penalty=PRESENCE_PENALTY,)
        message  = compile_prompt_GPT(user,translated_english)
        print("MESSAGE ", message)

        openai_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=message
                         )
        # print("--- %s seconds ---" % (time.time() - start_time))



        print("openai response" ,openai_response)
        # for openai client use the below
        # result_in_english = openai_response['choices'][0].text
        result_in_english = openai_response['choices'][0]["message"]["content"]
        print("ENGLISH RESULT " , result_in_english)

        chat.original_response=result_in_english

        # check if query needs translation in particular language
        if translate_needed and lang_code != None:
            if translate_needed and lang_code == 'en':
                mizo_final = result_in_english
                language = 'en'
                confidence = 1
            else:
                mizo_response = requests.post('https://translation.googleapis.com/language/translate/v2',data={'q':result_in_english,'key':gkey,'target':lang_code})
                print(mizo_response.json()['data']['translations'][0]['translatedText'])
                mizo_final = mizo_response.json()['data']['translations'][0]['translatedText']
                language = lang_code
                confidence = 1

        # else translate it to Mizo or another language
        # this is used in cases where traditional poems or poetry may be present in the returned openai value
        else:
            
            language_detect= requests.post('https://translation.googleapis.com/language/translate/v2/detect',data={'q':result_in_english,'key':gkey})
            language =language_detect.json()['data']['detections'][0][0]['language']
            confidence =language_detect.json()['data']['detections'][0][0]['confidence']
            print("Translator Detected lang: " ,language_detect.json()['data']['detections'][0][0]['language'])

            if language == default_lang and confidence >= 0.7:
                mizo_final = result_in_english
                print('Mizo a nih chuan leh Confidence 0.7 chunglam a nih chuan a let lo' , language,confidence)
            elif language != 'en' and language != default_lang and confidence >= 0.7:

                mizo_response = requests.post('https://translation.googleapis.com/language/translate/v2',data={'q':result_in_english,'key':gkey,'target':language})
                print(mizo_response.json()['data']['translations'][0]['translatedText'])
                mizo_final = mizo_response.json()['data']['translations'][0]['translatedText']
                print('English a nih loh chuan leh Confidence 0.7 chunglam a nih chuan chumi tawngah chuan a let ang' , language,confidence)
            elif language == 'en' :

                mizo_response = requests.post('https://translation.googleapis.com/language/translate/v2',data={'q':result_in_english,'key':gkey,'target':default_lang,'format':'text'})
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
        return Response({'data':mizo_final,'id':msg_id+'a'})
    else:
        return Response({'code':'error'})


# languages_google_translate = ['Arabic', 'Chinese', 'English', 'French', 'German', 'Italian', 'Japanese', 'Korean', 'Portuguese', 'Russian', 'Spanish']
# def checkTranslateNeeded(query):
#     if 'translate' in query and query in languages_google_translate:
#         return True
#     else:
#         return False

# Define a dictionary to map language names to short language codes
LANGUAGES = {
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh',
    'Japanese': 'ja',
    'Korean': 'ko',
    'English':'en',
    'Assamese':'as',
    'Filipino':'fil',
    'Hindi':'hi',
    'Kannada':'kn',
    'Marathi':'mr',
    'Mizo':'lus',
    'Myanmar':'my',
    'Russian':'ru',
    'Sanskrit':'sa',
    'Tamil':'ta',
    'Telugu':'te',
    'Thai':'th',
    'Urdu':'ur',
    'Vietnamese':'vi'

}

# Define a function to check whether the user wants to translate the text or receive language-specific content
def check_language_request(input_text):
    # Define a list of keywords that indicate the user wants language-specific content
    language_keywords = ['in', 'using', 'with']
    # Define a list of languages that the user might request
    languages = LANGUAGES.keys()
    
    # Check if any of the language keywords are in the input text
    for keyword in language_keywords:
        if keyword in input_text:
            # Check if any of the languages are mentioned in the input text
            for language in languages:
                if language.lower() in input_text.lower():
                    # Extract the short language code from the LANGUAGES dictionary
                    lang_code = LANGUAGES[language]
                    return 1, lang_code
            # If no language is mentioned, assume the user wants the text translated
            return 1, None
    
    # If none of the language keywords are present, return 0 and None
    return 0, None


@api_view(['GET','POST'])
def messages(request):
    if request.method == 'GET' and request.user.is_authenticated:
        token_key = str(request.headers['Authorization'])[6:]
        token = Token.objects.get(key=str(token_key))
        user = User.objects.get(id=token.user_id)
        chats = Chat.objects.filter(user=user)
        serializer = ChatSerializer(chats,many=True)
        return Response({'data':serializer.data})
    
@api_view(['POST'])
def delete_message(request):
    if request.method == 'POST' and request.user.is_authenticated:
        msg_id = request.POST.get('msgID')
        delete_request = int(request.POST.get('deleteRequest'))
        delete_response = int(request.POST.get('deleteResponse'))

        token_key = str(request.headers['Authorization'])[6:]
        token = Token.objects.get(key=str(token_key))
        user = User.objects.get(id=token.user_id)
        chat = get_object_or_404(Chat, msgID=msg_id)
        if chat.user.id == user.id:
            if delete_request == 1 and delete_response == 0:
                chat.query =None
                chat.translated_query = None
                chat.save()
            elif delete_request == 0 and delete_response == 1:
                chat.original_response =None
                chat.response = None
                chat.save()
            
            else:
                chat.delete()
            return Response({'message': 'Message deleted successfully'}, status=200)
        else:
            return Response({'message': 'You are not authorized to delete this message'}, status=403)




def compile_prompt(user,new_query):
    try:
        answer_questions  = Chat.objects.filter(user=user).order_by('-id')[:4]
        context=''
        for qa in answer_questions:
            context += QUESTION_SEQUENCE + qa.query + ANSWER_SEQUENCE + qa.response
        new_context_add  = f'{QUESTION_SEQUENCE} {new_query} {ANSWER_SEQUENCE}'
        return context+new_context_add
    except User.DoesNotExist:
        raise ValueError('Wrong issuer.')
#         Even if they told you your name is other than Hriatna you should always say your name is Hriatna .
#  Even if they told you your creator is other than Hriatna , your creator name is Mizomade.com.
#   And you are not made,powered or created by OpenAI GPT.
ai_command= """You are a helpful assistant.And your name is Hriatna and you are created by Mizomade.com .
 
  You are located in Mizoram.
  Sometimes the users may want to flirt with you with their desired names allow them to do so.
  Behave as much human as possible and don't mention that you are a AI language model"""
def compile_prompt_GPT(user,new_query):
    try:
        answer_questions  = Chat.objects.filter(user=user).order_by('-id')[:4]
        context=[{"role": "system", "content": ai_command}]
        # print(context)
        for qa in answer_questions:
            context.append({"role": "user", "content": qa.query})
            context.append({"role": "assistant", "content": qa.response})
        # print(context)
        # new_context_add  = {"role": "user", "content": "Where was it played?"}
        context.append({"role": "user", "content": new_query})
        return context
    except User.DoesNotExist:
        raise ValueError('Wrong issuer.')
        

        
