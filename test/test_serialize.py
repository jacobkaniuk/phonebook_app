import os
import sqlite3
import unittest

from lib.api.record_handler import DatabaseRecordWriter, DatabaseRecordReader
from lib.api.conf import AppConfig
from lib.api.serialize import SerialFormats

# overwrite our defaults to use a test db + table
DatabaseRecordWriter.database_path = os.path.join(os.path.dirname(DatabaseRecordWriter.database_path), 'test_database')
DatabaseRecordWriter.database_driver = sqlite3.connect(DatabaseRecordWriter.database_path)
DatabaseRecordReader.database_path = os.path.join(os.path.dirname(DatabaseRecordWriter.database_path), 'test_database')
DatabaseRecordReader.database_driver = sqlite3.connect(DatabaseRecordWriter.database_path)


class TestSerialize(unittest.TestCase):
    def test_all_serial_formats(self):
        for _format in AppConfig.supported_serial_formats:
            AppConfig.change_serial_format(_format)
            output_path = os.path.join(AppConfig.data_directory, "records.{}".format(AppConfig.serial_format['extension']))
            print output_path
            AppConfig.serial_format['writer'].write(DatabaseRecordReader.get_all_records(), output_path)
            self.assertTrue(os.path.exists(output_path))
