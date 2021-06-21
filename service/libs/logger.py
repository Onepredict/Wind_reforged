import logging
import logging.config
import os

from logging import Formatter
from logging.handlers import RotatingFileHandler

appname = None


class Logger:
    _app = None
    _file_path = None
    _file_size = 104857600
    _file_count = 10
    _logger_name = None
    _basic_config = {"version": 1, "disable_existing_loggers": True}

    def __init__(self, app, logger_name):
        self._app = app
        self._file_path = os.path.join(self._app.root_path, "log")

        global appname
        appname = logger_name

        print("Log files will be stored in {file_path}".format(file_path=self._file_path))

        if not os.path.exists(self._file_path):
            os.makedirs(self._file_path)

        self._initialize()

    def _initialize(self):
        _logger = self._app.logger

        _logger.setLevel(logging.INFO)
        format_string = "%(asctime)s [%(landscape)s][%(requestid)s][%(serviceid)s] %(levelname)s [%(funcname)s:%(flineno)s] %(message)s"
        _formatter = Formatter(format_string)
        # _logger.handlers[0].setFormatter(_formatter)
        # _logger.handlers[0].setLevel(logging.INFO)

        import os

        h_file = RotatingFileHandler(
            filename=os.path.join(self._file_path, "trace.log"),
            mode="a",
            maxBytes=self._file_size,
            encoding="utf8",
            delay=False,
            backupCount=self._file_count,
        )
        h_file.setFormatter(_formatter)
        h_file.setLevel(logging.DEBUG)
        _logger.addHandler(h_file)

        import logmatic  # https://github.com/logmatic/logmatic-python

        import os

        json_file = RotatingFileHandler(
            filename=os.path.join(self._file_path, "service.log"),
            mode="a",
            maxBytes=self._file_size / 10,
            encoding="utf8",
            delay=False,
            backupCount=self._file_count,
        )
        _json_formatter = logmatic.JsonFormatter()
        json_file.setFormatter(_json_formatter)
        json_file.setLevel(logging.DEBUG)
        _logger.addHandler(json_file)

        import sys
        from logging import StreamHandler

        h_stdout = StreamHandler(sys.stdout)
        h_stdout.setFormatter(_formatter)
        h_stdout.setLevel(logging.DEBUG)
        _logger.addHandler(h_stdout)


def _process():
    import inspect

    func = inspect.currentframe()
    back_func = func.f_back
    import os

    (path, filename) = os.path.split(back_func.f_back.f_code.co_filename)

    landscape_name = ""
    request_id = ""
    service_id = ""

    import threading

    thread_local = threading.current_thread()
    if thread_local and hasattr(thread_local, "landscape_name"):
        landscape_name = thread_local.landscape_name
    if thread_local and hasattr(thread_local, "request_id"):
        request_id = thread_local.request_id
    if thread_local and hasattr(thread_local, "service_id"):
        service_id = thread_local.service_id
    if thread_local and hasattr(thread_local, "monitor_id"):
        service_id = thread_local.monitor_id

    extra = {
        "fname": filename,
        "funcname": back_func.f_back.f_code.co_name,
        "flineno": back_func.f_back.f_lineno,
        "landscape": landscape_name,
        "requestid": request_id,
        "serviceid": service_id,
    }

    _adapter = logging.LoggerAdapter(logging.getLogger(appname), extra=extra)

    return _adapter


def debug(message):
    _process().debug(message)


def info(message):
    _process().info(message)


def warning(message):
    _process().warning(message)


def error(message):
    _process().error(_call_stack(message))


def critical(message):
    _process().error(_call_stack(message))


def _process_req_ext(
    req_method,
    req_url,
    req_header,
    req_param,
    req_body,
    req_callee,
    req_is_success,
    resp_status_code,
    resp_header,
    resp_body,
    elapsed_time_sec,
):
    import inspect

    func = inspect.currentframe()
    back_func = func.f_back
    import os

    (path, filename) = os.path.split(back_func.f_back.f_code.co_filename)

    landscape_name = ""
    request_id = ""
    service_id = ""

    import threading

    thread_local = threading.current_thread()
    if thread_local and hasattr(thread_local, "landscape_name"):
        landscape_name = thread_local.landscape_name
    if thread_local and hasattr(thread_local, "request_id"):
        request_id = thread_local.request_id
    if thread_local and hasattr(thread_local, "service_id"):
        service_id = thread_local.service_id

    extra = {
        "fname": filename,
        "funcname": back_func.f_back.f_code.co_name,
        "flineno": back_func.f_back.f_lineno,
        "landscape": landscape_name,
        "requestid": request_id,
        "serviceid": service_id,
        "req_method": req_method,
        "req_url": req_url,
        "req_header": req_header,
        "req_param": req_param,
        "req_body": req_body,
        "req_callee": req_callee,
        "req_is_success": req_is_success,
        "resp_status_code": resp_status_code,
        "resp_header": resp_header,
        "resp_body": resp_body,
        "elapsed_time_sec": elapsed_time_sec,
    }

    _adapter = logging.LoggerAdapter(logging.getLogger("flask_app"), extra=extra)
    return _adapter


def debug_req_ext(
    req_method,
    req_url,
    req_header,
    req_param,
    req_body,
    req_callee,
    req_is_success,
    resp_status_code,
    resp_header,
    resp_body,
    elapsed_time_sec,
    message,
):
    _process_req_ext(
        req_method,
        req_url,
        req_header,
        req_param,
        req_body,
        req_callee,
        req_is_success,
        resp_status_code,
        resp_header,
        resp_body,
        elapsed_time_sec,
    ).debug(message)


def _call_stack(message):
    import inspect

    full_stack = ""
    current_frame = inspect.currentframe()
    frame = current_frame.f_back
    i = 0
    while frame:
        temp = frame.f_code
        str_line = "%d: %s, line:%s in %s\n " % (i, temp.co_filename, temp.co_firstlineno, temp.co_name)
        full_stack += str_line
        frame = frame.f_back
        i += 1

    stack_message = "{} \n StackTrace \n {}".format(message, full_stack)

    return stack_message