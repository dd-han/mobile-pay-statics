from sys import argv
import json
import re

if len(argv)<=1: 
    print("no json file input !!")
    exit(3)

rules = {
    "銀行不支援、儲值不方便":  [
        {
            "sure-first": ["銀行","郵局","卡","華南","中信","國泰","世華","花旗","富邦","台銀","第一","合庫","彰化","高雄","兆豐"],
            "sure-second": ["只開放","太少","只有","早日","無法","不支援","未","希望","可以","能有"],
            "exclude": None,
        }
    ],
    "店家不支援":  [
        {
            "sure-first": ["廠商","商家","水費","瓦斯","7-11","711","小七","全家","OK","萊爾富","餐廳","超市"],
            "sure-second": ["只開放","何時","那時","哪時","啥時","什麼時候","不能","不支援","不","如果能","本.*信用卡","本.*悠遊卡"],
            "exclude": None,
        }
    ],
    "使用上不方便":  [
        {
            "sure-first": ["[很超]慢","非常慢","要等","效能[差慢不]","繁瑣","不方便","不直覺","很卡","閃退","軟體維修","維護","會更快"],
            "sure-second": None,
            "exclude": None,
        },
        {
            "sure-first": ["開啟","執行","指紋","對焦","條碼","掃描","推撥"],
            "sure-second": ["不行","不出來","出不來","不支援","無法","難辨識","難成功","希望"],
            "exclude": None,
        },
        {
            "sure-first": ["希望","如果","若能","能","可以"],
            "sure-second": ["增加","支援","可以","能"],
            "exclude":  ["銀行","郵局","卡"],
        }
    ],
    "盜刷與身分問題":  [

    ]
}

def filter(comment_content):
    result = {}
    for key, value in rules.items():
        result[key] = None
    
    for key_rule, value_rule in rules.items():
        for condition in rules[key_rule]:
            if result[key_rule] == True:
                continue

            print(condition)
            # result[key_rule] = True

    return result

jsonfile = argv[1]

jsonfileobject = open(jsonfile,'r')
data = json.loads(jsonfileobject.readline())

for comment in data: 
    print("====================================")
    print(comment["star"])
    print(comment["content"])
    print(filter(comment["content"]))
    break
    print("====================================")


print("Enter 結束他")
a = input()