import pandas as pd

# CSV 불러오기
df = pd.read_csv(r"C:\Users\jjj75\Desktop\dataset\SQLiV3_33000.csv")

# Label 컬럼을 숫자로 바꿔서 정상적인 행만 추출
df['Label'] = pd.to_numeric(df['Label'], errors='coerce')  # 숫자로 변환 가능한 경우만
filtered_df = df[df['Label'] == 0]  # 진짜 0인 것만

# 컬럼 이름 변경
filtered_df = filtered_df.rename(columns={'Sentence': 'Payload'})

# 필요한 열만 선택 (Payload, Label)
filtered_df = filtered_df[['Payload', 'Label']]

# 저장
save_path = r"C:\Users\jjj75\Desktop\dataset\filtered_output_0.csv"
filtered_df.to_csv(save_path, index=False)

# 결과 확인
print(f"최종 개수: {len(filtered_df)}")
