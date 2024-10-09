import os
import datetime
import subprocess
import re

TARGET_PATH = "/mnt/c/Users/giuseppe.storti/Formazione/Bash Bulk Renamer/test/[01] foto lavoro - io - anno 2024/"
DATETIME_TAGS = ["Date/Time Original", "Media Create Date"]
DEVICE_TAGS = ["Camera Model Name", "Author"]

def getExifData(file,data):

    mediafile_exif = subprocess.run(['exiftool', file], stdout=subprocess.PIPE).stdout.decode('utf-8')

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
                    result = value
                    break
                    

    return result

####################################################################################################################################

valid_formats = [".jpg",".mp4",".jpeg"]
original_files = []
for f in os.listdir(TARGET_PATH):
    ext = os.path.splitext(f)[1]
    if (os.path.isfile(TARGET_PATH + f) and ext.lower() in valid_formats):
        original_files.append(f)

for target_file in original_files:
    print(getExifData(TARGET_PATH+target_file,"datetime"))