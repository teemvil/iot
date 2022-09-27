from PIL import Image
from PIL.TiffImagePlugin import IFDRational
from PIL.ExifTags import TAGS
import json

# Extracts metadata from the given file. Returns a json string containing the
# information gathered from the image file.


def extract_metadata(file):
    image = Image.open(file.stream)
    exifdata = image.getexif()

    image_metadata = {}

    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)

        if isinstance(data, bytes):
            data = data.decode()

        # Change datatype from IFDRational to float so the dictionary
        # can be serialized properly.
        if isinstance(data, IFDRational):
            data = float(data)

        image_metadata[tag] = data

    # Should this turn the data to json already?
    # Probably not..
    return image_metadata
