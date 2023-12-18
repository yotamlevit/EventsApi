import logging
import json
import traceback


class JsonFormatter(logging.Formatter):
    def __init__(self, datefmt: str):
        self.dictfmt = {"@timestamp": "asctime", "level": "levelname", "message": "message"}
        self.extra_params = ["http_code", "response", "error", "payload"]
        super().__init__(datefmt=datefmt)

    def formatMessage(self, record: logging.LogRecord) -> dict:
        return {format_key: record.__dict__[format_value] for format_key, format_value in self.dictfmt.items()}

    def format(self, record: logging.LogRecord):
        record.message = record.getMessage()
        record.asctime = self.formatTime(record)

        message_dict = self.formatMessage(record)

        self.__add_extra_parameters(record, message_dict)

        return json.dumps(message_dict, default=str)

    def __add_extra_parameters(self, record, message_dict: dict):
        for param in self.extra_params:
            param_value = self.__extract_parameters(record, param)
            if param_value:
                message_dict[param] = param_value

    @classmethod
    def __extract_parameters(cls, record: logging.LogRecord, param_key: str) -> str:
        param_value = record.__dict__.get(param_key)

        if isinstance(type(param_value), Exception):
            return f'{param_value} {traceback.format_exc()}'

        if param_value and param_value != '""':
            return f'{param_value}'

        return ""