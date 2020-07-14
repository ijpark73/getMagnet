import requests, json, sys, os
from bs4 import BeautifulSoup

class JsonParser:
    def __init__(self, setfileName):
        self.JsonFile = setfileName
        try:
            dataFile = open(self.JsonFile, 'r', encoding='utf-8')
        except FileNotFoundError as e:
            print(str(e))
            print("Please set your file path.")
            sys.exit()
        else:
            self.data = json.load(dataFile)
            dataFile.close()

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        with open(self.JsonFile, 'w', encoding='utf-8') as dataFile:
            self.data[key] = value
            json.dump(self.data, dataFile, sort_keys=True, ensure_ascii=False, indent=4)

def getBsObj(addr):
    s = requests.Session()
    return BeautifulSoup(s.get(addr).content, 'html.parser')

def checkUrl(addr):
    try:
        getBsObj(addr)
    except Exception as e:
        print("Exception access url: %s" % e)
        print("Can't access %s, someting wrong.\n" % addr)
        return False
    return True

def getTqqUrl(addr):
    if checkUrl(addr):
        aTags = getBsObj(addr).select("div[class='ex-page-content text-center']>a")
        return aTags[0].get("href")
    else:
        return None

def ttobogo():
    JD = JsonParser("./setting.json")
    history = []
    lastId = JD.get("ttobogoLastId")
    start_Url = getTqqUrl(JD.get("ttobogoStartUrl"))
    board_Url = start_Url + "board/torrent_ent/"

    print("start_Url %s\nboard_Url %s"%(start_Url,board_Url))

    aTags = getBsObj(board_Url).select("div[class='wr-subject']>a")
    JD.set("ttobogoLastId", aTags[0].get('href').strip().replace(start_Url + "post/", ""))

    for aTag in aTags:
        itemUrl = aTag.get("href")
        itemId = aTag.get("href").strip().replace(start_Url + "post/", "")
        itemTitle = aTag.text.strip()
        if int(itemId) < int(lastId):
            print("Nothing to be downloaded from Bogobogonet.")
            break
        else:
            for keyword in JD.get("keywords"):
                if keyword in itemTitle:
                    if not keyword in history:  # already download?
                        tag = getBsObj(itemUrl).find_all("a", class_="btn btn-blue")

                        if len(tag[0]) > 0:
                            history.append(keyword)
                            magnet = tag[0].get('onclick').replace("file_download('", "").replace("')", "")
                            print(itemTitle, "[ttobogo] transmission-remote 9091 --add " + magnet)
                            os.system("transmission-remote 172.30.1.58:9091 --auth admin:Wkddudqls2! --add " + magnet)
    del history
    sys.exit()

def torrentmax():
    JD = JsonParser("./setting.json")
    history = []
    lastId = JD.get("torrentmaxLastId")
    start_Url = JD.get("torrentmaxStartUrl")
    board_Url = start_Url + "max/VARIETY"

#    print("start_Url %s\nboard_Url %s"%(start_Url,board_Url))

    aTags = getBsObj(board_Url).select("div[class='wr-subject']>a")
    JD.set("torrentmaxLastId", aTags[0].get('href').strip().replace(board_Url+"/", ""))

    for aTag in aTags:
        itemUrl = aTag.get("href")
        itemId = aTag.get("href").strip().replace(board_Url+"/", "")
        itemTitle = aTag.text.strip()
        if int(itemId) < int(lastId):
            print("Nothing to be downloaded from torrentmax.")
            break
        else:
            for keyword in JD.get("keywords"):
                if keyword in itemTitle:
                    if not keyword in history:  # already download?
                        tag = getBsObj(itemUrl).select("li[class='list-group-item en font-14 break-word']>a")

                        if len(tag[0]) > 0:
                            history.append(keyword)
                            magnet = tag[0].get('href')
                            print(itemTitle, "[torrentmax] transmission-remote 9091 --add " + magnet)
                            os.system("transmission-remote 172.30.1.58:9091 --auth admin:Wkddudqls2! --add " + magnet)
    del history
    sys.exit()

if __name__ == "__main__":
#  ttobogo()
  torrentmax()
