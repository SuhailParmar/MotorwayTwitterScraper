import logging
import config

'''
The logger will write to a file alongside stdout.
Once initiated the 'logger' becomes global.
'''


class Logger:

    @staticmethod
    def initiate_logger():

        console_logging_format =\
            '%(asctime)s %(name)s [%(levelname)s]: %(message)s'

        logging.basicConfig(level=logging.DEBUG,
                            filename=config.log_file,
                            format='%(asctime)s [%(levelname)s]: %(message)s',
                            datefmt='%Y-%m-%dT%H:%M:%S')

        console_logger = logging.StreamHandler()  # Handler to write to stdout
        console_logger.name = 'MotorwayScraper'
        console_logger.setLevel(logging.INFO)
        console_format = logging.Formatter(
            console_logging_format, datefmt='%Y-%m-%dT%H:%M:%S')
        console_logger.setFormatter(console_format)

        # or, disable propagation
        logging.getLogger("pika").propagate = False
        logging.getLogger('').addHandler(console_logger)
        logging.getLogger("requests").setLevel(logging.WARNING)
