import asyncio
import random
from telethon import TelegramClient, events

BOT_TOKEN = "твой_токен_сюда"

client = TelegramClient('bot', api_id=6, api_hash='eb06d4abfb49dc3eeb1aeb98ae0f581e').start(bot_token=BOT_TOKEN)

# Генератор ников
VOWELS = 'aeiouy'
CONSONANTS = 'bcdfghjklmnpqrstvwxz'

def generate_username(length=6):
    username = random.choice(CONSONANTS)
    while len(username) < length:
        username += random.choice(VOWELS) if len(username) % 2 == 1 else random.choice(CONSONANTS)
    return username[:length]

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("🚀 Бот запущен! Напиши /search")

@client.on(events.NewMessage(pattern='/search'))
async def search(event):
    await event.reply("🔍 Ищу...")
    attempts = 0
    while True:
        attempts += 1
        username = generate_username(random.choice([6,7,8]))
        try:
            await client.get_entity(f"@{username}")
        except ValueError:
            await event.reply(f"✅ @{username} — СВОБОДЕН! (проверено {attempts})")
            break
        except Exception:
            continue

print("🚀 Бот запущен на Railway!")
client.run_until_disconnected()
