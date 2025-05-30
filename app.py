from flask import Flask
from routes import blueprints

app = Flask(__name__)
app.secret_key = 'super-secret-key-123' 

for bp in blueprints:
    app.register_blueprint(bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
