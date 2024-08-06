from cartesi_nexus.helpers import str2hex, hex2str
import json


class Voucher:
    """
           Initialize a Voucher instance.
           Args:
               destination (str): The destination address.
               payload (str): The payload data in bytes or in str.
           Examples:
               Voucher(destination='0x1234', payload=b'data')
               Voucher('0x1234', 'data')
           """

    def __init__(self, *args, **kwargs):
        self._destination = None
        self._destination_to = None
        self._payload = None
        data = kwargs['data']
        if 'destination' in data and 'payload' in data and 'destination_to' not in data:
            self._destination = data['destination']
            self._payload = data['payload']
        elif 'destination' in data and 'payload' in data and 'destination_to' in data:
            self._destination = data['destination']
            self._destination_to = data['destination_to']
            self._payload = data['payload']

        elif len(args[0]) == 2:
            self._destination = args[0]['destination']
            self._payload = args[0]['payload']
        elif len(args[0]) == 3:
            self._destination = args[0]['destination']
            self._destination_to = args[0]['destination_to']
            self._payload = args[0]['payload']

        else:
            raise ValueError('Invalid arguments: must provide destination and payload')

    @property
    def payload(self):
        return self._payload

    @property
    def destination(self):
        return self._destination

    @property
    def destination_to(self):
        return self._destination_to

    @destination_to.setter
    def destination_to(self, value):
        self._destination_to = value

    @destination.setter
    def destination(self, value):
        self._destination = value

    @payload.setter
    def payload(self, value):
        self._payload = value


class Base:
    """
           Initialize an Error/Notice/Log instance.

           Args:
               payload (str): The payload data in string or bytes.
           Examples:
               Log(payload='data')
               Notice('data')
           """

    def __init__(self, *args, **kwargs):
        if 'payload' in kwargs:
            self._python_payload = kwargs['payload']
            self._payload = str2hex(json.dumps(kwargs['payload']))
        elif len(args) == 1:
            self._payload = str2hex(json.dumps(args[0]))
            self._python_payload = args[0]
        else:
            raise ValueError('Invalid arguments: must provide payload')

    @property
    def python_payload(self):
        return self._python_payload

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value


def __output_wrapper(output_type: str):
    output_obj = None
    if output_type.lower() == 'notice' or output_type.lower() == 'log' or output_type.lower() == 'error':
        output_obj = Base
    elif output_type.lower() == 'voucher':
        output_obj = Voucher
    else:
        raise ValueError('Invalid output_type must be either notice,log,voucher or error value')
    return output_obj


def output(output_type: str, *args, **kwargs):
    """
Voucher:
    Args:
    destination (str): The destination address.
    payload (str): The payload data in bytes.
Error/Notice/Log:
    Args:
    payload (str): The payload data.
Example:
    voucher = output('voucher', destination='', payload='')
    notice = output('notice', payload='')
:param output_type: The type of output to create ('voucher', 'notice', 'log', 'error').
"""

    factory_obj = None
    try:
        factory_obj = __output_wrapper(output_type)(*args, **kwargs)
    except ValueError as e:
        raise ValueError('Invalid input')
    return factory_obj
