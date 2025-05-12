import pandas as pd
import joblib
from sklearn.metrics import classification_report

# 1. 모델 및 벡터라이저 로드
model = joblib.load(r"D:\AI_dataset\in_use\rf_model.pkl")
vectorizer = joblib.load(r"D:\AI_dataset\in_use\tfidf_vectorizer.pkl")

# 2. 고도화된 페이로드들
test_data = [
    # 정상 요청 (label 0)
    "Welcome to our site!", "Contact us at support@example.com", "Click here to learn more.",
    "Our mission is to provide quality content.", "Thank you for visiting!", "Follow us on social media.",
    "Latest news updates available here.", "Download the latest version.", "Login to your account.",
    "Secure payment gateway enabled.", "Please enter your username.", "Password must be at least 8 characters.",
    "Your profile has been updated.", "Your session has timed out.", "Item added to cart successfully.",
    "Your order has been placed.", "Read our privacy policy.", "Cookies are used to improve experience.",
    "Subscription successful!", "Newsletter signup complete.", "Upload your document here.",
    "Download your file.", "Recent articles published.", "Browse categories.",
    "Add to wishlist.", "Save your progress.", "Sign up to receive updates.",
    "We value your feedback.", "Your account settings have been saved.", "View your transaction history.",
    
    # XSS 페이로드 (label 1)
    "<script>alert(1);</script>", "<img src='x' onerror='alert(1)'>", "<body onload='alert(\"XSS\")'>",
    "<iframe src='javascript:alert(2)'></iframe>", "<svg onload=alert(3)>", "<a href='javascript:alert(4)'>Click</a>",
    "<input type='text' value='<script>alert(5)</script>'>", "<div onmouseover='alert(6)'>Hover me</div>",
    "<marquee onstart='alert(7)'>Test</marquee>", "<b onmouseover=alert(8)>Bold</b>",
    "<button onclick='alert(9)'>Click</button>", "<form action='javascript:alert(10)'></form>",
    "<img src='nonexistent.png' onerror='alert(\"XSS\")'>", "<object data='javascript:alert(11)'></object>",
    "<embed src='javascript:alert(12)'>", "<meta http-equiv='refresh' content='0;url=javascript:alert(13)'>",
    "<audio src='invalid.mp3' onerror='alert(14)'></audio>", "<video src='invalid.mp4' onerror='alert(15)'></video>",
    "<img src='data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" onload=\"alert(16)\">'>",
    "<style>@import 'javascript:alert(17)';</style>", "<details ontoggle=alert(18)>Click me</details>",
    "<img src='x' onerror='this.onerror=null; alert(19);'>", "<link rel='stylesheet' href='javascript:alert(20)'>",
    "<script>fetch('/xss');</script>", "<object type='text/html' data='javascript:alert(21)'></object>",
    "<form><button formaction='javascript:alert(22)'>Submit</button></form>", "<input type='text' onfocus='alert(23)'>",
    "<meta charset='UTF-8' onerror='alert(24)'>", "<div data-test='<script>alert(25)</script>'></div>",
    "<a href='javascript:alert(\"XSS\")'>Test</a>",
    
    # SQLi 페이로드 (label 2)
    "' OR '1'='1'; --", "'; DROP TABLE users; --", "' OR 1=1#", 
    "admin'--", "' OR 'x'='x", "1' AND 1=1 --", "' OR '1'='1'/*", 
    "' UNION SELECT null, null, null --", "' OR ''=''", "admin' OR 1=1 --",
    "SELECT * FROM users WHERE username='admin'--", "1' UNION ALL SELECT username, password FROM users--",
    "SELECT version();", "SELECT user();", "SELECT database();", 
    "' AND 1=0 UNION SELECT 1,2,3 --", "admin' AND password='password' --",
    "' OR EXISTS (SELECT * FROM users)--", "1'; EXEC xp_cmdshell('dir'); --",
    "1' OR 'a'='a", "' AND pg_sleep(5)--", "SELECT * FROM information_schema.tables;",
    "' OR 'a'='a'--", "' AND 1=(SELECT COUNT(*) FROM users)--",
    "SELECT * FROM admin WHERE username='admin' AND password=''; --",
    "INSERT INTO users (username, password) VALUES ('admin', 'pass');",
    "SELECT * FROM accounts WHERE username='user' OR 1=1 --",
    "SELECT column_name FROM information_schema.columns WHERE table_name='users';",
    "DELETE FROM users WHERE username=''; --", "UPDATE users SET password='1234' WHERE username='admin';"
]

# 3. 벡터화 및 예측
X_test = vectorizer.transform(test_data)
y_pred = model.predict(X_test)

# 4. 예측 결과 데이터프레임 생성
results = pd.DataFrame({'Payload': test_data, 'Prediction': y_pred})
results['Attack Type'] = results['Prediction'].map({0: 'Normal', 1: 'XSS', 2: 'SQL Injection'})

# 5. 결과 출력
print(results)

# 6. 성능 평가
print("\nClassification Report:\n")
print(classification_report(y_pred, [0]*30 + [1]*30 + [2]*30))
