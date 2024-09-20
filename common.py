from telegram import InlineKeyboardButton

FROM_FILE_NAME = "from_channel.pickle"
TO_FILE_NAME = "to_channel.pickle"
AV_FILE_NAME = "av_message.pickle"
AV_SOON_FILE_NAME = "av_soon_message.pickle"

AV_SOON_TEXT = "سيتوفر قريبا"
AV_TEXT = "المنتج متوفر"

settings_keyboard = [
    [
        InlineKeyboardButton(
            text="تعديل قناة النسخ",
            callback_data=f"edit {FROM_FILE_NAME}",
        ),
    ],
    [
        InlineKeyboardButton(
            text="تعديل قناة اللصق",
            callback_data=f"edit {TO_FILE_NAME}",
        )
    ],
    [
        InlineKeyboardButton(
            text="عرض القنوات الحالية",
            callback_data="show",
        ),
    ],
    [
        InlineKeyboardButton(
            text="تعديل رسالة التوفر",
            callback_data=f"edit {AV_FILE_NAME}",
        )
    ],
    [
        InlineKeyboardButton(
            text="تعديل رسالة سيتوفر قريباً",
            callback_data=f"edit {AV_SOON_FILE_NAME}",
        )
    ],
]


def build_back_button(data: str):
    return [InlineKeyboardButton(text="الرجوع🔙", callback_data=data)]


products_dict = {
    "edgy-mint": "إيدجي منت",
    "garden-mint": "جاردن منت",
    "haila": "هيلة",
    "highland-berries": "هايلاند بيريز",
    "icy-rush": "آيسي رش",
    "mint-fusion": "منت فيوجن",
    "purple-mist": "بيربل مست",
    "dzrt-samra-special-edition": 'دزرت – "سمرة" إصدار خاص',
    "samra": "سمرة",
    "tamra": "تمرة",
    "spicy-zest": "سبايسي زيست",
    "seaside-frost": "سي سايد فروست",
}
