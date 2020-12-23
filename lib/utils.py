
def phone_number_to_integer_stream(phone_number):
    """
    Convert a phone number in string format with various alphabetic characters into a
    multi digit integer (ie. (647) 444-1552 => 6474441552 )
    :param phone_number: phone number we want to convert to a integer
    :type phone_number: object
    :return: phone number as integer stream
    :rtype: int
    """
    phone_number = str(phone_number)
    number = phone_number.replace('(', "").replace(')', "").replace('-', "").replace(" ", "")
    return int("".join(number.split(" ")))


def integer_stream_to_phone_number(phone_number):
    """
    Convert our integer stream to a more readable/human-friendly string format.
    (ie. 6474441552 => (647) 444-1552 )
    :param phone_number: integer stream we want to convert
    :type phone_number: object
    :return: phone number in readable string format
    :rtype: str
    """
    phone_number = str(phone_number)
    if len(phone_number) != 10:
        raise ValueError("\nInvalid phone number provided. Please use a 10 digit integer stream.")
    area_code = phone_number[:3]
    middle = phone_number[3:6]
    tail = phone_number[-4:]
    return "({area}) {middle}-{tail}".format(area=area_code, middle=middle, tail=tail)
