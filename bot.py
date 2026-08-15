import sqlite3
from dotenv import load_dotenv
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

load_dotenv()

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ADMIN_ID = 7557316295

CHANNELS = [
     -1004457328254,
     -1004310356306,
     -1004315056647,
     "@kuponlar001"
]

PRIVATE_LINKS = [
    "https://t.me/+--j67_kHSEA3NDRi",
    "https://t.me/+xDdkHqoF_kg2MWIy",
    "https://t.me/+L3Za_V-Ab2s0YjYy"
]

# DATABASE
db = sqlite3.connect("movies.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies(
code TEXT PRIMARY KEY,
file_id TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY
)
""")
try:
    cur.execute(
        "ALTER TABLE movies ADD COLUMN title TEXT"
    )
    db.commit()
except:
    pass
try:
    cur.execute(
        "ALTER TABLE movies ADD COLUMN caption TEXT"
    )
    db.commit()
except:
    pass
db.commit()



async def check_sub(bot, user_id):

    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user_id)

            if member.status in ["left", "kicked"]:
                return False

        except Exception as e:
            print("OBUNA XATOSI:", ch, e)
            return False

    return True

async def check_sub(bot, user_id):

    not_subscribed = []

    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user_id)

            print(
                "OBUNA:",
                ch,
                "USER:",
                user_id,
                "STATUS:",
                member.status
            )

            if member.status in ["left", "kicked"]:
                not_subscribed.append(ch)

        except Exception as e:
            print("OBUNA XATOSI:", ch, e)
            not_subscribed.append(ch)

    return not_subscribed

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cur.execute(
        "INSERT OR IGNORE INTO users VALUES (?)",
        (user_id,)
    )

    db.commit()

    not_subscribed = await check_sub(
        context.bot,
        user_id
    )

    if not_subscribed:

        btn = []

        channel_links = {
            -1004457328254: (
                "📢 1-kanalga qo'shilish",
                "https://t.me/+L3Za_V-Ab2s0YjYy"
            ),
            -1004310356306: (
                "📢 2-kanalga qo'shilish",
                "https://t.me/+xDdkHqoF_kg2MWIy"
            ),
            -1004315056647: (
                "📢 3-kanalga qo'shilish",
                "https://t.me/+--j67_kHSEA3NDRi"
            ),
            "@kuponlar001": (
                "🌐 Kuponlarga qo'shilish",
                "https://t.me/kuponlar001"
            )
        }

        for channel in not_subscribed:

            if channel in channel_links:

                button_text, link = channel_links[channel]

                btn.append([
                    InlineKeyboardButton(
                        button_text,
                        url=link
                    )
                ])

        btn.append([
            InlineKeyboardButton(
                "✅ Tekshirish",
                callback_data="check"
            )
        ])

        await update.message.reply_text(
            "📢 Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling.\n\n"
            "✅ Obuna bo'lgach, «Tekshirish» tugmasini bosing.",
            reply_markup=InlineKeyboardMarkup(btn)
        )

        return

    if user_id == ADMIN_ID:

        keyboard = [
            [
                InlineKeyboardButton(
                    "👨‍💼 Boshqaruv paneli",
                    callback_data="open_admin"
                )
            ]
        ]

        await update.message.reply_text(
            "🎬 CinemaHub\n\n"
            "👨‍💼 Admin sifatida kirdingiz.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        await update.message.reply_text(
            "🎬 CinemaHub\n\n"
            "📥 Video kodini yuboring.\n\n"
            "🍿 Tomoshani boshlang."
        )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id

    not_subscribed = await check_sub(
        context.bot,
        user_id
    )

    if not_subscribed:

        await q.answer(
            "❌ Hali barcha kanallarga obuna bo'lmagansiz.",
            show_alert=True
        )

        btn = []

        channel_links = {
            -1004457328254: (
                "📢 1-kanalga qo'shilish",
                "https://t.me/+L3Za_V-Ab2s0YjYy"
            ),
            -1004310356306: (
                "📢 2-kanalga qo'shilish",
                "https://t.me/+xDdkHqoF_kg2MWIy"
            ),
            -1004315056647: (
                "📢 3-kanalga qo'shilish",
                "https://t.me/+--j67_kHSEA3NDRi"
            ),
            "@kuponlar001": (
                "🌐 Kuponlarga qo'shilish",
                "https://t.me/kuponlar001"
            )
        }

        for channel in not_subscribed:

            if channel in channel_links:

                button_text, link = channel_links[channel]

                btn.append([
                    InlineKeyboardButton(
                        button_text,
                        url=link
                    )
                ])

        btn.append([
            InlineKeyboardButton(
                "✅ Tekshirish",
                callback_data="check"
            )
        ])

        await q.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )

        return

    await q.message.edit_text(
        "✅ Obuna tasdiqlandi!\n\n"
        "🎬 CinemaHub\n\n"
        "📥 Video kodini yuboring.\n\n"
        "🍿 Tomoshani boshlang."
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Siz admin emassiz.")
        return

    keyboard = [
        [InlineKeyboardButton("➕ Video qo‘shish", callback_data="admin_add")],
        [InlineKeyboardButton("🗑 Video o‘chirish", callback_data="admin_delete")],
        [InlineKeyboardButton("📋 Ro‘yxat", callback_data="admin_list")],
        [InlineKeyboardButton("📊 Statistika", callback_data="admin_stat")],
        [InlineKeyboardButton("📨 Xabar yuborish", callback_data="admin_sendall")]
    ]

    await update.message.reply_text(
        "⚙️ Boshqaruv paneli",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def open_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    keyboard = [
        [InlineKeyboardButton("➕ Video qo‘shish", callback_data="admin_add")],
        [InlineKeyboardButton("🗑 Video o‘chirish", callback_data="admin_delete")],
        [InlineKeyboardButton("📋 Ro‘yxat", callback_data="admin_list")],
        [InlineKeyboardButton("📊 Statistika", callback_data="admin_stat")],
        [InlineKeyboardButton("📨 Xabar yuborish", callback_data="admin_sendall")]
    ]

    await query.edit_message_text(
        "⚙️ Boshqaruv paneli",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    # ➕ VIDEO QO'SHISH
    if query.data == "admin_add":

        context.user_data["video"] = True

        await query.message.reply_text(
            "📹 Videoni yuboring.\n\n"
            "Kod avtomatik beriladi."
        )

    # 🗑 VIDEO O'CHIRISH
    elif query.data == "admin_delete":

        context.user_data["delete"] = True

        await query.message.reply_text(
            "🗑 O‘chirmoqchi bo‘lgan video kodini yuboring."
        )

    # 📋 KINO RO'YXATI
    elif query.data == "admin_list":

        cur.execute(
            "SELECT code, title FROM movies "
            "ORDER BY CAST(code AS INTEGER)"
        )

        movies = cur.fetchall()

        if not movies:

            await query.message.reply_text(
                "📋 Hozircha kinolar yo‘q."
            )

            return

        text = "📋 Kino ro‘yxati:\n\n"

        for code, title in movies:

            text += (
                f"🎬 {code} — "
                f"{title or 'Nomsiz'}\n"
            )

        await query.message.reply_text(text)

    # 📊 STATISTIKA
    elif query.data == "admin_stat":

        cur.execute(
            "SELECT COUNT(*) FROM movies"
        )

        movie_count = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM users"
        )

        user_count = cur.fetchone()[0]

        await query.message.reply_text(
            "📊 BOT STATISTIKASI\n\n"
            f"👥 Foydalanuvchilar: {user_count}\n"
            f"🎬 Kinolar: {movie_count}"
        )

    # 📨 BARCHA FOYDALANUVCHILARGA XABAR
    elif query.data == "admin_sendall":

        context.user_data["sendall"] = True

        await query.message.reply_text(
            "📨 Barcha foydalanuvchilarga yuboriladigan "
            "xabarni yozing."
        )


async def addkino(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data["add"] = True

    await update.message.reply_text(
        "Kino kodini yuboring (misol: 001)"
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()
    user_id = update.effective_user.id

    # ==================================================
    # ADMIN — KINO QO'SHISH
    # ==================================================
    if user_id == ADMIN_ID and context.user_data.get("add"):

        context.user_data["code"] = text
        context.user_data["add"] = False
        context.user_data["video"] = True

        await update.message.reply_text(
            "🎬 Endi videoni yuboring."
        )
        return

# ==================================================
    # ADMIN — BARCHA FOYDALANUVCHILARGA XABAR
    # ==================================================
    if user_id == ADMIN_ID and context.user_data.get("sendall"):

        message = text

        cur.execute(
            "SELECT user_id FROM users"
        )

        users = cur.fetchall()

        count = 0

        for user in users:

            try:
                await context.bot.send_message(
                    chat_id=user[0],
                    text=message
                )

                count += 1

            except Exception as e:

                print(
                    f"SENDALL XATOSI: {user[0]} -> {e}"
                )

        context.user_data["sendall"] = False

        await update.message.reply_text(
            f"✅ Xabar yuborildi!\n\n"
            f"👥 Jami: {len(users)} ta\n"
            f"📨 Yuborildi: {count} ta\n"
            f"❌ Yuborilmadi: {len(users) - count} ta"
        )

        return

    # ==================================================
    # ADMIN — KINO O'CHIRISH
    # ==================================================
    if user_id == ADMIN_ID and context.user_data.get("delete"):

        code = text

        cur.execute(
            "SELECT code FROM movies WHERE code=?",
            (code,)
        )

        movie = cur.fetchone()

        if not movie:
            context.user_data["delete"] = False

            await update.message.reply_text(
                f"❌ {code} kodi bo‘yicha kino topilmadi."
            )
            return

        cur.execute(
            "DELETE FROM movies WHERE code=?",
            (code,)
        )

        db.commit()

        context.user_data["delete"] = False

        await update.message.reply_text(
            f"🗑 Kino o‘chirildi!\n\n"
            f"🎬 Kod: {code}"
        )
        return

    # ==================================================
    # ADMIN — VIDEO YUBORISH HOLATI
    # ==================================================
    if user_id == ADMIN_ID and context.user_data.get("video"):
        return

    # ==================================================
    # MAJBURIY OBUNA TEKSHIRISH
    # ==================================================
    not_subscribed = await check_sub(
        context.bot,
        user_id
    )

    if not_subscribed:

        btn = []

        channel_links = {
            -1004457328254: (
                "📢 1-kanalga qo'shilish",
                "https://t.me/+L3Za_V-Ab2s0YjYy"
            ),
            -1004310356306: (
                "📢 2-kanalga qo'shilish",
                "https://t.me/+xDdkHqoF_kg2MWIy"
            ),
            -1004315056647: (
                "📢 3-kanalga qo'shilish",
                "https://t.me/+--j67_kHSEA3NDRi"
            ),
            "@kuponlar001": (
                "🌐 Kuponlarga qo'shilish",
                "https://t.me/kuponlar001"
            )
        }

        for channel in not_subscribed:

            if channel in channel_links:

                button_text, link = channel_links[channel]

                btn.append([
                    InlineKeyboardButton(
                        button_text,
                        url=link
                    )
                ])

        btn.append([
            InlineKeyboardButton(
                "✅ Tekshirish",
                callback_data="check"
            )
        ])

        await update.message.reply_text(
            "📢 Avval barcha kanallarga obuna bo‘ling.\n\n"
            "✅ Obuna bo‘lgach, «Tekshirish» tugmasini bosing.",
            reply_markup=InlineKeyboardMarkup(btn)
        )

        return

    # ==================================================
    # 🎬 VIDEO KODINI QIDIRISH
    # ==================================================
    cur.execute(
        "SELECT file_id, caption FROM movies WHERE code=?",
        (text,)
    )

    data = cur.fetchone()

    if data:

        await update.message.reply_video(
            video=data[0],
            caption=data[1] or ""
        )

        return

    # ==================================================
    # ❌ KOD TOPILMAGANDA
    # ==================================================
    await update.message.reply_text(
        "❌ Kechirasiz, bu kod bo‘yicha video topilmadi."
    )


async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    file_id = update.message.video.file_id

    cur.execute(
        "SELECT MAX(CAST(code AS INTEGER)) FROM movies"
    )

    last = cur.fetchone()[0]

    if last is None:
        code = "001"
    else:
        code = str(last + 1).zfill(3)
    caption = update.message.caption or ""

    cur.execute(
        "INSERT INTO movies(code, file_id, caption) VALUES (?, ?, ?)",
        (code, file_id, caption)
    )

    db.commit()

    context.user_data["video"] = False

    await update.message.reply_text(
        f"✅ Video muvaffaqiyatli qo'shildi.\n\n"
        f"🎬 Video kodi: {code}"
    )

async def deletekino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) == 0:
        await update.message.reply_text(
            "Misol: /deletekino 001"
        )
        return

    code = context.args[0]

    cur.execute(
        "DELETE FROM movies WHERE code=?",
        (code,)
    )

    db.commit()

    if cur.rowcount > 0:
        await update.message.reply_text(
            f"🗑 Kino o'chirildi: {code}"
        )
    else:
        await update.message.reply_text(
            "❌ Bunday kino topilmadi"
        )
async def listkino(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    cur.execute(
        "SELECT code FROM movies ORDER BY code"
    )

    movies = cur.fetchall()

    if not movies:
        await update.message.reply_text(
            "📂 Kino bazasi bo'sh"
        )
        return

    text = "🎬 Kinolar:\n\n"

    for movie in movies:
        text += f"• {movie[0]}\n"
async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    cur.execute(
        "SELECT COUNT(*) FROM users"
    )

    users = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM movies"
    )

    movies = cur.fetchone()[0]

    await update.message.reply_text(
        f"📊 Statistika\n\n"
        f"👤 Foydalanuvchilar: {users}\n"
        f"🎬 Kinolar: {movies}"
    )

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    with open("movies.db", "rb") as db_file:
        await update.message.reply_document(
            document=db_file,
            filename="movies.db",
            caption="💾 Ma'lumotlar bazasi (Backup)"
        )

async def sendall(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "Misol:\n/sendall Salom hammaga"
        )
        return

    message = " ".join(context.args)

    cur.execute(
        "SELECT user_id FROM users"
    )

    users = cur.fetchall()

    count = 0

    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user[0],
                text=message
            )
            count += 1

        except Exception as e:
            print(
                f"SENDALL XATOSI: {user[0]} -> {e}"
            )

    await update.message.reply_text(
        f"✅ Xabar yuborildi: {count} ta foydalanuvchi"
    )
    await update.message.reply_text(text)
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("addkino", addkino))
app.add_handler(CommandHandler("deletekino", deletekino))
app.add_handler(CommandHandler("listkino", listkino))
app.add_handler(CommandHandler("stat", stat))
app.add_handler(CommandHandler("backup", backup))
app.add_handler(CommandHandler("sendall", sendall))
app.add_handler(CallbackQueryHandler(check, pattern="check"))
app.add_handler(CallbackQueryHandler(admin_buttons, pattern="admin_"))
app.add_handler(CallbackQueryHandler(open_admin, pattern="^open_admin$"))
app.add_handler(MessageHandler(filters.VIDEO, video_handler))
app.add_handler(MessageHandler(filters.TEXT, text_handler))

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logging.error(context.error)

    print("XATO:", context.error)

app.add_error_handler(error_handler)

print("Bot ishga tushdi...")
app.run_polling()
