import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BALE_TOKEN = os.environ.get("BALE_TOKEN", "184589737:cG07pnZ4wzLui6zrsXO8zQU37Pe9J_0REJ4")
BALE_CHANNEL = os.environ.get("BALE_CHANNEL", "6161249214")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "")  # شناسه چت خودت

BALE_API = f"https://tapi.bale.ai/bot{BALE_TOKEN}"

def send_bale_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{BALE_API}/sendMessage", json=payload)

def publish_to_channel(text):
    # اضافه کردن تگ کانال بله
    final_text = text + "\n\n📢 @Zangedaneshir"
    requests.post(f"{BALE_API}/sendMessage", json={
        "chat_id": BALE_CHANNEL,
        "text": final_text
    })

@app.route(f"/webhook/{BALE_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return jsonify({"ok": True})

    message = data.get("message", {})
    chat_id = str(message.get("chat", {}).get("id", ""))
    text = message.get("text", "")

    # فقط ادمین میتونه استفاده کنه
    if ADMIN_CHAT_ID and chat_id != ADMIN_CHAT_ID:
        send_bale_message(chat_id, "⛔ شما دسترسی ندارید.")
        return jsonify({"ok": True})

    if text == "/start":
        send_bale_message(chat_id, 
            "سلام! 👋\nپیام خودت رو بفرست، بعد دکمه ارسال رو بزن.")
        return jsonify({"ok": True})

    if text == "✅ ارسال به کانال":
        # پیام ذخیره‌شده رو ارسال کن
        saved = pending_messages.get(chat_id)
        if saved:
            publish_to_channel(saved)
            del pending_messages[chat_id]
            send_bale_message(chat_id, "✅ پیام با موفقیت در کانال منتشر شد!")
        else:
            send_bale_message(chat_id, "⚠️ پیامی برای ارسال پیدا نشد.")
        return jsonify({"ok": True})

    if text == "❌ انصراف":
        pending_messages.pop(chat_id, None)
        send_bale_message(chat_id, "انصراف داده شد.")
        return jsonify({"ok": True})

    # ذخیره پیام و نمایش دکمه تأیید
    pending_messages[chat_id] = text
    keyboard = {
        "keyboard": [
            [{"text": "✅ ارسال به کانال"}, {"text": "❌ انصراف"}]
        ],
        "resize_keyboard": True
    }
    send_bale_message(chat_id,
        f"📝 پیام آماده ارسال:\n\n{text}\n\n---\nآیا ارسال شود؟",
        reply_markup=keyboard)

    return jsonify({"ok": True})

@app.route("/")
def index():
    return "ربات زنگ دانش فعال است ✅"

# حافظه موقت پیام‌ها
pending_messages = {}

if __name__ == "__main__":
    # ثبت webhook
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
