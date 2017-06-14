import requests
from bs4 import BeautifulSoup
import json
from sys import argv

def fetchData(appname,page=0):
    print("loading page "+str(page))
    payload = {
        "reviewType": 1,
        "pageNum": page,
        "id": appname,
        "reviewSortOrder": 2,
        "xhr": 1
    }

    r = requests.post("https://play.google.com/store/getreviews", data=payload)

    return r.text

def parseData(appname,page=0, exist_array=[]):
    fetchContent = fetchData(appname,page)
    jsonContent = fetchContent.split("\n")[2] + "]"
    jsonObject = json.loads(jsonContent)[0]


    if len(jsonObject) == 2:
        print("out of comment range")
        # return False
        return exist_array
    # print(jsonContent)
    # print(htmlContent)

    htmlContent = jsonObject[2]
    if htmlContent == "":
        print("no comments")
        return exist_array
        # return False

    commentGroup = []
    spliter = '<div class="single-review"'
    for html in htmlContent.split(spliter):
        if html != " " and html != "":
            commentGroup.append(spliter + html)


    soup = BeautifulSoup(htmlContent, "html5lib")

    for comment in commentGroup:
        soup = BeautifulSoup(comment, 'html5lib')
        header = soup.find('div',{"class": "single-review"})
        comment_star = int(soup.find('div',{"class": "tiny-star"}).attrs["aria-label"].split(" ")[1])

        comment_user = header.find("span",{"class": "author-name"}).text.replace(" ","")
        comment_date = header.find("span",{"class": "review-date"}).text.replace(" ","")
        
        comment_content = soup.find('div',{"class": "review-body"}).contents[2]

        body = soup.find("div", {"class": "review-body"})
        # print(body.text)

        reply = soup.find("div",{"class": "developer-reply"})
        comment_reply = None
        if reply != None:
            comment_reply = reply.text
            # print(reply.text)

        exist_array.append({
            "user": comment_user,
            "date": comment_date,
            "star": comment_star,
            "content": comment_content,
            "dev-replay": comment_reply
        })

    if len(commentGroup) == 40:
        return parseData(appname,page+1,exist_array)
        # return exist_array
        # print("full 40 comments")
    else:
        # print("not all comment")
        return exist_array


if len(argv)<1:
    print("no application name !!")
    exit(3)

appname = argv[1]

print("fetch: "+appname)
data = parseData(appname)

outputfile = open(appname+".json", "w")
outputfile.writelines(json.dumps(data))
outputfile.close()


print("end")