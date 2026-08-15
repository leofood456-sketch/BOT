import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
import aiohttp
from aiohttp_socks import ProxyConnector
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден в .env файле!")
    exit(1)

# ========== НАСТРОЙКА ==========

# Твой работающий прокси для Telegram
PROXY_URL = "socks5://127.0.0.1:1443"

# Пытаемся подключиться через прокси
bot = None

try:
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=BOT_TOKEN, session=session)
    print(f"✅ Подключение через SOCKS5: {PROXY_URL}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("🔄 Пробую альтернативный способ...")
    try:
        # Используем встроенный прокси-сервер aiogram
        from aiogram.client.session.base import BaseSession
        
        class ProxySession(BaseSession):
            async def make_request(self, method, **kwargs):
                connector = ProxyConnector.from_url(PROXY_URL)
                async with aiohttp.ClientSession(connector=connector) as session:
                    # Эмулируем запрос
                    pass
        
        bot = Bot(token=BOT_TOKEN)
        print("✅ Подключение через стандартный метод")
    except Exception as e2:
        print(f"❌ Всё плохо: {e2}")
        exit(1)

dp = Dispatcher()

# ========== ГЕНЕРАТОР НИКОВ ==========

VOWELS = 'aeiouy'
CONSONANTS = 'bcdfghjklmnpqrstvwxz'

WORDS = [
    'bear', 'wolf', 'lion', 'tiger', 'eagle', 'hawk', 'owl', 'fox', 'cat', 'dog',
    'sun', 'moon', 'star', 'sky', 'fire', 'ice', 'wind', 'rain', 'snow', 'cloud',
    'king', 'queen', 'lord', 'knight', 'dragon', 'phoenix', 'shadow', 'light',
    'dark', 'storm', 'thunder', 'nova', 'cosmos', 'nebula', 'galaxy', 'zen',
    'yoga', 'karma', 'soul', 'spirit', 'dream', 'hope', 'faith', 'love', 'rock',
    'jazz', 'blues', 'metal', 'punk', 'cyber', 'tech', 'code', 'data', 'byte',
    'pixel', 'vector', 'peak', 'summit', 'ocean', 'river', 'lake', 'forest',
    'crystal', 'flame', 'spark', 'glow', 'shine', 'silent', 'echo', 'whisper',
    'mystic', 'ancient', 'sacred', 'eternal', 'brave', 'fierce', 'swift',
    'eclipse', 'aurora', 'twilight', 'blaze', 'ember', 'frost', 'winter',
    'thunder', 'lightning', 'cyclone', 'valor', 'honor', 'vigor', 'stealth',
    'phoenix', 'titan', 'cosmic', 'stellar', 'lunar', 'solar', 'polar', 'vortex'
]

SYLLABLES = [
    'ab', 'ac', 'al', 'am', 'an', 'ap', 'ar', 'as', 'at', 'av', 'az',
    'ba', 'be', 'bi', 'bo', 'bu', 'by', 'ca', 'ce', 'ci', 'co', 'cu', 'cy',
    'da', 'de', 'di', 'do', 'du', 'dy', 'el', 'em', 'en', 'ep', 'er', 'es', 'et',
    'fa', 'fe', 'fi', 'fo', 'fu', 'fy', 'ga', 'ge', 'gi', 'go', 'gu', 'gy',
    'ha', 'he', 'hi', 'ho', 'hu', 'hy', 'in', 'is', 'it', 'iv', 'ix', 'iz',
    'ka', 'ke', 'ki', 'ko', 'ku', 'ky', 'la', 'le', 'li', 'lo', 'lu', 'ly',
    'ma', 'me', 'mi', 'mo', 'mu', 'my', 'na', 'ne', 'ni', 'no', 'nu', 'ny',
    'on', 'op', 'or', 'os', 'ot', 'ov', 'ox', 'oz',
    'pa', 'pe', 'pi', 'po', 'pu', 'py', 'ra', 're', 'ri', 'ro', 'ru', 'ry',
    'sa', 'se', 'si', 'so', 'su', 'sy', 'ta', 'te', 'ti', 'to', 'tu', 'ty',
    'un', 'up', 'ur', 'us', 'ut', 'uv', 'ux', 'uz',
    'va', 've', 'vi', 'vo', 'vu', 'vy', 'xa', 'xe', 'xi', 'xo', 'xu', 'xy',
    'za', 'ze', 'zi', 'zo', 'zu', 'zy'
]

def generate_username(length: int) -> str:
    style = random.choice(['vowel_consonant', 'syllable', 'word', 'word_syllable', 'syllable_word'])
    username = ""
    
    if style == 'vowel_consonant':
        username = random.choice(CONSONANTS)
        while len(username) < length:
            username += random.choice(VOWELS) if len(username) % 2 == 1 else random.choice(CONSONANTS)
        username = username[:length]
    
    elif style == 'syllable':
        while len(username) < length:
            syllable = random.choice(SYLLABLES)
            username += syllable[:length - len(username)] if len(username) + len(syllable) > length else syllable
    
    elif style == 'word':
        base = random.choice(WORDS)
        username = base + ''.join(random.choice(SYLLABLES) for _ in range(2)) if len(base) < length else base[:length]
        username = username[:length]
    
    elif style == 'word_syllable':
        base = random.choice(WORDS)
        if len(base) < length:
            username = base + random.choice(SYLLABLES)[:length - len(base)]
        else:
            username = base[:length]
    
    else:
        prefix = random.choice(SYLLABLES)
        base = random.choice(WORDS)
        username = (prefix + base)[:length]
    
    while len(username) < length:
        username += random.choice(VOWELS + CONSONANTS)
    username = username[:length]
    
    if not username[0].isalpha() or username[0] in VOWELS:
        username = random.choice(CONSONANTS) + username[1:]
    
    return username

async def check_username_socks5(username: str) -> bool:
    """Проверка через SOCKS5 прокси"""
    url = f"https://t.me/{username}"
    print(f"🔍 @{username}...", end=" ")
    
    try:
        connector = ProxyConnector.from_url(PROXY_URL)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, timeout=10) as response:
                status = response.status
                if status == 404:
                    print(f"✅ СВОБОДЕН!")
                    return True
                else:
                    print(f"❌ ЗАНЯТ (статус: {status})")
                    return False
    except Exception as e:
        print(f"⚠️ Ошибка: {str(e)[:40]}")
        return False

