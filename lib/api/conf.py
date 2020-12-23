
"""
This module is used to setup and configure the app settings on a global level. Settings are
written out to a config.ini file, which may be change directly through the API, or changed
in a simple text editor with valid values. When the application starts up, these values
are parsed from the config.ini file, and the application specific settings are changed in
the AppConfig class down below.
"""


import os
import sys
from os.path import dirname as dir_up
from auth import WriteAuthRules
from serialize import SerialFormats, SerialWriter
import configparser

# keys for easy access/avoiding incorrect key names in this module as well as others
DB_NAME = 'phonebook'
RECORDS_TABLE = 'records'
CONFIG_DIR = 'config'
TEST_DIR = 'test'
DATA_DIR = 'data'
DATA_DIR_KEY = 'data_dir'
SERIAL_FORMAT_KEY = 'serial_format'
WRITE_AUTH_RULE_KEY = 'write_auth_rule'
SUPPORTED_SERIAL_FORMATS = SerialFormats.ALL_FORMATS
APP_CONFIG_INI_PATH = os.path.join(dir_up(dir_up(dir_up(__file__))), CONFIG_DIR, 'config.ini')
APP_CONFIG_DEFAULTS = {DATA_DIR_KEY: os.path.join(dir_up(dir_up(dir_up(__file__))), DATA_DIR),
                       SERIAL_FORMAT_KEY: SerialFormats.JSON,
                       WRITE_AUTH_RULE_KEY: WriteAuthRules.WRITE_IF_PHONE_UNIQUE}


class AppConfig(object):
    """
    Config class we will use to change all the settings used throughout application.
    """
    config_ini_path         = APP_CONFIG_INI_PATH
    supported_serial_formats= SUPPORTED_SERIAL_FORMATS
    data_directory          = APP_CONFIG_DEFAULTS[DATA_DIR_KEY]
    serial_format           = APP_CONFIG_DEFAULTS[SERIAL_FORMAT_KEY]
    write_auth_rule         = APP_CONFIG_DEFAULTS[WRITE_AUTH_RULE_KEY]

    @classmethod
    def update_setting(cls, setting, value):
        """
        Update AppConfig based on the attribute names and values we provide
        :param setting: attribute name
        :type setting: str
        :param value: attribute value
        :type value: object
        :return: None
        """
        try:
            setattr(cls, setting, value)
            return True
        except AttributeError as err:
            sys.stderr.write(err.message)

    @classmethod
    def change_serial_format(cls, serial_format, quiet=False):
        """
        Change the serial output format to use when exporting database records to a serial file (ie. json, csv, etc.).
        :param serial_format: serial format we want to change to
        :type serial_format: SerialFormats
        :param quiet: whether we want to print the updated settings confirmation message
        :type quiet: bool
        :return: None
        """
        if not issubclass(serial_format['writer'], SerialWriter):
            raise TypeError("Invalid type provided for serial format change. Please use SerialFormats enum to specify "
                            "new/updated format. \nSupported formats:\n{}\n"
                            .format(cls.supported_serial_formats))
        if serial_format not in cls.supported_serial_formats:
            raise ValueError("Invalid type/format provided for serial format change. Please use SerialFormats enum "
                             "to specify new/updated format.\n.Supported formats: \n{}\n"
                             .format(cls.supported_serial_formats))
        if cls.update_setting('serial_format', serial_format):
            if not quiet:
                cls._confirm_and_display()

        APP_CONFIG_DEFAULTS[SERIAL_FORMAT_KEY] = serial_format['extension']
        write_config_ini(APP_CONFIG_DEFAULTS)

    @classmethod
    def change_data_directory(cls, data_directory, quiet=False):
        """
        Change the data directory filepath where we want all of our
        record data to go (ie. db file, results in serial formats, etc.)
        :param data_directory: directory filepath
        :type data_directory: str
        :param quiet: whether we want to print the updated settings confirmation message
        :type quiet: bool
        :return: None
        """
        if not os.path.exists(data_directory) or not os.path.isdir(data_directory):
            raise IOError("Data directory provided not valid. Please provide a valid path.\n")
        if data_directory == cls.data_directory:
            return
        if cls.update_setting('data_directory', data_directory):
            if not quiet:
                cls._confirm_and_display()

        APP_CONFIG_DEFAULTS[DATA_DIR_KEY] = data_directory
        write_config_ini(APP_CONFIG_DEFAULTS)

    @classmethod
    def change_write_auth_rule(cls, write_auth_rule, quiet=False):
        """
        Change the record write authority rule used to determine data criteria for new records
        :param write_auth_rule: authority rule to change to
        :type write_auth_rule: WriteAuthRules
        :param quiet: whether we want to print the updated settings confirmation message
        :type quiet: bool
        :return: None
        """
        if cls.update_setting('write_auth_rule', write_auth_rule):
            if not quiet:
                cls._confirm_and_display()

        APP_CONFIG_DEFAULTS[WRITE_AUTH_RULE_KEY] = write_auth_rule
        write_config_ini(APP_CONFIG_DEFAULTS)

    @classmethod
    def show_config_info(cls):
        print "=== APP CONFIG === \n"
        for attr in dir(cls):
            if not attr.startswith('__') and not attr.endswith('__') and not callable(getattr(cls, attr)):
                print "{}{}".format(attr.upper().ljust(25), getattr(cls, attr))

    @classmethod
    def _confirm_and_display(cls):
        print "\n*** Config settings successfully changed. ***\n"
        cls.show_config_info()


