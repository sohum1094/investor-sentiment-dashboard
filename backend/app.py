from flask import Flask, send_file, jsonify
import os


app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the ISD backend'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)