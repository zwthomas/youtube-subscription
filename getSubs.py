from bs4 import BeautifulSoup
import sqlite3

fh = open("subs.html", "r")

contents = fh.read()
soup = BeautifulSoup(contents, 'html.parser')

allSubs = soup.find_all("ytd-guide-entry-renderer")

conn = sqlite3.connect('youtube.db')
c = conn.cursor()
youtubeSubs = {}
for sub in allSubs:
    subAttributes = sub.a.attrs
    if "href" in subAttributes and "channel" in subAttributes["href"]:
        channelTitle = subAttributes["title"]
        channelId = subAttributes["href"].split("/")[-1] # /channel/UCiqnRXPAAk6iv2m47odUFzw
        youtubeSubs[channelId] = channelTitle
        
        # print (subAttributes["title"] + " " + subAttributes["href"])

# print(soup.find_all("ytd-guide-entry-renderer")[1].a.attrs["title"])
for channelId in youtubeSubs:
    c.execute("INSERT INTO subs VALUES (?, ?, ?, ?)", (channelId, youtubeSubs[channelId], "", ""))

conn.commit()
conn.close()