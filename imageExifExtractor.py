import datetime
from PIL import Image, ExifTags

def imageExif(file, data):
    """_summary_

    Args:
        file (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    mediafile = Image.open(file)
    mediafile_exif = mediafile.getexif()
    
    if not mediafile_exif:
        print('Sorry, image %s has no exif data.' % (file))
        result = "No EXIF data"
    else:
        for key, val in mediafile_exif.items():
            if key in ExifTags.TAGS:
                if data in f'{ExifTags.TAGS[key]}:{val}':
                    if data == "DateTime":
                        exifDatetime = val
                        exifDatetime = datetime.datetime.strptime(exifDatetime, "%Y:%m:%d %H:%M:%S")
                        exifDatetime = exifDatetime.strftime("%Y%m%d_%H%M%S")
                        result = exifDatetime
                    elif data == "Model":
                        exif_device = val
                        result = exif_device
            #else:
                #exif_infos.add(f'{key}:{val}')
    return result
