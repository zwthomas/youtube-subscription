import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import configparser

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
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

    subs = {}
    nextPageToken = ""

    while nextPageToken != None:
        response = youtube.subscriptions().list(
            part="snippet,contentDetails",
            channelId=config["youtube"]["yourChannel"],
            maxResults=50,
            pageToken=nextPageToken
        ).execute()

        for item in response["items"]:
            channelId = item["snippet"]["resourceId"]["channelId"]
            channelName = item["snippet"]["title"]
            print(channelId)
            subs[channelId] = channelName

        if "nextPageToken" in response.keys():
            nextPageToken = response["nextPageToken"]
        else: 
            nextPageToken = None
    
    print(subs)


if __name__ == "__main__":
    main()
