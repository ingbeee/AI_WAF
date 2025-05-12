# 필수 라이브러리 설치
!pip install tensorflow joblib

# 라이브러리 임포트
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from google.colab import files
import joblib

# 데이터 로드
file_path = "/content/merged_payload.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# 데이터 전처리: 결측치 제거 및 중복 제거
df = df.dropna(subset=['Payload']).drop_duplicates(subset=['Payload'])
print(f"데이터 크기: {df.shape}")

# X, y 분리
X_raw = df['Payload'].astype(str)
y = df['label']

# TF-IDF 벡터화 (문자 단위 n-gram)
vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(1, 5), max_features=5000)
X = vectorizer.fit_transform(X_raw).toarray()

# 레이블 인코딩
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# 학습/검증 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LSTM 모델 구성
model = Sequential([
    Embedding(input_dim=5000, output_dim=128, input_length=X.shape[1]),
    LSTM(128, return_sequences=False),
    Dense(64, activation='relu'),
    Dense(3, activation='softmax')
])

# 모델 컴파일
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 조기 종료 설정 (과적합 방지)
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# 모델 학습
model.fit(X_train, y_train, epochs=10, batch_size=128, validation_data=(X_test, y_test), callbacks=[early_stopping])

# 평가
loss, accuracy = model.evaluate(X_test, y_test)
print(f"LSTM 모델 정확도: {accuracy * 100:.2f}%")

# 모델 저장
model.save('/content/lstm_model.h5')
joblib.dump(vectorizer, '/content/tfidf_vectorizer.pkl')

# 파일 다운로드
files.download('/content/lstm_model.h5')
files.download('/content/tfidf_vectorizer.pkl')
