import requests
import json
from tqdm import tqdm

kakao_rest_api_key = input("KAKAO REST API KEY를 입력하세요 :")
latitude_list = []
longitude_list = []

def kakao_auth(kakao_rest_api_key):
    '''
    카카오 REST API 키 오류인지를 확인하기 위한 함수 입니다.
    판문점 위도값의 반올림은 항상 38이여야 합니다. 만약 그렇지 않다면 REST API 키 오류입니다.
    '''
    try:
        method = "GET"
        checkurl = 'https://dapi.kakao.com/v2/local/search/address.json?query='+"경기도 파주시 군내면 대성동길 151-13"
        headers = {"Authorization": f"KakaoAK {kakao_rest_api_key}"}
        check = json.loads(str(requests.request(method=method, url=checkurl, headers=headers).text))
        match = check['documents'][0]['address']
        lat = float(match['y'])

        return round(lat)

    except Exception:
        print("KAKAO REST API KEY가 잘못되었습니다.")


def kakao_geocoding(address):
    '''
    kakao api를 활용해서 지오코딩 실시합니다.
    address = 도로명 주소, 지번 주소만 가능합니다.
    주소에 맞는 위도(latitude)와 경도(longtitude)를 return 합니다.
    '''
    method = "GET"
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+address
    headers = {"Authorization": f"KakaoAK {kakao_rest_api_key}"}

    # 카카오 REST API 키가 정상이여야만 실행
    if kakao_auth(kakao_rest_api_key) == 38:
        # 메인 코드
        try:
            result = json.loads(str(requests.request(method=method, url=url, headers=headers).text))
            match_first = result['documents'][0]['address']

            latitude = float(match_first['y'])
            longitude = float(match_first['x'])

        # 지오코딩 실패한 행의 위도와 경도값은 0으로 예외처리합니다.
        except Exception:
            latitude = 0
            longitude = 0

        return latitude, longitude


def kakao_geocoding_to_list(addresslist):
    '''
    list 형태의 addresslist를 넣은 후반복문을 돌려서 csv 에 넣을 위도 경도 list 만듭니다.
    addresslist = 도로명 주소, 지번 주소를 담은 list만 가능합니다.
    주소에 맞는 위도(latitude)와 경도(longtitude)를 list 형태로 return 합니다.
    '''
    for i in tqdm(addresslist):
        latitude, longitude = kakao_geocoding(i)
        latitude_list.append(latitude)
        longitude_list.append(longitude)

    return latitude_list, longitude_list


if __name__ == "__main__":
    print("모듈을 import 해서 실행파일에서 함수로 사용하세요.\nkakao_gecoding(address) : 주소를 입력하면 return latitude, longitude \nkakao_geocoding_list(addresslist) : 주소 리스트를 입력하면 return latitude_list, longitude_list ")
