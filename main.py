import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types

from handlers import holiday_today, holiday_yesterday, holiday_tomorrow, callbackHandler



# Logger initialization and logging level setting
log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOGGING_LEVEL', 'INFO').upper())


# Handlers
async def start(message: types.Message):
    await message.reply('Can\'t wait to see what holiday is today!')


# AWS Lambda funcs
async def register_handlers(dp: Dispatcher):
    """Registration all handlers before processing update."""

    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(holiday_today.cmd_holiday, commands=['holiday'])
    dp.register_message_handler(holiday_tomorrow.cmd_holidayTomorrow, commands=['holiday_tomorrow'])
    dp.register_message_handler(holiday_yesterday.cmd_holidayYesterday, commands=['holiday_yesterday'])
    dp.register_callback_query_handler(callbackHandler.callbackHandler, lambda callback_query: True)


    log.debug('Handlers are registered.')


async def process_event(event, dp: Dispatcher):
    """
    Converting an AWS Lambda event to an update and handling that
    update.
    """

    log.debug('Update: ' + str(event))

    Bot.set_current(dp.bot)
    update = types.Update.to_object(event)
    await dp.process_update(update)


async def main(event):
    """
    Asynchronous wrapper for initializing the bot and dispatcher,
    and launching subsequent functions.
    """

    # Bot and dispatcher initialization
    bot = Bot(os.environ.get('TOKEN'))
    dp = Dispatcher(bot)

    await register_handlers(dp)
    await process_event(event, dp)

    return 'ok'


def lambda_handler(event, context):
    """AWS Lambda handler."""

    return asyncio.get_event_loop().run_until_complete(main(event))
