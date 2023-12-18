import logging
import json
import traceback


class JsonFormatter(logging.Formatter):
    def __init__(self, datafmt):
        self._datafmt = {"message": "message", "@timestamp": "asctime", "level": "levelname"}
        super().__init__(datafmt)

    def formatMessage(self, record) -> dict:
        return {format_key: record.__dict__[format_value] for format_key, format_value in self._datafmt.items()}

    def format(self, record):
        record.message = record.getMessage()

        message_dict = self.formatMessage(record)

        message_dict["http_code"] = self.__extract_parameters(record, "http_code")
        message_dict["response"] = self.__extract_parameters(record, "response")
        message_dict["error"] = self.__extract_parameters(record, "error")
        message_dict["payload"] = self.__extract_parameters(record, "payload")

        return json.dumps(message_dict, default=str)


    @classmethod
    def __extract_parameters(cls, record, param_key) -> str:
        param_value = record.__dict__.get(param_key)

        if isinstance(type(param_value), Exception):
            return f'{param_value} {traceback.format_exc()}'

        if param_value:
            return f'param_value'

        return ""