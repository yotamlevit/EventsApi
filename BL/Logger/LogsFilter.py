import logging


class NonRootLogsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.name == "root"