import os
import sys
import telebot

# ---------------------------
# DIRECT CONFIG (NO .ENV)
# ---------------------------
BOT_TOKEN = "8214030670:AAFHyG47OtE0CAvLJYJ3naoZN8W8Jn-C6bU"
CHANNEL_USERNAME = "SHAITaN_KA_BAAP_Hu"
OWNER_URL = "https://t.me/SHAITaN_KA_BAAP_Hu"
WORKERS = 16
OWNER_ID_1 = 5663291046
OWNER_ID_2 = 5663291046

# ---------------------------
# USER MANAGER (INLINE CODE)
# ---------------------------
class UserManager:
    def init(self):
        self.users = {}

    def add_user(self, user_id):
        self.users[user_id] = {"active": True}

    def is_user(self, user_id):
        return user_id in self.users


# ---------------------------
# KEYBOARDS (INLINE CODE)
# ---------------------------
from telebot import types

def create_start_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Start", "Help")
    return kb

def create_gates_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Open Gate", callback_data="open_gate"))
    return kb


# ---------------------------
# MESSAGES (INLINE CODE)
# ---------------------------
def format_welcome_message(user, channel, owner):
    return f"👋 Hello {user}!\nWelcome!\nJoin @{channel}\nOwner: {owner}"


# ---------------------------
# HANDLERS (INLINE CODE)
# ---------------------------
def register_command_handlers(bot, user_manager, OWNERS, channel, owner_url):

    @bot.message_handler(commands=["start"])
    def start(msg):
        user_id = msg.from_user.id
        user_manager.add_user(user_id)
        username = msg.from_user.first_name

        welcome = format_welcome_message(username, channel, owner_url)
        bot.send_message(user_id, welcome, reply_markup=create_start_keyboard())

    @bot.message_handler(commands=["admin"])
    def admin(msg):
        if msg.from_user.id not in OWNERS:
            return bot.reply_to(msg, "❌ You are not the owner!")

        bot.send_message(msg.chat.id, "👑 Welcome Owner")


def register_callback_handler(bot, user_manager, channel, owner_url):

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        if call.data == "open_gate":
            bot.answer_callback_query(call.id, "🚀 Gate opened!")
            bot.send_message(call.message.chat.id, "Gate opened.", reply_markup=create_gates_keyboard())


# ---------------------------
# BOT INITIALIZATION
# ---------------------------

# Validate token
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN missing!")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN, num_threads=WORKERS)
user_manager = UserManager()
OWNERS = [OWNER_ID_1, OWNER_ID_2]

# Register handlers
register_command_handlers(bot, user_manager, OWNERS, CHANNEL_USERNAME, OWNER_URL)
register_callback_handler(bot, user_manager, CHANNEL_USERNAME, OWNER_URL)


# ---------------------------
# MAIN LOOP
# ---------------------------
def main():
    print(f"🤖 Bot started with {WORKERS} workers")
    print(f"👑 Owners: {OWNER_ID_1}, {OWNER_ID_2}")
    print(f"📢 Channel: @{CHANNEL_USERNAME}")
    print("⚡️ Running...")

    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=30, skip_pending=True)
    except KeyboardInterrupt:
        print("🛑 Stopped by user")
        sys.exit(0)
    except Exception as e:
        print("❌ Error:", e)
        print("🔄 Restarting...")
        main()


if name == "main":
    main()
