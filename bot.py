from telegram import Chat, Update, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CommandHandler,
)

from functions import pickle_in, unpickle
from common import (
    channel_settings_keyboard,
    build_back_button,
    TO_FILE_NAME,
    FROM_FILE_NAME,
)

import os

NEW_CHANNEL_ID = 0


async def channels_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and update.effective_user.id in [
        int(os.getenv("OWNER_ID")),
        755501092,
    ]:
        if update.message:
            await update.message.reply_text(
                text="إعدادات القنوات",
                reply_markup=InlineKeyboardMarkup(channel_settings_keyboard),
            )
        else:
            await update.callback_query.edit_message_text(
                text="إعدادات القنوات",
                reply_markup=InlineKeyboardMarkup(channel_settings_keyboard),
            )
        return ConversationHandler.END


async def edit_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and update.effective_user.id in [
        int(os.getenv("OWNER_ID")),
        755501092,
    ]:
        edit_type = update.callback_query.data.split(" ")[1]
        context.user_data["from_or_to"] = edit_type
        if "channel" in edit_type:
            text = (
                "أرسل id القناة الجديدة.\n"
                "يمكنك معرفة الآيدي عن طريق هذا البوت https://t.me/username_to_id_bot."
            )
        else:
            text = "أرسل القالب الجديد\n" "ملاحظة: ضع $$$ مكان اسم المنتج"

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup.from_row(
                build_back_button("back to channels settings")
            ),
            disable_web_page_preview=True,
        )
        return NEW_CHANNEL_ID


async def new_channel_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and update.effective_user.id in [
        int(os.getenv("OWNER_ID")),
        755501092,
    ]:
        try:
            new_val = int(update.message.text)
        except ValueError:
            new_val = update.message.text

        if "message" in context.user_data["from_or_to"] and "$$$" not in new_val:
            await update.message.reply_text(
                text="يرجى وضع $$$ مكان اسم المنتج",
            )
            return

        pickle_in(f"{context.user_data['from_or_to']}", new_val)

        text = "تم التعديل بنجاح ✅"
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(channel_settings_keyboard),
        )
        return ConversationHandler.END


async def show_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and update.effective_user.id in [
        int(os.getenv("OWNER_ID")),
        755501092,
    ]:
        CHANNEL = unpickle(FROM_FILE_NAME)
        text = f"آيدي قناة النسخ: {CHANNEL}\n\n"
        CHANNEL = unpickle(TO_FILE_NAME)
        text += f"آيدي قناة اللصق: {CHANNEL}\n\n"
        text += "اختر ماذا تريد أن تفعل:"
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(channel_settings_keyboard),
        )


start_command = CommandHandler(
    "start",
    channels_settings,
)

show_channels_handler = CallbackQueryHandler(
    callback=show_channels,
    pattern="^show$",
)

edit_channel_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=edit_channel,
            pattern="^edit",
        ),
    ],
    states={
        NEW_CHANNEL_ID: [
            MessageHandler(
                filters=filters.Regex("^-?\d+$") | filters.TEXT & ~filters.COMMAND,
                callback=new_channel_id,
            )
        ],
    },
    fallbacks=[
        start_command,
        CallbackQueryHandler(
            callback=channels_settings,
            pattern="^back to channels settings$",
        ),
    ],
)
