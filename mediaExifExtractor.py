import datetime
import subprocess
import re
import shortNames

TARGET_PATH = "/mnt/c/Users/giuseppe.storti/Formazione/Bash Bulk Renamer/test/[01] foto lavoro - io - anno 2024/"
DATETIME_TAGS = ["Date/Time Original", "Media Create Date"]
DEVICE_TAGS = ["Camera Model Name", "Author"]

def getExifData(file,data):

    mediafile_exif = subprocess.run(['exiftool -api QuickTimeUTC', file], stdout=subprocess.PIPE).stdout.decode('utf-8') #-api QuickTimeUTC converts datetimes from UTC to local

    result = "No EXIF data"

    if data == "datetime":
        for line in mediafile_exif.splitlines():
            for tag in DATETIME_TAGS:
                if tag in line:
                    value = re.sub(r'^.*?: ', '', line)
                    value = value.split(".", 1)[0]
                    value = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    value = value.strftime("%Y%m%d_%H%M%S")
                    result = value
                    break
                
    elif data == "device":
        for tag in DEVICE_TAGS:
            for line in mediafile_exif.splitlines():
                if tag in line:
                    value = re.sub(r'^.*?: ', '', line)
                    result = shortNames.transform_device_name(value)
                    break
                    

    return result