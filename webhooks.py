import requests #dependency
import json

url = "" #webhook url, from here: https://i.imgur.com/aT3AThK.png

data = {}
#for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
data["content"] = "https://www.youtube.com/watch?v=Tri2WUiDNbo"
data["username"] = "custom username"

# #leave this out if you dont want an embed
# data["embeds"] = []
# embed = {}
# #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
# embed["description"] = "https://www.youtube.com/watch?v=Tri2WUiDNbo"
# embed["title"] = "embed title"
# data["embeds"].append(embed)

result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))