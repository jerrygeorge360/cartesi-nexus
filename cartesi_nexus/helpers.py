import json


def hex2str(hex_value):
    if isinstance(hex_value, str):
        if hex_value.startswith('0x'):
            hex_value = hex_value[2:]

    try:
        if isinstance(hex_value, bytes):
            return hex_value.hex()
        elif isinstance(hex_value, str):
            byte_data = bytes.fromhex(hex_value)
            string_data = byte_data.decode('utf-8')
            return string_data
        else:
            raise ValueError('value must be a string or a byte')
    except Exception as e:
        raise ValueError('byte or hexadecimal') from e


def str2hex(payload):
    if isinstance(payload, str):
        return "0x" + payload.encode('utf-8').hex()
    elif isinstance(payload, bytes):
        return "0x" + payload.hex()
    else:
        raise TypeError("Input must be a string")


# which corresponds to the first 4 bytes of the Keccak256-encoded result of "transfer(address,uint256)"
def function_selector_encoder(function_selector: str):
    pass
