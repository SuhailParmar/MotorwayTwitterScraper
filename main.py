import logging
from time import sleep
import lib.config as config

from lib.logger import Logger
from lib.scraper import Scraper
from lib.tweet import Tweet


main_logger = logging.getLogger("Main")


def main():
    if not isinstance(config.period, int):
        main_logger.info('Period ENV variable needs to be an Integer.')
        exit(1)
    sc = Scraper()

    while True:
        try:
            sc.scrape()
            main_logger.info('Finsihed scraping.')
            main_logger.info('Halting for {} seconds.'.format(config.period))
            sleep(config.period)
        except KeyboardInterrupt:
            main_logger.info('Finished Scraper.')
            exit(1)

if __name__ == "__main__":
    main()
