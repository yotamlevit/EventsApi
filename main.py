from App import app
import logging


logger = logging.getLogger("uvicorn")
logger.propagate = False

app = app()