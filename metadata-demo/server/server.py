from flask import Flask, request, jsonify
from extract_metadata import extract_metadata
import json
import uuid

app = Flask(__name__)

# This is here for testing purposes only. Data received from
# the client is going to be stored in the blockchain or similar.
images = []


@app.route('/api/images', methods=['GET', 'POST'])
def handle_images() -> str:
    if request.method == 'GET':
        # This here should return the image metadata stored somewhere.
        return jsonify(images)
    elif request.method == 'POST':
        received_image = request.files['media']
        metadata = extract_metadata(received_image)
        function_that_needs_to_be_moved_somewhere(metadata)

        return json.dumps(metadata)


@app.route('/api/images/<int:image_id>', methods=['GET'])
def get_single_image(image_id):
    print(image_id)
    return f'image_id {image_id}'


def function_that_needs_to_be_moved_somewhere(data):
    data['id'] = str(uuid.uuid4())
    images.append(data)


if __name__ == '__main__':
    app.run()
