import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

TOKEN = os.getenv("8631386176:AAGZ0OpS21IuoM2VJU_uUYyOnHjWkpq_56g")

router = Router()

REGIONS = {
    "andijon": {
        "name": "Andijon viloyati",
        "districts": {
            "andijon": "Andijon tumani",
            "asaka": "Asaka tumani",
        },
    },
    "samarqand": {
        "name": "Samarqand viloyati",
        "districts": {
            "urgut": "Urgut tumani",
            "jomboy": "Jomboy tumani",
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
        builder.button(text=district_name, callback_data=f"district:{region_key}:{district_key}")
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
        await message.answer_photo(
            photo=FSInputFile(photo_path),
            caption=text,
            reply_markup=reply_markup
        )
    else:
        await message.answer(text, reply_markup=reply_markup)


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Salom. Kerakli bo‘limni tanlang:", reply_markup=make_main_menu())


@router.message(F.text == "Viloyatlar")
async def regions_handler(message: Message):
    await message.answer("Viloyatni tanlang:", reply_markup=make_regions_keyboard())


@router.callback_query(F.data == "back:regions")
async def back_regions_handler(callback: CallbackQuery):
    await callback.message.answer("Viloyatni tanlang:", reply_markup=make_regions_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("region:"))
async def region_handler(callback: CallbackQuery):
    region_key = callback.data.split(":")[1]

    if region_key not in REGIONS:
        await callback.answer("Viloyat topilmadi", show_alert=True)
        return

    region_name = REGIONS[region_key]["name"]
    text = f"{region_name}\n\nKerakli tumanni tanlang."

    await send_photo_or_text(
        callback.message,
        get_region_photo(region_key),
        text,
        make_districts_keyboard(region_key)
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

    text = f"{district_name}\nViloyat: {REGIONS[region_key]['name']}"

    await send_photo_or_text(
        callback.message,
        get_district_photo(region_key, district_key),
        text,
        make_back_keyboard(region_key)
    )
    await callback.answer()


async def main():
    logging.basicConfig(level=logging.INFO)

    if not TOKEN:
        raise ValueError("BOT_TOKEN topilmadi")

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
