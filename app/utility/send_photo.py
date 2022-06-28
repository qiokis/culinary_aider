from app import bot


async def send_photo(chat_id, photo_path):
    if photo_path:
        photo = open(f'static/{photo_path}', 'rb')
        await bot.send_photo(chat_id=chat_id, photo=photo)
