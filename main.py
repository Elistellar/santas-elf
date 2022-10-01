import traceback

# Logger
from src.log import log

log.info('Starting Axolotl ...')

try:
    # Config
    from src.config import Config

    Config.load()

    # Database
    from src.database import Database

    Database.init()

    # Bot
    from src.bot import bot

    bot.run(Config["token"])

except:
    log.error(traceback.format_exc())
