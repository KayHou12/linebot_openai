#建立linebot訊息功能

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======載入程式碼==========
import tempfile, os
import datetime
import time
import traceback
from stock_info import stock_id
from weather import ask_weather
from stock_notify import *
from date import latestdate
from watchlist import *

#======建立linebot==========
app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

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
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
# re.match 的作用就是判斷文字是否一樣
import re
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text = event.message.text
    if re.match("你是誰",message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage("才不告訴你勒~~"))
    elif "個股資訊" in message:
        stock_n = stock_id(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(stock_n)])
    elif "天氣" in message:
        weather_feedback = ask_weather()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(weather_feedback))
    elif "關注清單" in message:
        watch_list_data = watch_list()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(watch_list_data))
    elif "最新日期" in message:
        latest_date = latestdate()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(str(latest_date)))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message))

#環境
import os
if __name__ == "__main__":    
    port = int(os.environ.get('PORT', 5000))     
    app.run(host='0.0.0.0', port=port) 
    