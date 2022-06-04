import logging
import asyncio

from aiogram import executor
from app import main

# from app import dp

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    # executor.start_polling(dp, skip_updates=True)