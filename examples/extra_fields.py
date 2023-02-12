import logging
import socket # for get hostname amd ip

from non_blocking_http_handler.handler import NonBlockingHttpHandler


log = logging.getLogger('test')


httpHandler = NonBlockingHttpHandler(
    url='http://localhost:5000/logs',
    max_workers=5,
    max_retries=3,
    extra={
        'hostname': socket.gethostname()
    }
)


httpHandler.setLevel(logging.WARNING)
log.addHandler(httpHandler)


def main():
    # sending logs

    log.debug("a")
    log.info("b")
    log.warning("c")

    try:
        1 / 0
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    main()
