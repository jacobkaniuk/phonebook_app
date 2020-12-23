import os
import unittest
import sqlite3

from lib.api.auth import WriteAuthRules
from lib.api.record_handler import DatabaseRecordWriter, DatabaseRecordReader, DatabaseRecord
from lib.api.auth import WriteAuthRuleHandler


# overwrite our defaults to use a test db + table
DatabaseRecordWriter.database_path = os.path.join(os.path.dirname(DatabaseRecordWriter.database_path), 'test_database')
DatabaseRecordWriter.database_driver = sqlite3.connect(DatabaseRecordWriter.database_path)
DatabaseRecordReader.database_path = os.path.join(os.path.dirname(DatabaseRecordWriter.database_path), 'test_database')
DatabaseRecordReader.database_driver = sqlite3.connect(DatabaseRecordWriter.database_path)


class TestDatabase(unittest.TestCase):
    def test_db_create(self):
        self.assertIsNotNone(DatabaseRecordWriter.database_path)
        self.assertIsNotNone(DatabaseRecordWriter.database_driver)
        self.assertTrue(DatabaseRecordWriter.create_records_database())

    def test_db_add_record(self):
        import random
        record1 = DatabaseRecord("Paul Wilson", str(random.randrange(6470000000, 6479999999)), "4122 Testing Road")
        record2 = DatabaseRecord("John Kal", "6445221234", "1554 Long St")
        self.assertTrue(DatabaseRecordWriter.add_record(record1))
        self.assertTrue(DatabaseRecordWriter.add_record(record2))

    def test_check_with_auth_rule(self):
        driver = DatabaseRecordWriter.database_driver
        cursor = driver.cursor()
        record1 = DatabaseRecord("Tim Cook", "6474478145", "1665 Test Court")
        record2 = DatabaseRecord("Matthew Chase", "6472253364", "502 Testing Road")
        for record in [record1, record2]:
            self.assertTrue(WriteAuthRuleHandler.can_add_with_auth_rule(DatabaseRecordWriter.records_table, cursor, WriteAuthRules.WRITE_ALL_NO_RULE, record))
            self.assertTrue(WriteAuthRuleHandler.can_add_with_auth_rule(DatabaseRecordWriter.records_table, cursor, WriteAuthRules.WRITE_IF_NAME_UNIQUE, record))
            self.assertTrue(WriteAuthRuleHandler.can_add_with_auth_rule(DatabaseRecordWriter.records_table, cursor, WriteAuthRules.WRITE_IF_PHONE_UNIQUE, record))
            self.assertTrue(WriteAuthRuleHandler.can_add_with_auth_rule(DatabaseRecordWriter.records_table, cursor, WriteAuthRules.WRITE_IF_ADDRESS_UNIQUE, record))
            self.assertTrue(WriteAuthRuleHandler.can_add_with_auth_rule(DatabaseRecordWriter.records_table, cursor, WriteAuthRules.WRITE_IF_ALL_UNIQUE, record))

    def test_get_records_with_keywords(self):
        query1 = DatabaseRecord("Paul", "647")
        query2 = DatabaseRecord(phone="647")
        query3 = DatabaseRecord(address="4122 Testing Road")
        for query in [query1, query2, query3]:
            for item in DatabaseRecordReader.get_records(query):
                self.assertIsNotNone(item)

    def test_update_records_names(self):
        query1 = DatabaseRecord("Paul Wilson")
        update1 = DatabaseRecord("Pauly Wilkins")
        self.assertTrue(DatabaseRecordWriter.update_record_names(query1, update1))

    def test_update_records_phones(self):
        query1 = DatabaseRecord(phone="647909")
        update1 = DatabaseRecord(phone="6475551231")
        self.assertTrue(DatabaseRecordWriter.update_record_phones(query1, update1))

    def test_update_records_addresses(self):
        query1 = DatabaseRecord("John Kal", "6445221234", "1554 Long St")
        self.assertTrue(DatabaseRecordWriter.add_record(query1))
        update1 = DatabaseRecord(address="1234 Someroad St")
        self.assertTrue(DatabaseRecordWriter.update_record_address(query1, update1))
        self.assertIsNotNone(DatabaseRecordReader.get_all_records())
