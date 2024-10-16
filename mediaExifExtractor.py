import datetime
import subprocess
import re
import shortNames

TARGET_PATH = "/mnt/c/Users/giuseppe.storti/Formazione/Bash Bulk Renamer/test/[01] foto lavoro - io - anno 2024/"
DATETIME_TAGS = ["Date/Time Original", "Media Create Date"]
DEVICE_TAGS = ["Camera Model Name", "Author"]

def get_exif_data(file,data,date_format):
    """Returns requested EXIF data if available

    Args:
        file (str): Target file
        data (str): datetime or device
        date_format (str): argument for strftime()

    Returns:
        str: EXIF value
    """

    exiftool_out = subprocess.run(
        ['exiftool', file],
        capture_output=True,
        text=True,
        check=True
    )

    exiftool_out_utc = subprocess.run(
            ['exiftool', '-api', 'QuickTimeUTC', file],
            capture_output=True,
            text=True,
            check=True
            )

    exiftool_out = exiftool_out.stdout

    # depending on brand, EXIF tags contain the Timezone

    if "HERO" or "GoPro" in exiftool_out: # GoPro
        mediafile_exif = exiftool_out
    elif "Galaxy" or "Samsung" in exiftool_out:
        if "File Type                       : MP4" in exiftool_out: # Samsung video
            mediafile_exif = exiftool_out_utc.stdout
        else: #samsung photo
            mediafile_exif = exiftool_out
    else: # other
        mediafile_exif = exiftool_out_utc.stdout

    result = "No EXIF data"

    if data == "datetime":
        for line in mediafile_exif.splitlines():
            for tag in DATETIME_TAGS:
                if tag in line:

                    if "0000:00:00 00:00:00" in line or "1904:01:01" in line:
                        result = "Invalid EXIF data"
                        break

                    value = re.sub(r'^.*?: ', '', line)
                    value = value.split(".", 1)[0]
                    value = value.split("+", 1)[0]
                    value = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    value = value.strftime(date_format)
                    result = value
                    break
                
    elif data == "device":
        for tag in DEVICE_TAGS:
            for line in mediafile_exif.splitlines():

                #if "Apple" in line:
                    #result = "iPhone"
                    #break
                if tag in line:
                    value = re.sub(r'^.*?: ', '', line)
                    result = shortNames.transform_device_name(value)
                    break
                    

    return result