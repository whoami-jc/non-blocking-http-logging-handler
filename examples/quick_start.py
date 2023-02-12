


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
