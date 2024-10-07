import datetime
import subprocess

def videoExif(file, data):

    mediafile_exif = subprocess.run(['exiftool', file], stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    for key, val in mediafile_exif.items():
        if key == "Media Create Date":
            exifDatetime = val
            exifDatetime = datetime.datetime.strptime(exifDatetime, "%Y:%m:%d %H:%M:%S")
            exifDatetime = exifDatetime.strftime("%Y%m%d_%H%M%S")
            result = exifDatetime
        elif data == "Author":
            exif_device = val
            result = exif_device

    return result
