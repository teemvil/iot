import base64
from flask import Flask, request, jsonify, send_file
import cv2
import json
import uuid

app = Flask(__name__)


def take_picture():
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    img_name = 'webcam_pic.jpg'
    cv2.imwrite(img_name, frame)

    cap.release()
    cv2.destroyAllWindows()


@app.route('/api/images', methods=['GET'])
def get_image():
    take_picture()
    return send_file('webcam_pic.jpg', mimetype="image/jpg")
    # with open('webcam_pic.jpg', 'rb') as image_file:
        # encoded_string = base64.b64encode(image_file.read())
        # return encoded_string


if __name__ == '__main__':
    app.run()
