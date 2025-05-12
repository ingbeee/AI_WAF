from datasets import load_dataset
import pandas as pd

# 데이터셋 로드
dataset = load_dataset("YangYang-Research/web-attack-detection", split="train")
df = dataset.to_pandas()

# 컬럼명 변경: Sentence → Payload, Label → label
df.rename(columns={"Sentence": "Payload", "Label": "label"}, inplace=True)

# HTTP 헤더 관련 키워드 목록
http_keywords = [
    "content-length", "host:", "user-agent", "accept:", "referer:",
    "cookie:", "connection:", "sec-", "cache-control", "origin:",
    "upgrade-insecure-requests", "accept-encoding", "accept-language",
    "post ", "get ", "put ", "delete "
]

# 필터링 함수 정의
def is_raw_http(payload):
    if not isinstance(payload, str):
        return False
    payload_lower = payload.lower()
    return any(keyword in payload_lower for keyword in http_keywords)

# HTTP 헤더 포함된 행 제외
df_cleaned = df[~df["Payload"].apply(is_raw_http)]

# 필요한 순서대로 열 정렬
df_cleaned = df_cleaned[["Idx", "Payload", "label"]]

# 저장
df_cleaned.to_csv("C:\\Users\\jjj75\\Downloads\\cleaned_payloads_all4.csv", index=False)

print(f"최종 개수: {len(df_cleaned)}")
