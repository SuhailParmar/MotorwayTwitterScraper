import config
import pytest
from file_handler import FileHandler


class TestFileHandlerTests:
    
    fh = FileHandler()

    def test_file_not_found(self):
        fh2 = FileHandler("doesnt_exist.txt")
        with pytest.raises(FileNotFoundError):
            fh2.read_id_from_file()

    def test_write_a_to_file(self):
        assert self.fh.write_id_to_file('100029019209')

    def test_read_int_from_file(self):
        assert self.fh.read_id_from_file() == 100029019209
        assert self.fh.read_id_from_file() != '100029019209'

    def test_cleanup_file(self):
        assert self.fh.clean_up_file()
