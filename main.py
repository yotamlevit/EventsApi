from App import app
from threading import Thread
from BL.EventReminder import run_reminder_thread
import logging


logger = logging.getLogger("uvicorn")
logger.propagate = False

Thread(target=run_reminder_thread).start()
app = app()