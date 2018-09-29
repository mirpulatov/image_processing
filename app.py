import uuid
import os
import resize_crop

from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES


app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'.format()
configure_uploads(app, photos)


@app.route('/api/v1/image/upload', methods=['POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        filename = 'uploads/' + str(filename)
        file_id = str(uuid.uuid4()).replace('-', '')
        img = resize_crop.ResizeCrop(filename=filename)
        path = img.resize()
        os.remove(filename)
        return jsonify({'path': path, 'id': file_id, 'status': 'active'}), 201
    return 'Error!'


@app.route('/api/v1/image/uploads/<image_id>/', methods=['GET'])
def get_photo(image_id):
    width = request.args.get('width', type=int)
    height = request.args.get('height', type=int)
    img = resize_crop.ResizeCrop(width=width, height=height, filename='uploads/' + str(image_id))
    if width is None and height is None:
        return jsonify({'path': image_id}), 200 ## In GET request 200 is more correct response code rather than 201
                                                ## 201 code is used only if something created via POST or PUT methods
    elif width >= 500:
        return jsonify({'path': image_id}), 200
    elif width < 500:
        res_file = img.resize()
        new_file = img.crop(res_file)
        os.remove(res_file)
        return jsonify({'path:': new_file}), 200
    else:
        return 'Error!'


if __name__ == '__main__':
    app.run(debug=True)
