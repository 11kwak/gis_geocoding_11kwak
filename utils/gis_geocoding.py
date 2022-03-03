import pandas as pd
import requests
import json
from tqdm import tqdm

kakao_rest_api_key = input("KAKAO REST API KEY를 입력하세요 :")
latitude_list = []
longitude_list = []
    
# kakao api 활용해서 지오코딩 실시, 1개의 주소만 가능
def kakaogeocoding(addr):
    try:
        method = "GET"
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+addr
        headers = {"Authorization": f"KakaoAK {kakao_rest_api_key}"}

         #메인 코드
        result = json.loads(str(requests.request(method=method,url=url,headers=headers).text))
        match_first = result['documents'][0]['address']

        latitude = float(match_first['y']) #위도 
        longitude = float(match_first['x']) #경도

        return latitude, longitude

    # 지오코딩 실패한 행들 예외처리
    except:
        latitude = 0  
        longitude = 0 
        return latitude, longitude



# 반복문을 돌려서 csv 에 넣을 위도 경도 list 만들기
def geocoding(addr):

    for i in tqdm(addr):
         latitude, longitude  = kakaogeocoding(i)
         latitude_list.append(latitude)
         longitude_list.append(longitude)

    return latitude_list, longitude_list

    

    
