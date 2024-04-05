
# 載入 json 標準函式庫，處理回傳的資料格式
import json
import base64
import hashlib
import hmac

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = '815b56b77f9912b9f89952f78712bd03'
        secret = 'FcNkcsTOvJhqbgHlwnUwUPerNwcmGs+mZHCYo0nMYOoqrIAS+v8y05vtRcGe+PQ76XrF/K/D90VI5TqT2KX4kxCedqN6qel9I7/3Sg2p4CM7fSZSXFeYo9Mun7t5d/8Yi6iWQ8t2l+qDQLkBpQRCqAdB04t89/1O/w1cDnyilFU='
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                    # 確認 secret 是否正確
        print('test1')
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")

        except Exception as e:
            print(f"An error occurred: {e}")
        # handler.handle(body, signature)                     # 綁定訊息回傳的相關資訊
        print('test2')
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            # print(msg)                                       # 印出內容
            reply = msg
        else:
            reply = '你傳的不是文字呦～'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
    except:
        print('except啦：')
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    app.run(port=5002)