import logging
from io import StringIO


# Set up a custom logging handler to capture log messages
class LogCaptureHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_stream = StringIO()

    def emit(self, record):
        self.log_stream.write(self.format(record) + '\n')

    def get_logs(self):
        return self.log_stream.getvalue()

    def extract_manipulation_status(self):
        log_message = self.get_logs()
        if 'NO MENIPULATION' in log_message:
            return 'NO MENIPULATION'
        elif 'MENIPULATION!!!!!' in log_message:
            return 'MENIPULATION!!!!!'
        else:
            return 'Unknown Status'