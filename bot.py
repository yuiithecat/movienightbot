import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

FILMS_FILE = "films.txt"


def get_items(item_type=None):
    if not os.path.exists(FILMS_FILE):
        return []

    items = []
    with open(FILMS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            t, title = line.split("|", 1)
            if item_type is None or t == item_type:
                items.append(title)

    return items


def add_item(item_type, title):
    with open(FILMS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{item_type}|{title}\n")


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        "🎬 Случайный фильм",
        "🧸 Случайный мультфильм"
    )
    keyboard.add(
        "🍝 Рестики",          # NEW
        "🎪 Прочее"            # NEW
    )

    await message.answer(
        "Кошечка, присылай сюда:\n\n"
        "ф название фильма 🎬\n"
        "м название мультфильма 🧸\n"
        "р название рестика 🍝\n"
        "п любые прочие планы и хотелки 🎪\n\n"
        "А бот всё сохранит 💾\n\n"
        "ps ты секси",
        reply_markup=keyboard
    )


@dp.message_handler(lambda m: m.text == "🎬 Случайный фильм")
async def random_film(message: types.Message):
    films = get_items("ф")
    if not films:
        await message.answer("Фильмов пока нет 😢")
        return
    await message.answer(f"Сегодня смотрим: 🎬 {random.choice(films)}")


@dp.message_handler(lambda m: m.text == "🧸 Случайный мультфильм")
async def random_cartoon(message: types.Message):
    cartoons = get_items("м")
    if not cartoons:
        await message.answer("Мультфильмов пока нет 😢")
        return
    await message.answer(f"Сегодня смотрим: 🧸 {random.choice(cartoons)}")


# NEW — список рестиков
@dp.message_handler(lambda m: m.text == "🍝 Рестики")
async def list_restaurants(message: types.Message):
    restaurants = get_items("р")
    if not restaurants:
        await message.answer("Список рестиков пуст 🍝")
        return

    text = "🍝 Рестики:\n\n" + "\n".join(
        f"{i+1}. {name}" for i, name in enumerate(restaurants)
    )
    await message.answer(text)


# NEW — список прочего
@dp.message_handler(lambda m: m.text == "🎪 Прочее")
async def list_other(message: types.Message):
    other = get_items("п")
    if not other:
        await message.answer("Прочее пока пусто 🎪")
        return

    text = "🎪 Прочее:\n\n" + "\n".join(
        f"{i+1}. {name}" for i, name in enumerate(other)
    )
    await message.answer(text)


@dp.message_handler()
async def add_item_handler(message: types.Message):
    text = message.text.strip()

    if not (
        text.startswith("ф ")
        or text.startswith("м ")
        or text.startswith("р ")   # NEW
        or text.startswith("п ")   # NEW
    ):
        await message.answer(
            "Кошечка, формат такой:\n\n"
            "ф фильм\n"
            "м мультфильм\n"
            "р рестик\n"
            "п прочее"
        )
        return

    item_type = text[0]
    title = text[2:].strip()

    if not title:
        await message.answer("Название пустое :(")
        return

    add_item(item_type, title)
    if item_type == "р":
        await message.answer("🍝 Рестик добавлен! Ты, конечно, невероятно сладкая лисичка")
    elif item_type == "п":
        await message.answer("🎪 Есть! Кстати, детка, ты просто отпад 🦄")
    elif item_type == "ф":
        await message.answer("🎬 Фильм в списке! Хочется чего-то сладенького..тебя, например?")
    elif item_type == "м":
        await message.answer("🧸 Мульт добавлен! Кошечка, ты супер хот")


if __name__ == "__main__":
    executor.start_polling(dp)
