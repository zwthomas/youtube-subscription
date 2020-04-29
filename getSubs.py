from bs4 import BeautifulSoup

fh = open("subs.html", "r")

contents = fh.read()
soup = BeautifulSoup(contents, 'html')

allSubs = soup.find_all("ytd-guide-entry-renderer")
for sub in allSubs:
    subAttributes = sub.a.attrs
    try: 
        print (subAttributes["title"] + " " + subAttributes["href"])
    except:
        print(subAttributes)

# print(soup.find_all("ytd-guide-entry-renderer")[1].a.attrs["title"])