import sys
import json
import logging

from urllib import request
from concurrent import futures


class NonBlockingHttpHandler(logging.Handler):
    def __init__(self, url: str, max_workers: int, max_retries: int = 0, extra: dict = {}):
        self.url = url
        self.executor = futures.ThreadPoolExecutor(max_workers=max_workers)
        self.max_retries = max_retries
        self.extra = extra

        super().__init__()

    def emit(self, record):
        self.executor.submit(custom_emit, self, record)


def custom_emit(self, record):
    req_body = {
        'level': record.levelname,
        'message': record.getMessage(),
        'timestamp': record.created,
        'line': record.lineno,
        'file': record.filename,
    }

    if self.extra:
        req_body.update(self.extra)

    # encode json data
    json_data = json.dumps(req_body)
    json_data_b = json_data.encode('utf-8')  # needs to be bytes

    req = request.Request(self.url)

    # add headers
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(json_data_b))

    try:
        # make the request
        response = request.urlopen(req, json_data_b)
    except Exception as e:
        print(f"Failed to send log to server {e}. Printing log data: {json_data}", flush=True, file=sys.stderr)
        return

    ok = True
    if response.status >= 400:
        ok = False
        for retry in range(self.max_retries):
            try:
                response = request.urlopen(req, json_data_b)
            except Exception as e:
                print(f"Failed to send log to server {e}. Printing log data: {json_data}", flush=True, file=sys.stderr)
                return
            if response.status < 400:
                ok = True
                break

    if not ok:
        print(f"Failed to send log to server {response.status}. Printing log data: {json_data}", flush=True,
              file=sys.stderr)
