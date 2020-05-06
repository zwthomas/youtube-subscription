import google_auth_oauthlib.flow
import googleapiclient.errors
import sqlite3
import requests
import json
from youtubeConfig import YoutubeConfig
import time

class Youtube(YoutubeConfig):

    def getChannelsAndMostRecent(self):
        conn = sqlite3.connect(self.dbPath)
        c = conn.cursor()
        c.execute("SELECT channelId, mostRecentId FROM subs")

        subInfo = {sub[0]: sub[1] for sub in c.fetchall()}

        conn.commit()
        conn.close()

        return subInfo

    def getNewVideosForSub(self, channelId, recentVideo):
        request = self.youtube.activities().list(
            part="snippet,contentDetails",
            channelId=channelId,
            maxResults=10
        )

        response = request.execute()
        newVideos = []
        for item in response["items"]:
            contentDetails = item["contentDetails"]
            if "upload" in contentDetails.keys():
                videoId = contentDetails["upload"]["videoId"]
                if videoId != recentVideo:
                    newVideos.append(videoId)
                else:
                    return newVideos
        return newVideos


    def postInDiscord(self, newVideos, channelId):
        self.updateMostRecent(newVideos[0], channelId)

        conn = sqlite3.connect(self.dbPath)
        c = conn.cursor()

        c.execute("SELECT category FROM subs WHERE channelId=?", (channelId,))
        category = c.fetchone()
        if len(category[0]) == 0: return
        url = self.config["youtube"][category[0]]

        for video in newVideos[::-1]:
            data = {}
            data["content"] = "https://www.youtube.com/watch?v=" + video
            data["username"] = "YoutubeBot"

            result = requests.post(url, data=json.dumps(data), headers={
                                "Content-Type": "application/json"})
        
        conn.commit()
        conn.close()
    
    def updateMostRecent(self, newVideo, channelId):
        conn = sqlite3.connect(self.dbPath)
        c = conn.cursor()

        c.execute("UPDATE subs SET mostRecentId=? WHERE channelId=?", (newVideo, channelId))

        conn.commit()
        conn.close()
        
    
    def run(self):
        while True:
            subInfo = self.getChannelsAndMostRecent()
            for sub in subInfo:
                newVideos = self.getNewVideosForSub(sub, subInfo[sub])
                if len(newVideos) > 0:
                    self.postInDiscord(newVideos, sub)
            time.sleep(14400) # Run once every four hours hopefully a better solution to come


if __name__ == "__main__":
    yt = Youtube()
    yt.run()