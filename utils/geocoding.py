import requests
import json
from tqdm import tqdm
import time

kakao_rest_api_key = input("KAKAO REST API KEY를 입력하세요 :")
latitude_list = []
longitude_list = []

# 카카오 REST API KEY 검증용
try:
    auth_method = "GET"
    auth_url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+"경기도 파주시 군내면 대성동길 151-13"
    auth_headers = {"Authorization": f"KakaoAK {kakao_rest_api_key}"}
    auth_result = json.loads(str(requests.request(method=auth_method, url=auth_url, headers=auth_headers).text))
    auth_match = auth_result['documents'][0]['address']
    lat = float(auth_match['y'])
    print("KAKAO REST API KEY가 정상입니다.")

except Exception:
    print("KAKAO REST API KEY가 잘못되었습니다. 다시 입력하세요.")
    exit()


def kakao_geocoding(address):
    '''
    kakao api를 활용해서 지오코딩 실시합니다.
    address = 도로명 주소, 지번 주소만 가능합니다.
    주소에 맞는 위도(latitude)와 경도(longtitude)를 return 합니다.
    '''
    method = "GET"
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+address
    headers = {"Authorization": f"KakaoAK {kakao_rest_api_key}"}

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


def geocoding_action(df):
    '''
    input data로 df를 받아서 위도, 경도 컬럼이 추가된 df를 return 합니다.
    최종 실행 함수입니다.
    '''
    print(df.columns)
    time.sleep(1)
    address_name = input("데이터 파일에 주소명을 담고 있는 컬럼명을 넣어주세요 : ")
    addr = df[f"{address_name}"]

    latitude_list, longitude_list = kakao_geocoding_to_list(addr)

    df["latitude"] = latitude_list
    df["longitude"] = longitude_list

    idx = df[df["latitude"] == 0].index
    print("##############################################################################################################")
    print("지오코딩에 실패한 행의 수 :", len(idx))
    print("지오코딩에 실패한 행의 인덱스 :", idx)
    print("##############################################################################################################")

    return df


if __name__ == "__main__":
    print("모듈을 import 해서 실행파일에서 함수로 사용하세요.")
