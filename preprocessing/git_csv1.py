import requests
import pandas as pd
import csv

# raw 텍스트 파일 URL
url = "https://raw.githubusercontent.com/Proviesec/xss-payload-list/main/xss-all-list.txt"

# 파일 불러오기
response = requests.get(url)
lines = response.text.splitlines()

# 빈 줄, 주석 제거하고 페이로드만 추출
payloads = [line.strip() for line in lines if line.strip() and not line.startswith("#")]

# DataFrame 생성 + Label 컬럼 추가
df = pd.DataFrame(payloads, columns=['Payload'])
df['Label'] = 1

# 저장
df.to_csv(
    r"C:\Users\jjj75\Desktop\dataset\proviesec_xss_payloads.csv",
    index=False,
    encoding='utf-8-sig',
    quoting=csv.QUOTE_ALL,
    lineterminator='\n'
)

print(f"총 페이로드 수: {len(df)}")
