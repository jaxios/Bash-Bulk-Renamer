import datetime
import ffmpeg

def videoExif(file, data):
    """_summary_

    Args:
        file (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """

    videoExifData = ffmpeg.probe(file)
    exifDatetime = videoExifData.get("streams")[0].get("tags").get("creation_time") #dictionary>list>dictionary>dictionary
    exifDatetime = datetime.datetime.strptime(exifDatetime, "%Y-%m-%dT%H:%M:%S.000000Z")
    result = exifDatetime.strftime("%Y%m%d_%H%M%S")

    return result
