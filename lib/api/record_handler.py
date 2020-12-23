
import os
import sqlite3
from conf import AppConfig, RECORDS_TABLE, DB_NAME


class DatabaseRecord(object):
    """
    Simple class to hold our record data
    """
    def __str__(self):
        return "{} {} {}".format(self.name, self.phone, self.address)

    def __init__(self, name=None, phone=None, address=None):
        self.name = name
        self.phone = phone
        self.address = address


class DatabaseRecordReader(object):
    """
    Class responsible for all read operations in database
    """
    database_path   = os.path.join(AppConfig.data_directory, DB_NAME)
    database_driver = sqlite3.connect(database_path)
    records_table   = RECORDS_TABLE

    @classmethod
    def get_all_records(cls):
        """
        Fetch all the records currently stored in the database
        :return: all records
        :rtype: list
        """
        cursor = cls.database_driver.cursor()
        cursor.execute("SELECT * FROM {table}".format(table=cls.records_table))
        results = cursor.fetchall()
        cursor.close()
        return results

    @classmethod
    def get_records(cls, db_record):
        """
        Fetch all the records in database based on the query data we provide as a record
        :param db_record: record to use as query data for db
        :type db_record: DatabaseRecord
        :return: records matching query criteria
        :rtype: list
        """
        cursor = cls.database_driver.cursor()
        cursor.execute("SELECT * FROM {table} WHERE instr(name, ?) and instr(phone, ?) and instr(address, ?)"
                       .format(table=cls.records_table),
                       ("" if not db_record.name else db_record.name,
                        "" if not db_record.phone else db_record.phone,
                        "" if not db_record.address else db_record.address))
        results = cursor.fetchall()
        cursor.close()
        return results


class DatabaseRecordWriter(object):
    """
    Class responsible for all write operations in database
    """
    database_path   = os.path.join(AppConfig.data_directory, DB_NAME)
    database_driver = sqlite3.connect(database_path)
    records_table   = RECORDS_TABLE

    @classmethod
    def create_records_database(cls):
        """
        Create our default tables for the application
        :return: setup success
        :rtype: bool
        """
        cursor = cls.database_driver.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS {table}(name, phone, address)".format(table=cls.records_table))
        cls.database_driver.commit()
        cursor.close()
        return True

    @classmethod
    def add_record(cls, db_record):
        """
        Add a new record to the database
        :param db_record: record we want to add
        :type db_record: DatabaseRecord
        :return: write success
        :rtype: bool
        """
        cursor = cls.database_driver.cursor()
        cursor.execute("INSERT INTO {table} VALUES(?, ?, ?)"
                       .format(table=cls.records_table), (db_record.name, db_record.phone, db_record.address))
        cls.database_driver.commit()
        cursor.close()
        return True

    @classmethod
    def delete_record(cls, query_record):
        """
        Delete records from the database based on our query data
        :param query_record: record we want to use as query data
        :type query_record: DatabaseRecord
        :return: delete successful
        :rtype: bool
        """
        cursor = cls.database_driver.cursor()
        cursor.execute("DELETE FROM {table} WHERE instr(name, ?) and instr(phone, ?) and instr(address, ?)"
                       .format(table=cls.records_table),
                       ("" if not query_record.name else query_record.name,
                        "" if not query_record.phone else query_record.phone,
                        "" if not query_record.address else query_record.address))
        cls.database_driver.commit()
        cursor.close()
        return True

    @classmethod
    def update_records(cls, field, query_record, updated_record):
        """
        Update records' fields in database based on our query data, and set to updated data
        :param field: record field/column we want to change
        :param query_record: record we want to use as query data
        :type query_record: DatabaseRecord
        :param updated_record: updated record we want to set query results data to
        :type updated_record: DatabaseRecord
        :return: update successful
        :rtype: bool
        """
        cursor = cls.database_driver.cursor()
        cursor.execute("UPDATE {table} SET {field} = ? WHERE instr({field}, ?)".
                       format(table=cls.records_table, field=field),
                       (getattr(updated_record, field), getattr(query_record, field)))
        cls.database_driver.commit()
        cursor.close()
        return True

    @classmethod
    def update_record_names(cls, query_record, updated_record):
        return cls.update_records('name', query_record, updated_record)

    @classmethod
    def update_record_phones(cls, query_record, updated_record):
        return cls.update_records('phone', query_record, updated_record)

    @classmethod
    def update_record_address(cls, query_record, updated_record):
        return cls.update_records('address', query_record, updated_record)

    @classmethod
    def update_records_by_all_fields(cls, query_record, updated_record):
        """
        Update all records matching query criteria (any fields), and set equal to the updated record data
        :param query_record: record we want to use as query data
        :type query_record: DatabaseRecord
        :param updated_record: record we want to use to set query results data equal to
        :type updated_record: DatabaseRecord
        :return: update successful
        :rtype: bool
        """
        cursor = cls.database_driver.cursor()
        cursor.execute("UPDATE {table} SET name = ?, phone = ?, address = ? "
                       "WHERE instr(name, ?) and instr(phone, ?) and instr(address, ?)"
                       .format(table=cls.records_table),
                       (updated_record.name, updated_record.phone, updated_record.address,
                        "" if not query_record.name else query_record.name,
                        "" if not query_record.phone else query_record.phone,
                        "" if not query_record.address else query_record.address))
        cls.database_driver.commit()
        cursor.close()
        return True
