from telethon import TelegramClient, events
from telethon.tl.patched import Message
import os
from functions import unpickle
from dotenv import load_dotenv
from DB import DB
from common import (
    AV_TEXT,
    AV_SOON_TEXT,
    FROM_FILE_NAME,
    TO_FILE_NAME,
    AV_FILE_NAME,
    AV_SOON_FILE_NAME,
    products_dict,
)

DB.creat_tables()
load_dotenv()

client = TelegramClient(
    session="session",
    api_hash=os.getenv("API_HASH"),
    api_id=os.getenv("API_ID"),
).start(phone=os.getenv("PHONE"))

bot = TelegramClient(
    session="bot_session",
    api_hash=os.getenv("API_HASH"),
    api_id=os.getenv("API_ID"),
).start(bot_token=os.getenv("BOT_TOKEN"))


@client.on(events.NewMessage())
async def get_post(event: events.NewMessage.Event | events.Album.Event):

    FROM_CHANNEL = unpickle(FROM_FILE_NAME)
    if event.chat_id != FROM_CHANNEL:
        return
    TO_CHANNEL = unpickle(TO_FILE_NAME)

    if all(i not in event.text for i in [AV_SOON_TEXT, AV_TEXT]):
        return
    elif AV_TEXT in event.text:
        temb: str = unpickle(AV_FILE_NAME)
    elif AV_SOON_TEXT in event.text:
        temb: str = unpickle(AV_SOON_FILE_NAME)
    else:
        return
    if not temb:
        return

    product = ""
    message: Message = event.message
    
    if not message.buttons:
        return
    
    for row in message.buttons:
        for b in row:
            for k, prod in products_dict.items():
                if k in b.url:
                    product = prod
    if not product:
        return

    stored_msg = None
    # Handle Single Media
    if not event.grouped_id:
        if event.is_reply:
            stored_msg = DB.get_messages(
                from_message_id=message.reply_to_msg_id,
                from_channel_id=event.chat_id,
                to_channel_id=TO_CHANNEL,
            )
        # Single Photo
        if message.photo or message.video:
            path = await client.download_media(message, "photos")
            msg = await bot.send_file(
                TO_CHANNEL,
                caption=temb.replace("$$$", product),
                file=path,
                reply_to=stored_msg[0] if stored_msg else None,
                buttons=message.buttons,
            )
            os.remove(path)
        # Just Text
        else:
            msg = await bot.send_message(
                entity=TO_CHANNEL,
                message=temb.replace("$$$", product),
                reply_to=stored_msg[0] if stored_msg else None,
                buttons=message.buttons,
            )
        await DB.add_message(
            from_message_id=message.id,
            to_message_id=msg.id,
            from_channel_id=event.chat_id,
            to_channel_id=TO_CHANNEL,
        )
    raise events.StopPropagation


if __name__ == "__main__":
    print("Running....")
    client.run_until_disconnected()
    print("Stopping...")
