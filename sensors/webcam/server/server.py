from flask import Flask, request, jsonify
import json
import uuid

app = Flask(__name__)

@app.route('/api/images', methods=['GET'])
def get_image():
    return 'Get image'

if __name__ == '__main__':
    app.run()
