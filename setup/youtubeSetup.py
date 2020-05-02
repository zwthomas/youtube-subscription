import os
import sqlite3
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import configparser


class YoutubeSetup():

    api_service_name = "youtube"
    api_version = "v3"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("../youtube.ini")
        self.DEVELOPER_KEY = self.config["youtube"]["key"]
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name,
            self.api_version,
            developerKey=self.DEVELOPER_KEY
        )

    def getAllSubs(self):
        subs = {}
        nextPageToken = ""

        while nextPageToken != None:
            response = self.youtube.subscriptions().list(
                part="snippet,contentDetails",
                channelId=self.config["youtube"]["yourChannel"],
                maxResults=50,
                pageToken=nextPageToken
            ).execute()

            for item in response["items"]:
                channelId = item["snippet"]["resourceId"]["channelId"]
                channelName = item["snippet"]["title"]
                subs[channelId] = channelName

            if "nextPageToken" in response.keys():
                nextPageToken = response["nextPageToken"]
            else:
                nextPageToken = None
        return subs

    def createDatabase(self, subs):
        conn = sqlite3.connect("youtube.db")
        c = conn.cursor()
        c.execute("CREATE TABLE subs ( `channelId` TEXT, `channelName` TEXT, `category` TEXT, `mostRecentId` TEXT, PRIMARY KEY(`channelId`) )")
        for subId in subs:
            c.execute(
                "INSERT INTO subs (channelId, channelName) VALUES (?, ?)", (subId, subs[subId]))
        conn.commit()
        conn.close()

    def fillMostRecentVids(self, allSubs):
        conn = sqlite3.connect('youtube.db')
        c = conn.cursor()

        for sub in allSubs:
            request = self.youtube.activities().list(
                part="snippet,contentDetails",
                channelId=sub,
                maxResults=5
            )
            response = request.execute()
            print(allSubs[sub])
            videos = [item["contentDetails"]["upload"]["videoId"]
                    for item in response["items"] if "upload" in item["contentDetails"].keys()]
            if len(videos) == 0:
                continue
            newestVideo = videos[0]
            c.execute("UPDATE subs SET mostRecentId=? WHERE channelId=?",
                    (newestVideo, sub))

        conn.commit()
        conn.close()
    
    def setup(self):
        subs = self.getAllSubs()
        self.createDatabase(subs)
        self.fillMostRecentVids(subs)


if __name__ == "__main__":
    ytSetup = YoutubeSetup()
    ytSetup.setup()