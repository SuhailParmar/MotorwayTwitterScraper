import config
import pytest
from file_handler import FileHandler


class TestFileHandlerTests:

    def test_file_not_found(self):
        fh = FileHandler("doesnt_exist.txt")
        with pytest.raises(FileNotFoundError):
            fh.read_from_text_file()

    def test_write_a_to_file(self):
        fh = FileHandler()
        assert fh.write_to_text_file('100029019209')

    def test_read_int_from_file(self):
        fh = FileHandler()
        assert fh.read_from_text_file() == 100029019209
        assert fh.read_from_text_file() != '100029019209'
