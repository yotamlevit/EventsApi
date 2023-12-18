import logging
import json


def log(level: int, msg: str,
        http_code: int = 0,
        response: str = "",
        error: Exception = None,
        payload: str = ""):
    logging.log(level, msg, extra={
        "http_code": http_code,
        "response": json.dumps(response),
        "error": error.with_traceback(None) if error else None,
        "payload": payload
    })


def debug(msg: str,
          http_code: int = 0,
          response: str = "",
          error: Exception = None,
          payload: str = ""):
    log(logging.DEBUG, msg, http_code, response, error, payload)


def info(msg: str,
         http_code: int = 0,
         response: str = "",
         error: Exception = None,
         payload: str = ""):
    log(logging.INFO, msg, http_code, response, error, payload)


def warning(msg: str,
            http_code: int = 0,
            response: str = "",
            error: Exception = None,
            payload: str = ""):
    log(logging.WARNING, msg, http_code, response, error, payload)


def error(msg: str,
          http_code: int = 0,
          response: str = "",
          error: Exception = None,
          payload: str = ""):
    log(logging.ERROR, msg, http_code, response, error, payload)


def fatal(msg: str,
          http_code: int = 0,
          response: str = "",
          error: Exception = None,
          payload: str = ""):
    log(logging.FATAL, msg, http_code, response, error, payload)
