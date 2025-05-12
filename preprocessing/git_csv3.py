import requests
import pandas as pd
import csv

# GitHub의 README.md raw URL
url = "https://raw.githubusercontent.com/payloadbox/xss-payload-list/master/README.md"

# 파일 내용 불러오기
response = requests.get(url)
lines = response.text.splitlines()

# 코드 블록 안의 페이로드만 추출 (주석 제거 포함)
payloads = []
inside_code_block = False

for line in lines:
    line = line.strip()
    if line.startswith("```"):
        inside_code_block = not inside_code_block
        continue
    if inside_code_block:
        # HTML 주석, 빈 줄 제거
        if line.startswith("<!--") or line.endswith("-->") or not line:
            continue
        payloads.append(line)

# DataFrame 생성 + Label 컬럼 추가
df = pd.DataFrame(payloads, columns=['Payload'])
df['Label'] = 1  # 모두 1로 채움

# CSV 저장 (Excel 호환)
df.to_csv(
    r"C:\Users\jjj75\Desktop\dataset\github_xss_payloads.csv",
    index=False,
    encoding='utf-8-sig',
    quoting=csv.QUOTE_ALL,
    lineterminator='\n'
)

print(f"총 페이로드 수: {len(df)}")
