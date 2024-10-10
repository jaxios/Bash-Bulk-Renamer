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

    result = subprocess.run(
        ['exiftool', '-api', 'QuickTimeUTC', file],
        capture_output=True,
        text=True,
        check=True
    )

    mediafile_exif = result.stdout

    result = "No EXIF data"

    if data == "datetime":
        for line in mediafile_exif.splitlines():
            for tag in DATETIME_TAGS:
                if tag in line:
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
                if tag in line:
                    value = re.sub(r'^.*?: ', '', line)
                    result = shortNames.transform_device_name(value)
                    break
                    

    return result