def write_config_ini(config_settings):
    """
    Create/update config.ini file based on settings passed in
    :param config_settings: application settings to write/update
    :type config_settings: dict
    :return: None
    """
    parser = configparser.ConfigParser()
    parser["DEFAULT"] = config_settings
    with open(APP_CONFIG_INI_PATH, 'w') as f:
        parser.write(f)


def read_config_ini(config_settings_path):
    """
    Read the config.ini file from disk, parse the values for each of the settings,
    then set the AppConfig settings based on the parsed values, as settings can be
    changed via the API, or by editing the serial config.ini with valid values
    :param config_settings_path: path to the config.ini used to read app settings
    :type config_settings_path: str
    :return: None
    """
    if not os.path.exists(config_settings_path) or not os.path.isfile(config_settings_path):
        raise IOError("Could not parse settings INI. Please provide a valid INI filepath.\n")

    parser = configparser.ConfigParser()
    parser.read(config_settings_path)
    data_dir = parser['DEFAULT'][DATA_DIR_KEY] if parser['DEFAULT'][DATA_DIR_KEY] != "" else APP_CONFIG_DEFAULTS[DATA_DIR_KEY]
    AppConfig.change_data_directory(data_dir, quiet=True)
    if parser["DEFAULT"][SERIAL_FORMAT_KEY] in [key['extension'] for key in AppConfig.supported_serial_formats]:
        AppConfig.change_serial_format([_format for _format in AppConfig.supported_serial_formats if
                                        _format['extension'] == parser['DEFAULT'][SERIAL_FORMAT_KEY]][0], quiet=True)
    if int(parser["DEFAULT"][WRITE_AUTH_RULE_KEY]) in WriteAuthRules.ALL_RULES:
        AppConfig.change_write_auth_rule(([rule for rule in WriteAuthRules.ALL_RULES if
                                           rule == int(parser['DEFAULT'][WRITE_AUTH_RULE_KEY])][0]), quiet=True)


def setup_app_config():
    """
    Entry point for configuring our app settings. If a config.ini file exists, parse this
    file and set the app settings equal to parsed values. If it doesn't exist, create one
    using the default settings and write it to disk.
    :return:
    """
    if not os.path.isfile(APP_CONFIG_INI_PATH) or \
            not os.path.exists(APP_CONFIG_INI_PATH):
        write_config_ini(APP_CONFIG_DEFAULTS)
        return APP_CONFIG_INI_PATH
    elif os.path.isfile(APP_CONFIG_INI_PATH):
        read_config_ini(APP_CONFIG_INI_PATH)
        return APP_CONFIG_INI_PATH
