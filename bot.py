import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BALE_TOKEN = os.environ.get("BALE_TOKEN", "2112844221:6qmjOR4mOG8nMD4RzNpT3j2g-5C8F43_pSI")
BALE_API = f"https://tapi.bale.ai/bot{BALE_TOKEN}"

COURSES = {
    "course_1": {
        "name": "تولید محتوا با هوش مصنوعی",
        "price_original": "۱,۵۹۰,۰۰۰ تومان",
        "price_discount": "۸۹۰,۰۰۰ تومان",
        "link": "https://www.zangedanesh.com/product/تولید-محتوا-با-هوش-مصنوعی/",
        "description": "یاد بگیر چطور با ابزارهای هوش مصنوعی محتوای حرفه‌ای تولید کنی و زمانت رو چند برابر کنی."
    },
    "course_2": {
        "name": "طراحی سایت و تولید محتوای سایت",
        "price_original": "۲,۰۰۰,۰۰۰ تومان",
        "price_discount": "۹۵۰,۰۰۰ تومان",
        "link": "https://www.zangedanesh.com/product/طراحی-سایت-سئو/",
        "description": "از صفر تا صد طراحی سایت و تولید محتوای سئو شده رو یاد بگیر."
    },
    "course_3": {
        "name": "آموزش اینستاگرام و تولید محتوا",
        "price_original": "۱,۶۹۰,۰۰۰ تومان",
        "price_discount": "۹۹۰,۰۰۰ تومان",
        "link": "https://www.zangedanesh.com/product/goldenroad/",
        "description": "رشد واقعی در اینستاگرام با تولید محتوای هدفمند و استراتژی درست."
    },
    "course_4": {
        "name": "یوتیوبر شو",
        "price_original": "۱,۳۹۰,۰۰۰ تومان",
        "price_discount": "۷۹۰,۰۰۰ تومان",
        "link": "https://www.zangedanesh.com/product/دوره-آموزشی-یوتیوبر-شو/",
        "description": "کانال یوتیوب بساز، محتوا تولید کن و درآمد دلاری داشته باش."
    }
}

CONTACT_TEXT = """سلام به تمام زنگ دانشی‌ها 👋🏻❤️
من امیر صالح هستم، موسس و مدیر مجموعه آموزشی زنگ‌دانش.

راه‌های ارتباطی با من 👇🏻

👤 تلگرام: @AmiirSaleh
📱 شماره تماس: 09374694169
📸 اینستاگرام: https://www.instagram.com/zangedanesh
📢 کانال تلگرام: https://t.me/zangedanesh
▶️ یوتیوب: https://www.youtube.com/@zangedanesh
🎬 آپارات: https://www.aparat.com/zangedanesh/
🌐 وبسایت: https://zangedanesh.com
📲 سروش: https://splus.ir/zangedanesh
💬 بله: https://ble.ir/zangedaneshir
📩 ایتا: https://eitaa.com/zangedanesh"""

ABOUT_TEXT = """🎓 <b>درباره زنگ دانش</b>

زنگ دانش یه مجموعه آموزشی تخصصیه که توسط امیر صالح تأسیس شده.

ما آموزش‌های کاربردی در حوزه‌های زیر ارائه می‌دیم:
🤖 تولید محتوا با هوش مصنوعی
🌐 طراحی سایت و سئو
📸 اینستاگرام و شبکه‌های اجتماعی
▶️ یوتیوب و تولید محتوای ویدیویی

هدف ما کمک به رشد حرفه‌ای و درآمدزایی شماست. 🚀

🌐 وبسایت: https://zangedanesh.com"""


def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{BALE_API}/sendMessage", json=payload)


def main_menu():
    return {
        "keyboard": [
            [{"text": "📚 دوره‌های آموزشی"}],
            [{"text": "📞 ارتباط با ما"}, {"text": "ℹ️ درباره زنگ دانش"}]
        ],
        "resize_keyboard": True
    }


def courses_menu():
    return {
        "keyboard": [
            [{"text": "🤖 تولید محتوا با هوش مصنوعی"}],
            [{"text": "🌐 طراحی سایت و تولید محتوا"}],
            [{"text": "📸 آموزش اینستاگرام"}],
            [{"text": "▶️ یوتیوبر شو"}],
            [{"text": "🔙 بازگشت"}]
        ],
        "resize_keyboard": True
    }


