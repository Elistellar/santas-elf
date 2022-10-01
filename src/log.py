import logging

# add SQL log level and Logger.sql() method.
logging.SQL = 15
logging.addLevelName(logging.SQL, "SQL")

def _sql(logger, message, *args, **kwargs):
    if logger.isEnabledFor(logging.SQL):
        logger._log(logging.SQL, message, args, **kwargs)

logging.Logger.sql = _sql

# logger initialization
from datetime import datetime
from .file_manager import path


log = logging.getLogger('axolotl')
log.setLevel(logging.SQL)

filename = datetime.now().strftime('%Y-%m-%d %Hh%M.log')
handler = logging.FileHandler(path('logs/' + filename), encoding='utf-8')
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(message)s',
    '%H:%M:%S'
))
log.addHandler(handler)
