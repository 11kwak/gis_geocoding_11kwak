import utils.geocoding as geo
import pandas as pd

# df 설정하기
PATH = "data/data"
df = pd.read_csv(f"{PATH}.csv", encoding="cp949")

# 지오코딩 함수 실행
df = geo.geocoding_action(df)

# 지오코딩 완료된 df 저장하기
df.to_csv(f"{PATH}(지오코딩실행).csv", encoding="cp949")

# # 지오코딩에 실패한 열 삭제 - 필요시 진행
# idx = df[df["위도"]==0].index
# print("##############################################################################################################")
# print("지오코딩에 실패한 행의 수 :", len(idx))
# print("지오코딩에 실패한 행의 인덱스 :", idx)
# print("##############################################################################################################")
# df.drop(idx, inplace=True)
# df.reset_index(drop=True, inplace=True)

# df.to_csv(f"{PATH}(지오코딩 실패 행 삭제).csv", encoding="cp949")
