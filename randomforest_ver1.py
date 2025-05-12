import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 1. 데이터 불러오기
df = pd.read_csv(r"D:\AI_dataset\bin_class\cleaning_Data\merged_payloads.csv", encoding='ISO-8859-1')
print(df.columns)


# 결측치 제거 (전체가 아니라 Payload 열만 기준으로)
df = df.dropna(subset=['Payload'])

# 2. X, y 분리
X_raw = df['Payload']
y = df['label']


# 3. TF-IDF 벡터화 (문자 단위 n-gram)
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3), max_features=2000)
X = vectorizer.fit_transform(X_raw)

# 4. 학습/검증 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. 평가
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 7. 저장
joblib.dump(model, r"D:\AI_dataset\bin_class\cleaning_Data\rf_model.pkl")
joblib.dump(vectorizer, r"D:\AI_dataset\bin_class\cleaning_Data\tfidf_vectorizer.pkl")
