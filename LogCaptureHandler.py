import logging
from io import StringIO


class LogCaptureHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_capture_string = StringIO()
        self.setFormatter(logging.Formatter('%(message)s'))

    def emit(self, record):
        message = self.format(record)
        if "final budget b*" in message or "final prices p*" in message:
            self.log_capture_string.write(message + '\n')

    def get_logs(self):
        return self.log_capture_string.getvalue()