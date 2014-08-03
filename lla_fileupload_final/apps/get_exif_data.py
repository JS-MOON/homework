from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(filename):
    fileinfo = {}
    try:
        img = Image.open(filename)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            print exifinfo
            if exifinfo != None:
                fileinfo = dict([(TAGS.get(key,key), str(value).decode('utf-8', 'ignore'))
                        for key, value in exifinfo.items()
                        if type(TAGS.get(key,key)) is str])
    except IOError:
        logging.error(filename)
    return fileinfo