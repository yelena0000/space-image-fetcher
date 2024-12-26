import telegram
from environs import Env

env = Env()
env.read_env()

token=env.str('TG_BOT_TOKEN')
bot = telegram.Bot(token)

bot.send_message(text='Hello everyone!', chat_id='@space_collecti0n')