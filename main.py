import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

TOKEN = "8631386176:AAGZ0OpS21IuoM2VJU_uUYyOnHjWkpq_56g"

router = Router()

REGIONS = {
    "andijon": {
        "name": "Andijon viloyati",
        "districts": {
            "andijon": "Andijon tumani",
            "asaka": "Asaka tumani",
            "baliqchi": "Baliqchi tumani",
            "boston": "Boʻston tumani",
            "buloqboshi": "Buloqboshi tumani",
            "izboskan": "Izboskan tumani",
            "jalaquduq": "Jalaquduq tumani",
            "xojaobod": "Xoʻjaobod tumani",
            "qorgontepa": "Qoʻrgʻontepa tumani",
            "marhamat": "Marhamat tumani",
            "oltinkol": "Oltinkoʻl tumani",
            "paxtaobod": "Paxtaobod tumani",
            "shahrixon": "Shahrixon tumani",
            "ulugnor": "Ulugʻnor tumani",
        },
    },
    "buxoro": {
        "name": "Buxoro viloyati",
        "districts": {
            "olot": "Olot tumani",
            "buxoro": "Buxoro tumani",
            "gijduvon": "Gʻijduvon tumani",
            "jondor": "Jondor tumani",
            "kogon": "Kogon tumani",
            "qorakol": "Qorakoʻl tumani",
            "qorovulbozor": "Qorovulbozor tumani",
            "peshku": "Peshku tumani",
            "romitan": "Romitan tumani",
            "shofirkon": "Shofirkon tumani",
            "vobkent": "Vobkent tumani",
        },
    },
    "fargona": {
        "name": "Fargʻona viloyati",
        "districts": {
            "oltiariq": "Oltiariq tumani",
            "bagdod": "Bagʻdod tumani",
            "beshariq": "Beshariq tumani",
            "buvayda": "Buvayda tumani",
            "dangara": "Dangʻara tumani",
            "fargona": "Fargʻona tumani",
            "furqat": "Furqat tumani",
            "qoshtepa": "Qoʻshtepa tumani",
            "quva": "Quva tumani",
            "rishton": "Rishton tumani",
            "sox": "Soʻx tumani",
            "toshloq": "Toshloq tumani",
            "uchkoprik": "Uchkoʻprik tumani",
            "uzbekiston": "Oʻzbekiston tumani",
            "yozyovon": "Yozyovon tumani",
        },
    },
    "jizzax": {
        "name": "Jizzax viloyati",
        "districts": {
            "arnasoy": "Arnasoy tumani",
            "baxmal": "Baxmal tumani",
            "dostlik": "Doʻstlik tumani",
            "forish": "Forish tumani",
            "gallaorol": "Gʻallaorol tumani",
            "sharof_rashidov": "Sharof Rashidov tumani",
            "mirzachol": "Mirzachoʻl tumani",
            "paxtakor": "Paxtakor tumani",
            "yangiobod": "Yangiobod tumani",
            "zomin": "Zomin tumani",
            "zafarobod": "Zafarobod tumani",
            "zarbdor": "Zarbdor tumani",
        },
    },
    "namangan": {
        "name": "Namangan viloyati",
        "districts": {
            "chortoq": "Chortoq tumani",
            "chust": "Chust tumani",
            "kosonsoy": "Kosonsoy tumani",
            "mingbuloq": "Mingbuloq tumani",
            "namangan": "Namangan tumani",
            "norin": "Norin tumani",
            "pop": "Pop tumani",
            "toraqorgon": "Toʻraqoʻrgʻon tumani",
            "uchqorgon": "Uchqoʻrgʻon tumani",
            "uychi": "Uychi tumani",
            "yangiqorgon": "Yangiqoʻrgʻon tumani",
        },
    },
    "navoiy": {
        "name": "Navoiy viloyati",
        "districts": {
            "konimex": "Konimex tumani",
            "qiziltepa": "Qiziltepa tumani",
            "xatirchi": "Xatirchi tumani",
            "navbahor": "Navbahor tumani",
            "karmana": "Karmana tumani",
            "nurota": "Nurota tumani",
            "tomdi": "Tomdi tumani",
            "uchquduq": "Uchquduq tumani",
        },
    },
    "qashqadaryo": {
        "name": "Qashqadaryo viloyati",
        "districts": {
            "chiroqchi": "Chiroqchi tumani",
            "dehqonobod": "Dehqonobod tumani",
            "guzor": "Gʻuzor tumani",
            "qamashi": "Qamashi tumani",
            "qarshi": "Qarshi tumani",
            "koson": "Koson tumani",
            "kasbi": "Kasbi tumani",
            "kitob": "Kitob tumani",
            "mirishkor": "Mirishkor tumani",
            "muborak": "Muborak tumani",
            "nishon": "Nishon tumani",
            "shahrisabz": "Shahrisabz tumani",
            "yakkabog": "Yakkabogʻ tumani",
            "kokdala": "Koʻkdala tumani",
        },
    },
    "samarqand": {
        "name": "Samarqand viloyati",
        "districts": {
            "bulungur": "Bulungʻur tumani",
            "ishtixon": "Ishtixon tumani",
            "jomboy": "Jomboy tumani",
            "kattaqorgon": "Kattaqoʻrgʻon tumani",
            "qoshrabot": "Qoʻshrabot tumani",
            "narpay": "Narpay tumani",
            "nurobod": "Nurobod tumani",
            "oqdaryo": "Oqdaryo tumani",
            "paxtachi": "Paxtachi tumani",
            "payariq": "Payariq tumani",
            "pastdargom": "Pastdargʻom tumani",
            "samarqand": "Samarqand tumani",
            "toyloq": "Toyloq tumani",
            "urgut": "Urgut tumani",
        },
    },
    "sirdaryo": {
        "name": "Sirdaryo viloyati",
        "districts": {
            "oqoltin": "Oqoltin tumani",
            "boyovut": "Boyovut tumani",
            "guliston": "Guliston tumani",
            "xovos": "Xovos tumani",
            "mirzaobod": "Mirzaobod tumani",
            "sardoba": "Sardoba tumani",
            "sayxunobod": "Sayxunobod tumani",
            "sirdaryo": "Sirdaryo tumani",
        },
    },
    "surxondaryo": {
        "name": "Surxondaryo viloyati",
        "districts": {
            "angor": "Angor tumani",
            "bandixon": "Bandixon tumani",
            "boysun": "Boysun tumani",
            "denov": "Denov tumani",
            "jarqorgon": "Jarqoʻrgʻon tumani",
            "qiziriq": "Qiziriq tumani",
            "qumqorgon": "Qumqoʻrgʻon tumani",
            "muzrabot": "Muzrabot tumani",
            "oltinsoy": "Oltinsoy tumani",
            "sariosiyo": "Sariosiyo tumani",
            "sherobod": "Sherobod tumani",
            "shorchi": "Shoʻrchi tumani",
            "termiz": "Termiz tumani",
            "uzun": "Uzun tumani",
        },
    },
    "toshkent": {
        "name": "Toshkent viloyati",
        "districts": {
            "bekobod": "Bekobod tumani",
            "bostonliq": "Boʻstonliq tumani",
            "boka": "Boʻka tumani",
            "chinoz": "Chinoz tumani",
            "qibray": "Qibray tumani",
            "ohangaron": "Ohangaron tumani",
            "oqqorgon": "Oqqoʻrgʻon tumani",
            "parkent": "Parkent tumani",
            "piskent": "Piskent tumani",
            "quyichirchiq": "Quyichirchiq tumani",
            "zangiota": "Zangiota tumani",
            "ortachirchiq": "Oʻrtachirchiq tumani",
            "yangiyol": "Yangiyoʻl tumani",
            "yuqorichirchiq": "Yuqorichirchiq tumani",
            "toshkent_tumani": "Toshkent tumani",
        },
    },
    "xorazm": {
        "name": "Xorazm viloyati",
        "districts": {
            "bogot": "Bogʻot tumani",
            "gurlan": "Gurlan tumani",
            "xonqa": "Xonqa tumani",
            "hazorasp": "Hazorasp tumani",
            "xiva": "Xiva tumani",
            "qoshkopir": "Qoʻshkoʻpir tumani",
            "shovot": "Shovot tumani",
            "urganch": "Urganch tumani",
            "yangiariq": "Yangiariq tumani",
            "yangibozor": "Yangibozor tumani",
            "tuproqqala": "Tuproqqalʼa tumani",
        },
    },
}


