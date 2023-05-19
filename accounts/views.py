from django.shortcuts import render, redirect
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views import View
import requests
import json
import os
# Create your views here.

load_dotenv()

API_KEY = os.getenv('API_KEY')

class KakaoSigninView(View):
    def get(self, request):
        # dotenv 내의 api key 불러 오기
        api_key = API_KEY
        # redirect url 설정
        redirect_uri = 'http://localhost:8000/accounts/signin/kakao/callback'
        # 인증 url 설정
        kakao_auth_url = 'https://kauth.kakao.com/oauth/authorize?response_type=code'

        return redirect(f'{kakao_auth_url}&client_id={api_key}&redirect_uri={redirect_uri}')
    
class KakaoSigninCallbackView(View):
    def get(self, request):
        # Authorization Code 받아오기
        auth_code = request.GET.get('code')

        kakao_token_api = 'https://kauth.kakao.com/oauth/token'

        data = {
            'grant_type': 'authorization_code',
            'client_id': API_KEY,
            'redirection_uri': 'http://localhost:8000/accounts/signin/kakao/callback',
            'code': auth_code,
        }

        # access token 응답받기
        token_response = requests.post(kakao_token_api, data=data)

        access_token = token_response.json().get('access_token')
        # 유저 정보 응답 받기
        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer ${access_token}'})
        # json 형식으로 유저 정보 획득
        return JsonResponse({'user_info': user_info_response.json()})