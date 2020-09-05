from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    print("1")
    return jsonify({'status': 'ok'})