import requests
from extract_metadata import extract_metadata

URL = 'http://127.0.0.1:5000/api/'

def send_image_request(image_name):
    try:
        files = {'media': open(image_name, 'rb')}
    except FileNotFoundError:
        # TODO: handle exceptions..
        print("File not found")

    try:
        r = requests.post(f'{URL}/images', files=files)
        print(r.json())
    except BaseException as e:
        # TODO: handle exceptions..
        print(e)

def main():
    send_image_request('pic_with_metadata.jpg')


if __name__ == '__main__':
    main()