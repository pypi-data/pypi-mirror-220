from datetime import datetime
from agora_utils import AgoraTimeStamp

class MediaData:
    mediaData_id = -1

    def __init__(self):
        self.Type = ""            
        if MediaData.mediaData_id == -1:
            MediaData.mediaData_id = self.__get_mediadata_id()
        MediaData.Id = MediaData.mediaData_id + 1
        self.Id = MediaData.mediaData_id
        self.ZoneId = ""
        self.CameraId = ""
        self.MotTrackerId = None
        self.EdgeFilename = ""
        self.MotEdgeFilename = ""
        self.MIMEType = ""
        self.AltText = ""
        self.DetectedStart_tm = 0
        self.DetectedEnd_tm = 0

    def __get_mediadata_id(self):
        utcnow = datetime.utcnow()
        beginning_of_year = datetime(utcnow.year, 1, 1)
        time_difference = utcnow - beginning_of_year
        return int(time_difference.total_seconds()*10)