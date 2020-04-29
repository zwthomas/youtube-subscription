import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import configparser


config = configparser.ConfigParser()
config.read("youtube.ini")
url = config["youtube"]["tech"]

DEVELOPER_KEY = config["youtube"]["key"]
api_service_name = "youtube"
api_version = "v3"


youtube = googleapiclient.discovery.build(
    api_service_name,
    api_version,
    developerKey=DEVELOPER_KEY
)

request = youtube.activities().list(
    part="snippet,contentDetails",
    channelId="UCXuqSBlHAE6Xw-yeJA0Tunw",
    maxResults=10
)
response = request.execute()

# print(type(response))
# print(response.keys())
# print(type(response["items"]))

data = {}
data["content"] = "https://www.youtube.com/watch?v=" + str(response["items"][0]["contentDetails"]["upload"]["videoId"])
data["username"] = "custom username"

print(data["content"])
# result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

# for item in response["items"]:
#     # print(type(item))
#     # print(item.keys())
#     # print(item["snippet"].keys())
#     try:
#         print(str(item["contentDetails"]["upload"]["videoId"]) + " - " + item["snippet"]["title"])
#     except:
#         print("skip")

# request = youtube.activities().list(
#     part="snippet,contentDetails",
#     channelId="UCXuqSBlHAE6Xw-yeJA0Tunw",
#     maxResults=5
# )
# response = request.execute()

# print(response)

# request = youtube.channels().list(
#     part="snippet,contentDetails,statistics",
#     id="UCXuqSBlHAE6Xw-yeJA0Tunw"
# )

# response = request.execute()
# print(response)

# search_response = youtube.search().list(
#     q="LinusTechTips",
#     part="id,snippet",
#     maxResults=5
# ).execute()

# print(search_response.get("items",[]))