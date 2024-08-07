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
        print(log_message)
        if 'NO MANIPULATION' in log_message:
            return 'NO MANIPULATION'
        elif 'MANIPULATION!!!!!' in log_message:
            return 'MANIPULATION!!!!!'
        else:
            return 'Unknown Status'

    def extract_ACEEI_data(self):
        log_message = self.get_logs()  # Capture logs before resetting
        result_lines = []

        # Extract lines starting with "final budget b*" or "final prices p*"
        for line in log_message.splitlines():
            if line.startswith("final budget b*") or line.startswith("final prices p*"):
                result_lines.append(line)

        # After processing, reset the log stream to clear processed logs
        self.log_stream.seek(0)
        self.log_stream.truncate(0)

        print("result_lines: ", result_lines)
        print("_________________________________")

        return '\n'.join(result_lines)

    def extract_tabu_search_data(self):
        log_message = self.get_logs()  # Capture logs before resetting
        result_lines = []

        # Extract lines starting with "final budget b*" or "final prices p*"
        for line in log_message.splitlines():
            if line.startswith("final prices p*"):
                result_lines.append(line)

        # After processing, reset the log stream to clear processed logs
        self.log_stream.seek(0)
        self.log_stream.truncate(0)

        print("result_lines: ", result_lines)
        print("_________________________________")

        return '\n'.join(result_lines)