def make_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Viloyatlar")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def make_regions_keyboard():
    builder = InlineKeyboardBuilder()
    for region_key, data in REGIONS.items():
        builder.button(text=data["name"], callback_data=f"region:{region_key}")
    builder.adjust(2)
    return builder.as_markup()


def make_districts_keyboard(region_key: str):
    builder = InlineKeyboardBuilder()
    for district_key, district_name in REGIONS[region_key]["districts"].items():
        builder.button(
            text=district_name,
            callback_data=f"district:{region_key}:{district_key}"
        )
    builder.button(text="⬅️ Orqaga", callback_data="back:regions")
    builder.adjust(2)
    return builder.as_markup()


def make_back_keyboard(region_key: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Shu viloyat tumanlariga qaytish", callback_data=f"region:{region_key}")
    builder.button(text="🏠 Viloyatlarga qaytish", callback_data="back:regions")
    builder.adjust(1)
    return builder.as_markup()


def get_region_photo(region_key: str):
    return f"images/regions/{region_key}.jpg"


def get_district_photo(region_key: str, district_key: str):
    return f"images/districts/{region_key}/{district_key}.jpg"


async def send_photo_or_text(message: Message, photo_path: str, text: str, reply_markup=None):
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo, caption=text, reply_markup=reply_markup)
    else:
        await message.answer(text, reply_markup=reply_markup)


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Salom. Kerakli bo‘limni tanlang:",
        reply_markup=make_main_menu()
    )


