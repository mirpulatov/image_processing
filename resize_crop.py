import uuid
from PIL import Image


class ResizeCrop:
    _width = None
    _height = None
    _filename = None

    def __init__(self, width, height, filename):
        self._width = width
        self._height = height
        self._filename = filename

    def resize(self):
        img = Image.open(self._filename)
        wpercent = (self._width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((self._width, hsize), Image.ANTIALIAS)
        resized_file = 'uploads/' + str(uuid.uuid4()) + '.jpg'
        img.save(resized_file)
        img.close()
        return resized_file

    def crop(self, tmp_filename):
        img = Image.open(tmp_filename)
        width, height = img.size
        centre = [width / 2, height / 2]
        area = (centre[0] - self._width / 2, centre[1] - self._height / 2, centre[0] + self._width / 2,
                centre[1] + self._height / 2)
        cropped_img = img.crop(area)
        file_name = 'uploads/' + str(uuid.uuid4()) + '.jpg'
        cropped_img.save(file_name)
        img.close()
        return file_name
