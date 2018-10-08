import config
import logging
import os.path

fh_logger = logging.getLogger("FileHandler")


class FileHandler:

    def __init__(self, filename=config.FILENAME):
        self.filename = filename

    @staticmethod
    def file_exists(filename=config.FILENAME):
        return os.path.exists(filename)

    def write_to_text_file(self, content):
        # Writes regardless of a file pre-existing
        with open(self.filename, mode='w') as a_file:
            a_file.write(content)
            a_file.close()
            fh_logger.debug("Successfully written {} to file".format(content))
            return True
        return False

    def read_from_text_file(self):
        # Use case is to read the id from the file
        # We use this id later as an int.
        content = ""
        try:
            with open(self.filename) as a_file:
                content = a_file.read()
                a_file.close()
        except FileNotFoundError:
            fh_logger.error(
                'File {} does not exist.\n Exiting...'.format(self.filename))
            raise
        return int(content)
