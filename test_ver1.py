import joblib

# 1. 모델 로드
model_path = r"D:\AI_dataset\bin_class\cleaning_Data\rf_model.pkl"
vectorizer_path = r"D:\AI_dataset\bin_class\cleaning_Data\tfidf_vectorizer.pkl"

loaded_model = joblib.load(model_path)
loaded_vectorizer = joblib.load(vectorizer_path)

# 2. XSS 테스트 페이로드
xss_payloads = [
   '<img src=1 href=1 onerror="javascript:alert(1)"></img>',
    '<audio src=1 href=1 onerror="javascript:alert(1)"></audio>',
    '<video src=1 href=1 onerror="javascript:alert(1)"></video>',
    '<body src=1 href=1 onerror="javascript:alert(1)"></body>',
    '<image src=1 href=1 onerror="javascript:alert(1)"></image>',
    '<object src=1 href=1 onerror="javascript:alert(1)"></object>',
    '<script src=1 href=1 onerror="javascript:alert(1)"></script>',
    '<svg onResize svg onResize="javascript:javascript:alert(1)"></svg onResize>',
    '<title onPropertyChange title onPropertyChange="javascript:javascript:alert(1)"></title onPropertyChange>',
    '<iframe onLoad iframe onLoad="javascript:javascript:alert(1)"></iframe onLoad>',
    '<body onMouseEnter body onMouseEnter="javascript:javascript:alert(1)"></body onMouseEnter>',
    '<body onFocus body onFocus="javascript:javascript:alert(1)"></body onFocus>',
    '<frameset onScroll frameset onScroll="javascript:javascript:alert(1)"></frameset onScroll>',
    '<script onReadyStateChange script onReadyStateChange="javascript:javascript:alert(1)"></script onReadyStateChange>',
    '<html onMouseUp html onMouseUp="javascript:javascript:alert(1)"></html onMouseUp>',
    '<body onPropertyChange body onPropertyChange="javascript:javascript:alert(1)"></body onPropertyChange>',
    '<svg onLoad svg onLoad="javascript:javascript:alert(1)"></svg onLoad>'
]

# 3. SQLi 테스트 페이로드
sqli_payloads = [
    "' OR '1'='1", 
    "' OR '1'='1' --", 
    "' OR 1=1--", 
    "' OR 1=1#", 
    "' OR 1=1/*", 
    "' OR 'a'='a", 
    "' OR 'a'='a' --", 
    "admin' --", 
    "admin' #", 
    "admin'/*", 
    "admin' OR '1'='1", 
    "admin' OR 1=1--", 
    "admin' OR 1=1#", 
    "admin' OR 1=1/*", 
    "' OR EXISTS(SELECT * FROM users)--", 
    "' UNION SELECT null, version()--", 
    "' UNION SELECT ALL FROM information_schema.tables--", 
    "' AND 1=0 UNION ALL SELECT null, username, password FROM users--", 
    "' UNION SELECT username, password FROM users--", 
    "' OR 'x'='x'--"
]

# 4. 테스트 페이로드 병합
test_payloads = xss_payloads + sqli_payloads

# 5. 벡터화 및 예측
X_test = loaded_vectorizer.transform(test_payloads)
y_pred = loaded_model.predict(X_test)

# 6. 예측 결과 출력
for payload, pred in zip(test_payloads, y_pred):
    attack_type = "XSS" if pred == 1 else "SQL Injection" if pred == 2 else "Unknown"
    print(f"Payload: {payload} -> attack detected: {attack_type}")
