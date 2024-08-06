import json

from eth_utils import decode_hex, to_checksum_address


def _decode_ether_deposit(payload):
    try:
        if isinstance(payload, str):
            payload_bytes = decode_hex(payload)
        elif isinstance(payload, bytes):
            payload_bytes = payload
        else:
            raise TypeError("Payload must be a string or bytes")

        if len(payload_bytes) < 52:
            raise ValueError("Payload too short for Ether deposit")

        sender_address = to_checksum_address(payload_bytes[:20].hex())
        amount = (int.from_bytes(payload_bytes[20:52], 'big') / 10 ** 18)  # converting from wei to eth
        arbitrary_data = payload_bytes[52:].rstrip(b'\x00').decode('utf-8')

        decoded_abi = {
            'sender_address': sender_address,
            'amount': amount,
            'arbitrary_data': arbitrary_data
        }
        return decoded_abi
    except Exception as error:
        raise ValueError(
            "Payload does not conform to Ether transfer ABI") from error


def _decode_erc20_deposit(payload):
    try:
        if isinstance(payload, str):
            payload_bytes = decode_hex(payload)
        elif isinstance(payload, bytes):
            payload_bytes = payload
        else:
            raise TypeError("Payload must be a string or bytes")

        if len(payload_bytes) < 73:
            raise ValueError("Payload too short for ERC20 deposit")

        success = payload_bytes[0]
        token_address = to_checksum_address(payload_bytes[1:21].hex())
        sender_address = to_checksum_address(payload_bytes[21:41].hex())
        amount = int.from_bytes(payload_bytes[41:73], 'big')
        arbitrary_data = payload_bytes[73:].rstrip(b'x\00').decode('utf-8')

        return {
            'success': success,
            'token_address': token_address,
            'sender_address': sender_address,
            'amount': amount,
            'arbitrary_data': arbitrary_data
        }
    except Exception as error:
        raise ValueError(
            "Payload does not conform to Ether transfer ABI") from error


def _decode_erc721_deposit(payload):
    try:
        if isinstance(payload, str):
            payload_bytes = decode_hex(payload)
        elif isinstance(payload, bytes):
            payload_bytes = payload
        else:
            raise TypeError("Payload must be a string or bytes")

        if len(payload_bytes) < 72:
            raise ValueError("Payload too short for ERC721 deposit")

        token_address = to_checksum_address(payload_bytes[:20].hex())
        sender_address = to_checksum_address(payload_bytes[20:40].hex())
        token_id = int.from_bytes(payload_bytes[40:72], 'big')
        arbitrary_data = payload_bytes[72:].rstrip(b'\x00').decode('utf-8')

        return {
            'token_address': token_address,
            'sender_address': sender_address,
            'token_id': token_id,
            'arbitrary_data': arbitrary_data
        }
    except Exception as error:
        raise ValueError(
            "Payload does not conform to Ether transfer ABI") from error


def _decode_packed_abi(token_type: str):
    token_type = token_type.lower()
    decoder = None
    if token_type == 'eth':
        decoder = _decode_ether_deposit
        return decoder
    elif token_type == 'erc20':
        decoder = _decode_erc20_deposit
        return decoder
    elif token_type == 'erc721':
        decoder = _decode_erc721_deposit
        return decoder
    else:
        raise ValueError('Invalid token type')


def decode_packed_abi(token_type: str, payload: json):
    """


    param token_type: eth or erc20 or erc721
    :param token_type:
    :param payload: the abi data from the portal
    :return:
    """
    parsed_payload: dict = json.loads(payload)
    if 'payload' in parsed_payload:
        parsed_payload: bytes = bytes.fromhex(parsed_payload['payload'][2:])
    factory_obj = None
    try:
        factory_obj = _decode_packed_abi(token_type)
        return factory_obj(parsed_payload)
    except ValueError as e:
        raise ValueError('Invalid input: payload should be a packed abi data and token type should either be eth,'
                         'erc20 or erc721')
