import pytest
import unittest
from unittest.mock import patch, mock_open
from os import stat_result
from pathlib import Path
import builtins
from keiconf import KeiConf
import json

'''
I'm terrible at writing tests in python, sorry
'''

class TestKeiConf(unittest.TestCase):
    '''
    __init__ notes: 
    
    # checks Path.is_dir
    # if not Path.is_file()
        # runs Path.mkdir 
        # runs Path.write_text
    # with open filepath
        # json load
    '''
    file_content_mock = """
    {
        "a_key": "a_value",
        "b_key": {
            "subkey": "subvalue"
        }
    }
    """
    file_path_mock = '/fake/path/to/file.json'
    file_dir_mock = '/fake/path/to'
    
    # these should be configured to fail after the test
    # in case it somehow doesn't raise 
    def test_init_with_int_filename(self):
        with pytest.raises(TypeError):
            k = KeiConf(filepath=1)
    
    def test_init_with_bool_filename(self):
        with pytest.raises(TypeError):
            k = KeiConf(filepath=True)

    def test_init_with_string_indent(self):
        with pytest.raises(TypeError):
            k = KeiConf(filepath=self.file_path_mock, indent="yes")

    @patch('pathlib.Path.is_dir')
    def test_init_with_string_missing_key_bool(self, path_mock):
        path_mock.return_value = False
        with pytest.raises(TypeError):
            k = KeiConf(filepath=self.file_path_mock, fail_on_missing_key="yes")
    
    @patch('pathlib.Path.is_dir')
    def test_init_with_string_create_if_not_exist_bool(self, path_mock):
        path_mock.return_value = False
        with pytest.raises(TypeError):
            k = KeiConf(filepath=self.file_path_mock, create_if_not_exist="yes")
    
    @patch('pathlib.Path.is_dir')
    def test_path_is_a_dir(self, mock_is_dir):
        mock_is_dir.return_value = True
        with pytest.raises(IsADirectoryError):
            k = KeiConf(filepath=self.file_content_mock)
    
    @patch('keiconf.Path.lstat')
    @patch('keiconf.Path.is_dir')
    @patch('keiconf.Path.is_file')
    @patch('keiconf.Path.mkdir', autospec=True)
    @patch('keiconf.Path.write_text')
    def test_create_config_if_not_exist(self, mock_write_text, \
                                        mock_mkdir, mock_is_file, \
                                        mock_is_dir, mock_stat):

        mock_is_dir.return_value = False
        mock_is_file.return_value = False

        # The 10 elements always present are st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, st_size, st_atime, st_mtime, st_ctime.        
        # a modified st_mtime = stat_result([0, 0, 0, 0, 0, 0, 0, 0, X, 0])
        mock_stat.return_value = stat_result([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        with patch("keiconf.open", mock_open(read_data=self.file_content_mock)) as mock_file:
            k = KeiConf(filepath=self.file_path_mock, create_if_not_exist=True)
            mock_mkdir.assert_called_with(Path(self.file_dir_mock), parents=True, exist_ok=True)
            mock_write_text.assert_called_with("{}")
     