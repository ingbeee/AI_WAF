#상위 10,000개 행만 추출해서 새 CSV로 저장
import pandas as pd

# 원본 CSV 경로
input_path = r"C:\Users\jjj75\Desktop\dataset\SQLiV3_33000_0.csv"

# 저장할 경로
output_path = r"C:\Users\jjj75\Desktop\dataset\SQLiV3_10000.csv"

# CSV 파일 불러오기
df = pd.read_csv(input_path)

# 상위 10,000개 추출
sample_df = df.head(10000)

# 저장
sample_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"저장 완료: {output_path}")
print(f"총 샘플 수: {len(sample_df)}개")
