import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import configparser

config = configparser.ConfigParser()
config.read("youtube.ini")

DEVELOPER_KEY = config["youtube"]["key"]
api_service_name = "youtube"
api_version = "v3"


youtube = googleapiclient.discovery.build(
    api_service_name,
    api_version,
    developerKey=DEVELOPER_KEY
)

search_response = youtube.search().list(
    q="Hello",
    part="id,snippet",
    maxResults=5
).execute()

print(search_response.get("items",[]))