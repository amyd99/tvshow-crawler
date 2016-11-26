import sys
import http.client

from pathlib import Path
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.found = False
        self.tv_list = []

    def handle_starttag(self, tag, attrs):
        if tag != "input":
            return
        for attr in attrs:
            if len(attr) != 2:
                continue
            if attr[0] == "class" and attr[1] == "down_url":
                self.found = True
            if attr[0] == "value":
                url = attr[1]
            if attr[0] == "file_name":
                name = attr[1]
        if self.found:
            self.found = False
            self.tv_list.append({"url": url, "name": name})

    def output_rss(self, flist):
        for tv in self.tv_list:
            if tv["name"] not in flist:
                print(tv["url"])

def parse(tv, conn):
    #print("parse", url, file=sys.stderr)
    print("")
    print(tv["folder"].replace("/", "\\"))
    conn.request("GET", tv["url"])
    r = conn.getresponse()
    if r.status == 200:
        parser = MyHTMLParser()
        parser.feed(str(r.read(), "gbk"))
        flist = [ p.name for p in Path("D:/Media/TV Shows/" + tv["folder"]).iterdir() ]
        parser.output_rss(flist)


tv_dict = [
        {"url": "/content/meiju22476.html", "folder": "The Walking Dead/Season 07"},
        {"url": "/content/meiju22422.html", "folder": "Criminal Minds/Season 12"}
        ]

conn = http.client.HTTPConnection("www.meijutt.com")

for tv in tv_dict:
    parse(tv, conn)