@router.message(F.text == "Viloyatlar")
async def regions_handler(message: Message):
    await message.answer(
        "12 ta viloyatdan birini tanlang:",
        reply_markup=make_regions_keyboard()
    )


@router.callback_query(F.data == "back:regions")
async def back_regions_handler(callback: CallbackQuery):
    await callback.message.answer(
        "12 ta viloyatdan birini tanlang:",
        reply_markup=make_regions_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("region:"))
async def region_handler(callback: CallbackQuery):
    region_key = callback.data.split(":")[1]

    if region_key not in REGIONS:
        await callback.answer("Viloyat topilmadi", show_alert=True)
        return

    region_name = REGIONS[region_key]["name"]
    district_count = len(REGIONS[region_key]["districts"])
    text = (
        f"{region_name}\n\n"
        f"Tumanlar soni: {district_count}\n"
        f"Kerakli tumanni tanlang."
    )

    await send_photo_or_text(
        callback.message,
        get_region_photo(region_key),
        text,
        reply_markup=make_districts_keyboard(region_key)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("district:"))
async def district_handler(callback: CallbackQuery):
    _, region_key, district_key = callback.data.split(":")

    if region_key not in REGIONS:
        await callback.answer("Viloyat topilmadi", show_alert=True)
        return

    district_name = REGIONS[region_key]["districts"].get(district_key)
    if not district_name:
        await callback.answer("Tuman topilmadi", show_alert=True)
        return

    region_name = REGIONS[region_key]["name"]
    text = (
        f"{district_name}\n"
        f"Viloyat: {region_name}\n\n"
        f"Bu joyga o‘zing tumanga oid matn yozib qo‘yasan.\n"
        f"Rasm bo‘lsa: images/districts/{region_key}/{district_key}.jpg"
    )

    await send_photo_or_text(
        callback.message,
        get_district_photo(region_key, district_key),
        text,
        reply_markup=make_back_keyboard(region_key)
    )
    await callback.answer()


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
