from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from googletrans import Translator

app = Flask(__name__)

# ここに LINE Developers で取得したチャネルアクセストークンとチャネルシークレットを入れる
LINE_CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"
LINE_CHANNEL_SECRET = "YOUR_CHANNEL_SECRET"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

translator = Translator()

# 言語コードの対応
LANG_MAP = {
    "JP": "ja",
    "EN": "en",
    "VN": "vi",
    "KR": "ko",
    "CN": "zh-cn"
}


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("Error:", e)

    return "OK"


@handler.add(event=WebhookHandler)
def handle_message(event):
    text = event.message.text.strip()
    
    if " " not in text:
        reply = "This language is not supported."
    else:
        code, message = text.split(" ", 1)
        code = code.upper()

        if code not in LANG_MAP:
            reply = "This language is not supported."
        else:
            target_lang = LANG_MAP[code]
            translated = translator.translate(message, dest=target_lang)
            reply = translated.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )


if __name__ == "__main__":
    app.run()
