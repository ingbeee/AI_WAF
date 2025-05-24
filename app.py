from flask import Flask, render_template, jsonify, request, redirect, url_for
from routes.main import main

app = Flask(__name__)
    
app.register_blueprint(main, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
