import configparser
import googleapiclient.discovery

class YoutubeConfig:
    api_service_name = "youtube"
    api_version = "v3"
    dbPath = "/config/youtube.db"
    configPath = "/config/youtube.ini"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.configPath)
        self.DEVELOPER_KEY = self.config["youtube"]["key"]
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name,
            self.api_version,
            developerKey=self.DEVELOPER_KEY
        )