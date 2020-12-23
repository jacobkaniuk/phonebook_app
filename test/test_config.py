import os
import unittest
import sqlite3

from lib.api.auth import WriteAuthRules
from lib.api.serialize import  SerialFormats
from lib.api.conf import setup_app_config, AppConfig
from lib.api.record_handler import DatabaseRecordWriter, DatabaseRecordReader

# overwrite our defaults to use a test db + table
DatabaseRecordWriter.database_path = os.path.join(os.path.dirname(DatabaseRecordWriter.database_path), 'test_database')
DatabaseRecordWriter.database_driver = sqlite3.connect(DatabaseRecordWriter.database_path)
DatabaseRecordReader.database_path = os.path.join(os.path.dirname(DatabaseRecordWriter.database_path), 'test_database')
DatabaseRecordReader.database_driver = sqlite3.connect(DatabaseRecordWriter.database_path)


class TestConfig(unittest.TestCase):
    def test_config_creation(self):
        self.assertTrue(os.path.exists(setup_app_config()))

    def test_config_data_dir_change(self):
        prev_data_dir = AppConfig.data_directory
        new_data_dir = os.path.dirname(__file__)
        AppConfig.change_data_directory(new_data_dir)
        self.assertEquals(AppConfig.data_directory, new_data_dir)
        AppConfig.change_data_directory(prev_data_dir)  # restore to previous

    def test_config_serial_format_change(self):
        prev_format = AppConfig.serial_format
        new_format = SerialFormats.CSV
        AppConfig.change_serial_format(new_format)
        self.assertEquals(AppConfig.serial_format, new_format)
        with self.assertRaises(Exception) as error:
            AppConfig.change_serial_format('cvs')
            self.assertTrue('Please use SerialFormats enum to specify new/updated format' in error.exception)
        AppConfig.change_serial_format(prev_format)  # restore to previous

    def test_write_auth_rule_change(self):
        prev_rule = AppConfig.write_auth_rule
        new_rule = WriteAuthRules.WRITE_IF_ADDRESS_UNIQUE
        AppConfig.change_write_auth_rule(new_rule)
        self.assertEquals(AppConfig.write_auth_rule, new_rule)
        AppConfig.change_write_auth_rule(prev_rule)  # restore to previous
