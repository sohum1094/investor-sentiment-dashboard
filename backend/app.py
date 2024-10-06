from flask import Flask, send_file, jsonify
import os


app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the ISD backend'