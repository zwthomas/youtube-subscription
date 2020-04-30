import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import configparser
import sqlite3
import requests
import json


config = configparser.ConfigParser()
config.read("youtube.ini")
TECH = config["youtube"]["tech"]

DEVELOPER_KEY = config["youtube"]["key"]
api_service_name = "youtube"
api_version = "v3"
channelId = "UCXuqSBlHAE6Xw-yeJA0Tunw"


def getAllChannels():
    conn = sqlite3.connect('youtube.db')
    c = conn.cursor()

    c.execute("SELECT channelId FROM subs")
    allSubs = [sub[0] for sub in c.fetchall()]

    conn.commit()
    conn.close()

    return allSubs


def getChannelsAndMostRecent():
    conn = sqlite3.connect("youtube.db")
    c = conn.cursor()
    c.execute("SELECT channelId, mostRecentId FROM subs")

    subInfo = {sub[0]: sub[1] for sub in c.fetchall()}

    conn.commit()
    conn.close()

    return subInfo


def fillMostRecentVids(allSubs):
    conn = sqlite3.connect('youtube.db')
    c = conn.cursor()

    for sub in allSubs:
        request = youtube.activities().list(
            part="snippet,contentDetails",
            channelId=sub,
            maxResults=5
        )
        response = request.execute()
        print(sub)
        videos = [item["contentDetails"]["upload"]["videoId"]
                  for item in response["items"] if "upload" in item["contentDetails"].keys()]
        if len(videos) == 0:
            continue
        newestVideo = videos[0]
        c.execute("UPDATE subs SET mostRecentId=? WHERE channelId=?",
                  (newestVideo, sub))

    conn.commit()
    conn.close()


def getNewVideosForSub(channelId, recentVideo):
    request = youtube.activities().list(
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


def postInDiscord(newVideos, channelId):
    conn = sqlite3.connect("youtube.db")
    c = conn.cursor()

    c.execute("SELECT category FROM subs WHERE channelId=?", (channelId,))
    category = c.fetchone()
    if len(category[0]) == 0: return
    url = config["youtube"][category[0]]

    for video in newVideos:
        data = {}
        data["content"] = "https://www.youtube.com/watch?v=" + video
        data["username"] = "custom username"

        result = requests.post(url, data=json.dumps(data), headers={
                               "Content-Type": "application/json"})


youtube = googleapiclient.discovery.build(
    api_service_name,
    api_version,
    developerKey=DEVELOPER_KEY
)

request = youtube.activities().list(
    part="snippet,contentDetails",
    channelId=channelId,
    maxResults=10
)
response = request.execute()

subInfo = getChannelsAndMostRecent()
for sub in subInfo:
    newVideos = getNewVideosForSub(sub, subInfo[sub])
    if len(newVideos) > 0:
        postInDiscord(newVideos, sub)



# print(type(response))
# print(response.keys())
# print(type(response["items"]))

# data = {}
# data["content"] = "https://www.youtube.com/watch?v=" + str(response["items"][0]["contentDetails"]["upload"]["videoId"])
# data["username"] = "custom username"

# print(data["content"])
# result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

# conn = sqlite3.connect('youtube.db')
# c = conn.cursor()
# # c.execute("SELECT mostRecentId FROM subs WHERE channelId = ?", (channelId,))
# c.execute("SELECT * FROM subs")
# allSubs = c.fetchall()
# subDict = {sub[0]:sub[3] for sub in allSubs}
# print(subDict)
# for sub in allSubs:
#     print(sub[0] + " " + sub[3])

# mostRecentId = c.fetchone()[0]


# for item in response["items"]:
#     # print(type(item))
#     # print(item.keys())
#     # print(item["snippet"].keys())
#     contentDetails = item["contentDetails"]
#     if "upload" in contentDetails.keys():
#         videoId = contentDetails["upload"]["videoId"]
#         if videoId != mostRecentId:
#             print(videoId)
#         else:
#             break
#         # print(videoId)
#         # print(str(item["contentDetails"]["upload"]["videoId"]) + " - " + item["snippet"]["title"])


#     # try:
#     #     print(str(item["contentDetails"]["upload"]["videoId"]) + " - " + item["snippet"]["title"])
#     # except:
#     #     print("skip")
