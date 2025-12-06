from flask import Flask, jsonify
import os

app = Flask(__name__)
counter = 0

@app.route('/api/visits')
def visits():
    global counter
    counter += 1
    return jsonify({"visits": counter})

@app.route('/')
def root():
    return "Visitor API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
