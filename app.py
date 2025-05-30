from flask import Flask
from routes import blueprints
from flask import session
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'super-secret-key-123' 
app.permanent_session_lifetime = timedelta(hours=1)

for bp in blueprints:
    app.register_blueprint(bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
