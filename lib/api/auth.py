
"""
Module used to manage write rules for new database records. Separate from data writer classes
to avoid creating unnecessary dependencies/coupling. Validation of write access should be done at the
component usage implementation level, rather than the writer interface level.
"""


class WriteAuthRules(object):
    """
    Rules for determining whether or not we can write new database records based on the new record data.
    """
    WRITE_ALL_NO_RULE       = 1
    WRITE_IF_NAME_UNIQUE    = 2
    WRITE_IF_PHONE_UNIQUE   = 3
    WRITE_IF_ADDRESS_UNIQUE = 4
    WRITE_IF_ALL_UNIQUE     = 5

    ALL_RULES = [WRITE_ALL_NO_RULE, WRITE_IF_NAME_UNIQUE, WRITE_IF_PHONE_UNIQUE, WRITE_IF_ADDRESS_UNIQUE, WRITE_IF_ALL_UNIQUE]


class WriteAuthRuleHandler(object):
    """
    Rule handler for each rule type, and which function dictates whether writing may proceed or not
    """
    @classmethod
    def filter_by_string(cls, query_string, db_cursor, args):
        """
        Method used to determine whether or not any results are returned from db, based on the input
        provided by each rule type. If something is returned, then writing cannot proceed.
        :param query_string: SELECT SQL query we want to run on the db. In here we provide the column names to check.
        :type query_string: str
        :param db_cursor: cursor to the db
        :type db_cursor: Cursor
        :param args: query data we want to use to fetch results
        :type args: tuple
        :return: did we find any results, if yes, we cannot proceed with writing
        :rtype: bool
        """
        db_cursor.execute(query_string, args)
        if db_cursor.fetchone():
            return False
        return True

    @classmethod
    def can_add_with_auth_rule(cls, table, db_cursor, auth_rule, db_record):
        """
        Method used to map the different auth rules to select method above, based on criteria we pass in
        :param table: db table we want to check against
        :type table: str
        :param db_cursor: db cursor we want to use
        :type db_cursor: Cursor
        :param auth_rule: authority rule we want to check against
        :type auth_rule: int
        :param db_record: record we want to use as query data
        :type db_record: DatabaseRecord
        :return: whether or not we can write the record based on query data passed in
        :rtype: bool
        """
        if auth_rule == WriteAuthRules.WRITE_ALL_NO_RULE:
            return True
        elif auth_rule == WriteAuthRules.WRITE_IF_NAME_UNIQUE:
            return cls.filter_by_string("SELECT * FROM {} WHERE name=?".format(table), db_cursor, (db_record.name,))
        elif auth_rule == WriteAuthRules.WRITE_IF_PHONE_UNIQUE:
            return cls.filter_by_string("SELECT * FROM {} WHERE phone=?".format(table), db_cursor, (db_record.phone,))
        elif auth_rule == WriteAuthRules.WRITE_IF_ADDRESS_UNIQUE:
            return cls.filter_by_string("SELECT * FROM {} WHERE address=?".format(table), db_cursor, (db_record.address,))
        elif auth_rule == WriteAuthRules.WRITE_IF_ALL_UNIQUE:
            return cls.filter_by_string("SELECT * FROM {} WHERE name=? and phone=? and address=?".format(table), db_cursor,
                                        (db_record.name, db_record.phone, db_record.address))
