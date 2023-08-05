import logging


class ln():

    def __init__(self, origin=None, toscreen=True, tofile=None) -> None:
        logging.getLogger().handlers = []
        self.logger = logging.getLogger(origin)  # configure `root` logger when no arguments passed

        self.logger.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(asctime)s[%(filename)s:%(lineno)d]: %(message)s', datefmt='[%m-%d %H:%M:%S]')
        # formatter = logging.Formatter('%(message)s', datefmt='[%m-%d %H:%M:%S]')
        formatter = logging.Formatter("[%(asctime)s %(process)d] %(message)s")

        if toscreen:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        if tofile is not None:
            fh = logging.FileHandler(tofile)
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)


    def get_logger(self):
        return self.logger

    def debug(self, output):
        self.logger.debug(output)

    def info(self, output):
        self.logger.info(output)

    def warning(self, output):
        self.logger.warning(output)

    def error(self, output):
        self.logger.error(output)


if __name__ == '__main__':
    log = ln(__name__, toscreen=True, tofile='trainer.log').get_logger()
    log.info('no')
