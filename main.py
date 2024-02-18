from aiogram import Bot,Dispatcher
from aiogram.dispatcher.filters import CommandStart,Command
from bot_config import BOT_TOKEN
from prices import get_BTC_price, get_USDT_price, get_RUB_price
import logging
from aiogram import types
import asyncio
import datetime

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(CommandStart())
async def start_message(message:types.Message):
    await message.answer(text=f"""Привет, {message.from_user.full_name}!
                         \nЭто бот для отправки цены 1 BTC к USD
                         \nДля получения информации по актуальному курсу BTC и USDT напишите\n/now\n больше информации в /help""")
    
@dp.message_handler(Command("help"))
async def help_message(message:types.Message):
    text = "Бот знает следующие команды:\n/start - запуск бота\n/now - показывает текущий курс биткоина и доллара\n/set_price - установка таргетного значения"
    
    await message.answer(text=text)

@dp.message_handler(Command("now"))
async def send_current_price(message:types.Message):
        BTC_price = float(get_BTC_price().replace(",",""))
        USDT_price = float(get_USDT_price().replace(",",""))
        await message.answer(f"Цена 1 BTC к USD: {round(BTC_price,ndigits=2)}")
        await message.answer(f"Цена 1 USDT к рублю: {round(USDT_price * get_RUB_price(),ndigits=2)}")
     

@dp.message_handler(Command("set_price"))
async def ask_target_price(message:types.Message):
    await message.answer(""""Введите значения следующим сообщением
                         max
                         min""")

@dp.message_handler()
async def set_target_price(message:types.Message):
    if len(message.text.split("\n")) == 2:
        max_value = message.text.split("\n")[0]
        min_value = message.text.split("\n")[1]
    else:
        await message.answer("Неправильно введены значения")
        
    if max_value.isdigit() and min_value.isdigit():
        await message.answer(f"Установлены следующие значения, max:{max_value}, min: {min_value}\nИнформация по курсу обновляется раз в 5 минут")
    else:
        await message.answer(f"Введено неправильно значение")
    
    
    time_checker = {"minutes":[i for i in range(0,61,5)],
                    "hours":[i for i in range(0,24,1)]}

    while datetime.datetime.now().minute:
        curr = datetime.datetime.now().minute
        
        if curr in time_checker["minutes"]:
            
            if float(max_value) <= float(get_BTC_price().replace(",","")):
                await message.answer(f"Цена BTC превысила порог в {max_value}")
                break

            elif float(min_value) >= float(get_BTC_price().replace(",","")):
                await message.answer(f"Цена BTC опустилась ниже {min_value}")
                break
            
            else:
                continue
        
        else:
            continue


@dp.message_handler()
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())