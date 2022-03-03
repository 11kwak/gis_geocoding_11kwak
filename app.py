import utils.gis_geocoding as geo
import pandas as pd

"""
준비물 
1. 카카오 REST API 키 
2. 주소명 컬럼이 존재하는 csv 데이터파일

사용방법
1. 데이터 폴더를 만들고 안에 csv 형태의 데이터를 넣어주세요
2. 데이터파일 이름과 도로명, 지번 주소명을 가르키는 컬럼명을 지정해주세요
3. 터미널을 열어 $ python app.py를 실행하세요. 
"""

#데이터 파일 이름과 주소 컬럼명을 넣어주세요
csv_name = "data폴더안에 넣은 csv 파일의 이름을 넣어주세요"
address_name = "csv 파일 안에 도로명,지번 주소를 담은 컬럼명을 넣어주세요"




#데이터 불러오기
df = pd.read_csv(f"data/{csv_name}.csv",encoding="cp949")
df.drop(['Unnamed: 0'], axis=1, inplace=True)

#주소 컬럼명 지정 
addr = df[f"{address_name}"]

#함수 실행 
latitude_list, longitude_list = geo.geocoding(addr)

# df에 저장 
df["위도"] = latitude_list
df["경도"] = longitude_list

# 지오코딩에 실패한 열 삭제
idx = df[df["위도"]==0].index
print("지오코딩에 실패한 행의 수 :",len(idx))

df.drop(idx, inplace=True)
df.reset_index(drop=True,inplace=True)   #인덱스 초기화

df.to_csv("data/data.csv",encoding="cp949")
print("데이터 파일에 위도, 경도 컬럼이 추가되었습니다.")