async def check_batch(usernames: list) -> dict:
    print(f"\n📦 ПАРТИЯ из {len(usernames)} ников:")
    tasks = [check_username_socks5(username) for username in usernames]
    results = await asyncio.gather(*tasks)
    return {usernames[i]: results[i] for i in range(len(usernames))}

# ========== КЛАВИАТУРА ==========

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Редкие (4-7)", callback_data="rare")],
        [InlineKeyboardButton(text="📌 Обычные (7-10)", callback_data="normal")],
        [InlineKeyboardButton(text="📏 Длинные (10-12)", callback_data="long")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")]
    ])
    return keyboard

# ========== КОМАНДЫ ==========

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"🚀 **БОТ ДЛЯ ПОИСКА ЮЗЕРНЕЙМОВ!**\n\n"
        f"🔌 Прокси: MTProto (порт 1443)\n"
        f"🌐 Проверка: через SOCKS5\n\n"
        "Выбери режим:",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    
    if callback.data == "rare":
        mode_name = "РЕДКИЕ"
        lengths = [4, 5, 6, 7]
        emoji = "🔥"
    elif callback.data == "normal":
        mode_name = "ОБЫЧНЫЕ"
        lengths = [7, 8, 9, 10]
        emoji = "📌"
    elif callback.data == "long":
        mode_name = "ДЛИННЫЕ"
        lengths = [10, 11, 12]
        emoji = "📏"
    else:
        await callback.answer()
        return
    
    batch_size = 15
    
    print("\n" + "="*60)
    print(f"🚀 {mode_name} | Длина: {lengths}")
    print("="*60 + "\n")
    
    status_msg = await bot.send_message(
        chat_id,
        f"{emoji} **{mode_name} ПОИСК**\n\n"
        f"📏 Длина: {', '.join(map(str, lengths))}\n"
        f"⏳ Ищу..."
    )
    
    found = None
    total_attempts = 0
    batch_count = 0
    
    while not found:
        batch_count += 1
        batch = []
        
        for _ in range(batch_size):
            length = random.choice(lengths)
            username = generate_username(length)
            if random.random() < 0.2 and len(username) < 12:
                username += str(random.randint(1, 99))
            if username not in batch and len(username) >= 4:
                batch.append(username)
        
        results = await check_batch(batch)
        total_attempts += len(batch)
        
        for username, available in results.items():
            if available:
                found = username
                print("\n" + "="*60)
                print(f"🎉 НАЙДЕН! @{username}")
                print(f"📊 Проверено: {total_attempts}")
                print("="*60 + "\n")
                break
        
        if batch_count % 3 == 0:
            try:
                await status_msg.edit_text(
                    f"{emoji} **{mode_name} ПОИСК**\n\n"
                    f"📊 Проверено: {total_attempts}\n"
                    f"📦 Партий: {batch_count}\n"
                    f"⏳ Продолжаю..."
                )
            except:
                pass
        
        await asyncio.sleep(0.3)
    
    if found:
        await bot.send_message(
            chat_id,
            f"🎉 **НАШЁЛ!**\n\n"
            f"✅ @{found} — **СВОБОДЕН!**\n"
            f"📏 Длина: {len(found)} символов\n"
            f"📊 Проверено: {total_attempts}\n\n"
            f"⚡ Забирай! 🔥",
            reply_markup=get_main_keyboard()
        )
    
    await callback.answer()

# ========== ЗАПУСК ==========

async def main():
    print("="*60)
    print("🚀 БОТ ЗАПУЩЕН!")
    print(f"🤖 Токен: {BOT_TOKEN[:10]}...")
    print(f"🔌 Прокси: 127.0.0.1:1443 (MTProto)")
    print("="*60 + "\n")
    print("📱 Открой Telegram и напиши /start")
    print("="*60 + "\n")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())