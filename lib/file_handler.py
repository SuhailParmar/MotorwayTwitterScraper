import logging
from os import path
from os import remove
import lib.config as config


fh_logger = logging.getLogger("FileHandler")


class FileHandler:

    def __init__(self, filename=config.FILENAME):
        self.filename = filename

    @staticmethod
    def file_exists(filename=config.FILENAME):
        return path.exists(filename)

    def write_id_to_file(self, id):
        # Writes regardless of a file pre-existing
        id = str(id)  # Can't write an int to file
        with open(self.filename, mode='w') as a_file:
            a_file.write(id)
            a_file.close()
            fh_logger.debug("Successfully written {} to file".format(id))
            return True
        return False

    def read_id_from_file(self):
        try:
            with open(self.filename) as a_file:
                content = a_file.read()
                a_file.close()
        except FileNotFoundError:
            fh_logger.error(
                'File {} does not exist.\n Exiting...'.format(self.filename))
            raise
        # The ID is used throughout the application as an integer
        return int(content)

    def clean_up_file(self):
        try:
            remove(self.filename)
            fh_logger.info('Removed file {}'.format(self.filename))
            return True
        except Exception:
            fh_logger.warn('Couldn\'t remove file {}'.format(self.filename))
            return False
