from flask import Flask
from routes.main import main
from routes.about import about

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(about)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