def course_detail_menu(course_name):
    return {
        "keyboard": [
            [{"text": f"💳 ثبت‌نام در {course_name}"}],
            [{"text": "🔙 بازگشت به دوره‌ها"}]
        ],
        "resize_keyboard": True
    }


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "", 200

    message = data.get("message", {})
    chat_id = str(message.get("chat", {}).get("id", ""))
    text = message.get("text", "").strip()

    if not chat_id or not text:
        return "", 200

    if text == "/start":
        send_message(chat_id,
            "سلام! 👋 به <b>زنگ دانش</b> خوش اومدی!\n\n"
            "اینجا میتونی دوره‌های آموزشی ما رو ببینی و ثبت‌نام کنی.\n"
            "از منوی پایین شروع کن 👇",
            reply_markup=main_menu())

    elif text == "📚 دوره‌های آموزشی":
        send_message(chat_id,
            "دوره‌های آموزشی زنگ دانش 👇\nیه دوره انتخاب کن:",
            reply_markup=courses_menu())

    elif text == "📞 ارتباط با ما":
        send_message(chat_id, CONTACT_TEXT, reply_markup=main_menu())

    elif text == "ℹ️ درباره زنگ دانش":
        send_message(chat_id, ABOUT_TEXT, reply_markup=main_menu())

    elif text == "🤖 تولید محتوا با هوش مصنوعی":
        c = COURSES["course_1"]
        send_message(chat_id,
            f"🤖 <b>{c['name']}</b>\n\n"
            f"📝 {c['description']}\n\n"
            f"💰 قیمت اصلی: <s>{c['price_original']}</s>\n"
            f"🔥 قیمت با تخفیف: <b>{c['price_discount']}</b>",
            reply_markup=course_detail_menu(c['name']))

    elif text == "🌐 طراحی سایت و تولید محتوا":
        c = COURSES["course_2"]
        send_message(chat_id,
            f"🌐 <b>{c['name']}</b>\n\n"
            f"📝 {c['description']}\n\n"
            f"💰 قیمت اصلی: <s>{c['price_original']}</s>\n"
            f"🔥 قیمت با تخفیف: <b>{c['price_discount']}</b>",
            reply_markup=course_detail_menu(c['name']))

    elif text == "📸 آموزش اینستاگرام":
        c = COURSES["course_3"]
        send_message(chat_id,
            f"📸 <b>{c['name']}</b>\n\n"
            f"📝 {c['description']}\n\n"
            f"💰 قیمت اصلی: <s>{c['price_original']}</s>\n"
            f"🔥 قیمت با تخفیف: <b>{c['price_discount']}</b>",
            reply_markup=course_detail_menu(c['name']))

    elif text == "▶️ یوتیوبر شو":
        c = COURSES["course_4"]
        send_message(chat_id,
            f"▶️ <b>{c['name']}</b>\n\n"
            f"📝 {c['description']}\n\n"
            f"💰 قیمت اصلی: <s>{c['price_original']}</s>\n"
            f"🔥 قیمت با تخفیف: <b>{c['price_discount']}</b>",
            reply_markup=course_detail_menu(c['name']))

    elif text.startswith("💳 ثبت‌نام در"):
        course_key = None
        for key, c in COURSES.items():
            if c["name"] in text:
                course_key = key
                break
        if course_key:
            c = COURSES[course_key]
            send_message(chat_id,
                f"✅ برای ثبت‌نام در دوره <b>{c['name']}</b> روی لینک زیر کلیک کن:\n\n"
                f"🔗 {c['link']}\n\n"
                "موفق باشی! 🚀",
                reply_markup=courses_menu())

    elif text == "🔙 بازگشت به دوره‌ها":
        send_message(chat_id, "دوره‌های آموزشی 👇", reply_markup=courses_menu())

    elif text == "🔙 بازگشت":
        send_message(chat_id, "منوی اصلی 👇", reply_markup=main_menu())

    else:
        send_message(chat_id,
            "از منوی پایین یه گزینه انتخاب کن 👇",
            reply_markup=main_menu())

    return "", 200


@app.route("/")
def index():
    return "ربات زنگ دانش فعال است ✅"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
