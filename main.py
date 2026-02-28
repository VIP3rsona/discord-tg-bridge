import discord
import requests
import os

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author.bot:
        return
if str(message.channel.id) != os.environ["DISCORD_CHANNEL_ID"]:
    return

    attachments = message.attachments
    text = message.content

    if len(attachments) >= 2:
        media = []
        for i, att in enumerate(attachments):
            item = {
                "type": "photo",
                "media": att.url
            }
            if i == 0 and text:
                item["caption"] = text
            media.append(item)

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMediaGroup",
            json={"chat_id": CHAT_ID, "media": media}
        )

    elif len(attachments) == 1:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
            json={
                "chat_id": CHAT_ID,
                "photo": attachments[0].url,
                "caption": text
            }
        )

    elif text:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text}
        )

client.run(DISCORD_TOKEN)
