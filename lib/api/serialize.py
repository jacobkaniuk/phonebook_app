
"""
Module used to serialize all data from our data source (database) to a serial format we can then
use in other applications/for different purposes (ie. json, csv, html, etc.)
"""


from abc import ABCMeta, abstractmethod
import csv
import json
import yaml
import sys

from lib.utils import integer_stream_to_phone_number


class SerialWriter(object):
    """
    Abstract base class for other writers to inherit from. All writers should have
    the same API interface.
    """
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def write(input_data, output_path):
        """
        Abstract method for writing serial data to serial format, based on serial writer format
        :param input_data: data from a datasource we want to write out in serial format
        :type input_data: dict
        :param output_path: output path of the exported file written out in serial format
        :type output_path: str
        :return: None
        """
        pass

    @classmethod
    def log_write_message(cls, writer_type, output_path, input_data):
        """
        Log message to print serial writer info, input data and output path to the console based
        on different writer formats.
        :param writer_type: shortname/extension for serial writer format
        :type writer_type: str
        :param output_path: output path of exported serial file
        :type output_path: str
        :param input_data: data from a datasource being written out to serial file
        :type input_data: dict
        :return: None
        """
        sys.stdout.write("Writing {} to {}. Data: {}".format(writer_type, output_path, input_data))


# list of different serial writers implementing their format-specific functionality

class JSONWriter(SerialWriter):
    @staticmethod
    def write(input_data, output_path):
        JSONWriter.log_write_message("JSON", output_path, input_data)
        output_data = {}
        with open(output_path, 'w') as json_file:
            for result in input_data:
                # hash our fields since there might be duplicate keys and JSON doesn't allow that
                hash_id = hash(result[0] + str(result[1]) + result[2])
                output_data[hash_id] = {"name": result[0],
                                        "phone": integer_stream_to_phone_number(str(result[1])),
                                        "address": result[2]}
            json.dump(output_data, json_file)


class CSVWriter(SerialWriter):
    @staticmethod
    def write(input_data, output_path):
        CSVWriter.log_write_message("CSV", output_path, input_data)
        columns = ["Name", "Phone", "Address"]
        with open(output_path, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for result in input_data:
                writer.writerow({"Name": result[0],
                                 "Phone": integer_stream_to_phone_number(str(result[1])),
                                 "Address": result[2]})


class YAMLWriter(SerialWriter):
    @staticmethod
    def write(input_data, output_path):
        YAMLWriter.log_write_message("YAML", output_path, input_data)
        output_data = {}
        with open(output_path, 'w') as json_file:
            for result in input_data:
                # hash our fields since there might be duplicate keys and YAML doesn't allow that
                hash_id = hash(result[0] + str(result[1]) + result[2])
                output_data[hash_id] = {"name": str(result[0]),
                                        "phone": integer_stream_to_phone_number(str(result[1])),
                                        "address": str(result[2])}
            yaml.dump(output_data, json_file)


class HTMLWriter(SerialWriter):
    @staticmethod
    def write(input_data, output_path):
        HTMLWriter.log_write_message("HTML", output_path, input_data)
        body = ""
        for result in input_data:
            body += "<div>"
            body += "<h5>Name: {}</h5>".format(str(result[0]))
            body += "<h5>Phone: {}</h5>".format(integer_stream_to_phone_number(str(result[1])))
            body += "<h5>Address: {}</h5>".format(str(result[2]))
            body += "<br>"
            body += "</div>"
        html_code = "<html>{body}</html>".format(body=body)
        with open(output_path, 'w') as html_file:
            html_file.write(html_code)


class SerialFormats(object):
    """
    Class of all currently supported formats. Used as an enum in order to
    change the serial format used in the AppConfig, as the writer and extension
    type are keys in the attributes.
    """
    CSV =  {'extension': 'csv',  'writer': CSVWriter}
    JSON = {'extension': 'json', 'writer': JSONWriter}
    YAML = {'extension': 'yaml', 'writer': YAMLWriter}
    HTML = {'extension': 'html', 'writer': HTMLWriter}

    # list of all the currently supported formats for easily checking
    # if an input for serial change is valid/supported
    ALL_FORMATS = [CSV, JSON, YAML, HTML]
