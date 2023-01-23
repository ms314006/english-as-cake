from flask import Flask, request, abort
from bs4 import BeautifulSoup
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os #用來開檔案和曲環境變數
import random
import json
import requests

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


def randomGetWordQuest(intRan,userId,wordCount):
    jsonWord = ''
    with open('Data/word.json' , 'r') as reader:
        jsonWord = json.load(reader)
    strQuest = "單字：" + jsonWord["word"][intRan]["english"]
    arrAns = [jsonWord["word"][intRan]["chinese"]]

    while(len(arrAns)<4):
        strOption = jsonWord["word"][random.randint(0,wordCount)]["chinese"]
        if strOption in arrAns:
            continue
        arrAns.append(strOption)
    #亂數排列
    random.shuffle(arrAns)
    #選項
    arrItem = ['A','B','C','D']
    strAns = arrItem[arrAns.index(jsonWord["word"][intRan]["chinese"])]
    for i in range(4):
        strQuest += "\n(" + arrItem[i] + ") " + arrAns[i]

    jsonTest = ''
    with open('Data/test.json' , 'r') as reader:
        jsonTest = json.load(reader)
    with open("Data/test.json","w") as f:
        jsonTest[userId] = [strAns,"W"]
        json.dump(jsonTest, f)
    return strQuest

def randomGetTalkQuest(intRan,userId):
    jsonTalk = ''
    with open('Data/talk.json' , 'r') as reader:
        jsonTalk = json.load(reader)
    strQuest = "句型：\n" + jsonTalk["quest"][intRan]["title"]
    arrOption = jsonTalk["quest"][intRan]["options"]

    #亂數排列
    random.shuffle(arrOption)
    #選項
    arrItem = ['A','B','C','D']
    strAns = arrItem[arrOption.index(jsonTalk["quest"][intRan]["answer"])]
    for i in range(4):
        strQuest += "\n(" + arrItem[i] + ") " + arrOption[i]

    jsonTest = ''
    with open('Data/test.json' , 'r') as reader:
        jsonTest = json.load(reader)
    with open("Data/test.json","w") as f:
        jsonTest[userId] = [strAns,"T"]
        json.dump(jsonTest, f)
    return strQuest

def tk(a):
    # 獲取google翻譯內容的tk值
    # a：要翻譯的內容，以字符串指定
    # 注意：要翻譯的內容只能是英文，即只能是包含ASCII碼的英文本符串
    TKK = (lambda a=561666268, b=1526272306:str(406398) + '.' + str(a + b))()
    
    def b(a, b):
        for d in range(0, len(b)-2, 3):
            c = b[d + 2]
            c = ord(c[0]) - 87 if 'a' <= c else int(c)
            c = a >> c if '+' == b[d + 1] else a << c
            a = a + c & 4294967295 if '+' == b[d] else a ^ c
        return a
    
    e = TKK.split('.')
    h = int(e[0]) or 0
    g = []
    d = 0
    f = 0
    while f < len(a):
        c = ord(a[f])
        if 128 > c:        
            g.insert(d,c)
            d += 1
        else:
            if 2048 > c:
                g[d] = c >> 6 | 192
                d += 1
            else:
                if (55296 == (c & 64512)) and (f + 1 < len(a)) and (56320 == (ord(a[f+1]) & 64512)):
                    f += 1
                    c = 65536 + ((c & 1023) << 10) + (ord(a[f]) & 1023)
                    g[d] = c >> 18 | 240
                    d += 1
                    g[d] = c >> 12 & 63 | 128
                    d += 1
                else:
                    g[d] = c >> 12 | 224
                    d += 1
                    g[d] = c >> 6 & 63 | 128
                    d += 1
                g[d] = c & 63 | 128
                d += 1
        f += 1
    a = h
    for d in range(len(g)):
        a += g[d]
        a = b(a, '+-a^+6')
    a = b(a, '+-3^+b+-f')
    a ^= int(e[1]) or 0
    if 0 > a:a = (a & 2147483647) + 2147483648
    a %= 1E6
    return str(int(a)) + '.' + str(int(a) ^ h)



# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    userId = json.loads(request.get_data(as_text=True))["events"][0]["source"]["userId"]

    wordCount = 5999
    talkCount = 184

    if message == '來單字':
        intRan = random.randint(0,wordCount)
        jsonWord = ''
        with open('Data/word.json' , 'r') as reader:
            jsonWord = json.load(reader)
        strWord_e =  jsonWord["word"][intRan]["english"]
        strWord_c = jsonWord["word"][intRan]["chinese"]

        kk = jsonWord["word"][intRan]["kk"]
        if (kk == ""):
            kk = " "

        content = {"type": "bubble",
                    "styles": {
                        "body": {
                            "backgroundColor": "#ffffff"
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "單字：",
                                "size": "md",
                                "color": "#696969"
                            },
                            {
                                "type": "text",
                                "text":  strWord_e,
                                "size": "lg",
                                "weight": "bold",
                                "color": "#272727",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text":  kk,
                                "size": "md",
                                "color": "#ae0000",
                                "wrap": True
                            },
                            {
                                "type": "separator"
                            },
                            {
                                "type": "text",
                                "text": "意思：",
                                "size": "md",
                                "color": "#696969"
                            },
                            {
                                "type": "text",
                                "text": strWord_c,
                                "size": "md",
                                "color": "#272727",
                                "wrap": True
                            },
                            {
                                "type": "separator"
                            },
                            {
                                "type": "text",
                                "text": "例句：",
                                "size": "md",
                                "color": "#696969"
                            },
                        ]
                    }
                }

        sentence =  jsonWord["word"][intRan]["sentence"]
        if (len(sentence) == 0):
            content["body"]["contents"].append({"type":"text","text":"暫無資料","size": "md","color": "#272727"})
        else:
            content["body"]["contents"].append({"type":"text","text":sentence[0]["english"],"size": "md","color": "#00db00","wrap": True})
            content["body"]["contents"].append({"type":"text","text":sentence[0]["chinese"],"size": "md","color": "#272727","wrap": True})
            #content["body"]["contents"].append({"type":"text","text":" ","size": "md"})

        #content["body"]["contents"].append({"type": "button","style": "link","action": {"type": "uri","label": "詳細連結","uri": "https://www.en995.com/" + jsonWord["word"][intRan]["wordId"]}})

        headers = {"Content-Type":"application/json","Authorization": "Bearer 3Ma92PMIfy790ZdLw13WwBlKGvBSKfDYJmEoNajayWtzBks2klZeEtNCxeBwcNaXRk3OY47NiyBXVNhjqSx54pH2QP9hGmoZZoIUBlpcjHRPAFuEvl8wB00weGm265WtyP67xkyHMvq+4OGaEwy22wdB04t89/1O/w1cDnyilFU="}  
        data = '{"to": "' + userId + '","messages": [{ "type": "flex","altText": "' + strWord_e + '","contents":' + json.dumps(content) + '}]}'

        rex = requests.post("https://api.line.me/v2/bot/message/push", headers = headers,data = data)

    elif message == '單字':
        intRan = random.randint(0,wordCount)
        returnMessage = TextSendMessage(text=randomGetWordQuest(intRan,userId,wordCount))
        line_bot_api.reply_message(event.reply_token, returnMessage)

    elif message.upper() == 'A' or message.upper() == 'B' or message.upper() == 'C' or message.upper() == 'D':
        strStatus = ''
        #取目前測驗資料
        jsonTest = ''
        with open('Data/test.json' , 'r') as reader:
            jsonTest = json.load(reader)
        if jsonTest[userId][0] == '':
            strStatus = '還未有題目ㄛ！'
        elif message != jsonTest[userId][0]:
            strStatus = '登愣！答錯了！'
        else:
            strStatus = '沒錯！答對了！'
            tempJsonTest = jsonTest
            #查看模式
            jsonSet = ''
            with open('Data/setting.json' , 'r') as reader:
                jsonSet = json.load(reader)
            if userId in jsonSet and jsonSet[userId] == "Y":
                if tempJsonTest[userId][1] == "W":
                    intRan = random.randint(0,wordCount)
                    strStatus += "\n下一題" + randomGetWordQuest(intRan,userId,wordCount)
                elif tempJsonTest[userId][1] == "T":
                    intRan = random.randint(0,talkCount)
                    strStatus += "\n下一題" + randomGetTalkQuest(intRan,userId)
            else:
                with open("Data/test.json","w") as f:
                    tempJsonTest[userId][0] = ''
                    json.dump(tempJsonTest, f)

        returnMessage = TextSendMessage(text=strStatus)
        line_bot_api.reply_message(event.reply_token, returnMessage)
    elif message == '切換模式':
        strStatus = ''
        jsonSet = ''
        with open('Data/setting.json' , 'r') as reader:
            jsonSet = json.load(reader)

        if userId in jsonSet and jsonSet[userId] == "Y":
            jsonSet[userId] = "N"
            strStatus = '已關閉連續模式'
        else:
            jsonSet[userId] = "Y"
            strStatus = '已開啟連續模式'
        
        with open("Data/setting.json","w") as f:
            json.dump(jsonSet, f)

        returnMessage = TextSendMessage(text=strStatus)
        line_bot_api.reply_message(event.reply_token, returnMessage)

    elif message == '填空':
        intRan = random.randint(0,talkCount)
        returnMessage = TextSendMessage(text=randomGetTalkQuest(intRan,userId))
        line_bot_api.reply_message(event.reply_token, returnMessage)
        
    elif message == '切換翻譯語言':
        # translate.json
        strStatus = ''
        jsonSet = ''
        with open('Data/translate.json' , 'r') as reader:
            jsonSet = json.load(reader)

        if userId in jsonSet and jsonSet[userId] == "Y":
            jsonSet[userId] = "N"
            strStatus = '已切換中翻英模式'
        else:
            jsonSet[userId] = "Y"
            strStatus = '已切換為英翻中模式'
        
        with open("Data/translate.json","w") as f:
            json.dump(jsonSet, f)

        returnMessage = TextSendMessage(text=strStatus)
        line_bot_api.reply_message(event.reply_token, returnMessage)
    elif message == '測試' :
        intRan = random.randint(0,wordCount)
        
    else:

        def translate(word):
            url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
            key = {
                'type': "AUTO",
                'i': word,
                "doctype": "json",
                "version": "2.1",
                "keyfrom": "fanyi.web",
                "ue": "UTF-8",
                "action": "FY_BY_CLICKBUTTON",
                "typoResult": "true"
            }
            response = requests.post(url, data=key)
            if response.status_code == 200:
                return response.text
            else:
                return None

        #去除所有標點符號
        message = message.replace("‘","'").replace("’","'").replace("，",",").replace(". ",".")

        #查看模式
        jsonTranslate = ''
        with open('Data/translate.json' , 'r') as reader:
            jsonTranslate = json.load(reader)

        if userId in jsonTranslate and jsonTranslate[userId] == "Y":
            content_tk = tk(message)  # 獲取tk值
            content_url_template = 'https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl=zh-TW&hl=zh-TW&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&source=bh&ssel=0&tsel=0&kc=1&tk={tk}&q={q}'
            content_url = content_url_template.format(tk='{}'.format(content_tk),q='{}'.format(message))  # 根據待翻譯content和tk值拼湊URL
            response = requests.get(content_url)  # 根據URL獲取翻譯數據
            json_data = response.text
            data = json.loads(json_data)
            returnMessage = TextSendMessage(text=data[0][0][0])
            line_bot_api.reply_message(event.reply_token, returnMessage)

        while(message.replace(' ','').encode('UTF-8').isalpha() == False):
            message = json.loads(translate(message))['translateResult'][0][0]['tgt']
        returnMessage = TextSendMessage(text=message)
        line_bot_api.reply_message(event.reply_token, returnMessage)
        

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
