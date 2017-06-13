import requests
from bs4 import BeautifulSoup
import json

def fetchData(page=0):
    print("loading page "+str(page))
    payload = {
        "reviewType": 1,
        "pageNum": page,
        "id": "tw.com.twmp.twhcewallet",
        "reviewSortOrder": 2,
        "xhr": 1
    }

    r = requests.post("https://play.google.com/store/getreviews", data=payload)

    return r.text

def parseData(page=0):
    fetchContent = fetchData(page)
    jsonContent = fetchContent.split("\n")[2] + "]"
    jsonObject = json.loads(jsonContent)[0]


    if len(jsonObject) == 2:
        print("out of comment range")
        return False
    # print(jsonContent)
    # print(htmlContent)

    htmlContent = jsonObject[2]
    if htmlContent == "":
        print("no comments")
        return False


    commentGroup = []
    spliter = '<div class="single-review"'
    for html in htmlContent.split(spliter):
        if html != " " and html != "":
            commentGroup.append(spliter + html)


    soup = BeautifulSoup(htmlContent, "html5lib")

    for comment in commentGroup:
        soup = BeautifulSoup(comment)
        header = soup.find('div',{"class": "single-review"})
        comment_user = header.find("span",{"class": "author-name"}).text.replace(" ","")
        comment_date = header.find("span",{"class": "review-date"}).text.replace(" ","")

        body = soup.find("div", {"class": "review-body"})
        print(body.text)

        reply = soup.find("div",{"class": "developer-reply"})
        if reply != None:
            None
            # print(reply.text)

    if len(commentGroup) == 40:
        print("full 40 comments")
    else:
        print("not all comment")


parseData(1)