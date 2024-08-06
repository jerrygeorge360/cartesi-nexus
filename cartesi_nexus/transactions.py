import json
from cartesi_nexus.abi_deposit_decoder import decode_packed_abi
from cartesi_nexus.abi_withdraw_encoder import FuncSel, withdraw_encoder
from cartesi_nexus.helpers import hex2str
from cartesi_nexus.outputs import output
from cartesi_nexus.token_manager import TokenManager


def transfer_decode_payload(payload):
    payload: json = hex2str(payload)

    pythonic_payload: dict = json.loads(payload)
    if pythonic_payload['payload']:
        pythonic_payload = pythonic_payload['payload']
    tuple_payload: tuple = tuple(pythonic_payload.values())
    sender_address, destination_address, amount, *data = tuple_payload
    return sender_address, destination_address, amount, *data


def _transfer_ether(sender_address: str, destination_address: str, amount: float, data=None):
    token_manager_sender = TokenManager(account=sender_address)
    token_manager_destination = TokenManager(account=destination_address)
    token_manager_sender.ether_decrease(amount)
    token_manager_destination.ether_increase(amount)
    notice = {'payload': {'type': 'ether_transfer',
                          'data': {'from': sender_address, 'to': destination_address, 'amount': amount}}}

    return output('notice', notice).payload


def _transfer_erc20(sender_address: str, destination_address: str, amount: float, data=None):
    token_type: str = data[0]['token_type']
    token_manager_sender = TokenManager(account=sender_address)
    token_manager_destination = TokenManager(account=destination_address)
    token_manager_sender.erc20_decrease(token_type, amount)
    token_manager_destination.erc20_increase(token_type, amount)
    notice = {'payload': {'type': 'erc20_transfer',
                          'data': {'token_type': token_type, 'from': sender_address, 'to': destination_address,
                                   'amount': amount}}}
    return output('notice', notice).payload


def _transfer_erc721(sender_address: str, destination_address: str, amount: float, data=None):
    nft_name = data[0]['nft_name']
    nft_id = str(data[0]['nft_id'])
    token_manager_sender = TokenManager(account=sender_address)
    token_manager_sender.remove_nft_token(nft_name, nft_id)
    token_manager_destination = TokenManager(account=destination_address)
    token_manager_destination.add_nft_token(nft_name, nft_id)
    notice = {'payload': {'type': 'erc721_transfer',
                          'data': {'nft_id': nft_id, 'nft_name': nft_name, 'from': sender_address,
                                   'to': destination_address,
                                   'amount': amount}}}
    return output('notice', notice).payload


def _transfer_wrapper(token_type: str):
    token_type = token_type.lower()

    if token_type == 'eth':
        return _transfer_ether
    elif token_type == 'erc20':
        return _transfer_erc20
    elif token_type == 'erc721':
        return _transfer_erc721
    else:
        raise ValueError('token_type should be eth, erc20, or erc721')


def transfer_token(token_type: str, payload) -> output:
    try:
        sender_address, destination_address, amount, data = transfer_decode_payload(payload)
        transfer_function = _transfer_wrapper(token_type)
        return transfer_function(sender_address, destination_address, amount, data)
    except ValueError as e:

        print(e)


def _withdraw_ether(enum: FuncSel, address, amount, *args):
    data = withdraw_encoder(enum, address, amount, *args)
    destination = address
    return output('voucher', data={'payload': data, 'destination': destination})


def _withdraw_erc20(enum: FuncSel, address, amount, *args):
    data = withdraw_encoder(enum, address, amount, *args)
    destination = address
    return output('voucher', data={'payload': data, 'destination': destination})


def _withdraw_erc20_to_another(enum: FuncSel, address, amount, *args):
    data = withdraw_encoder(enum, address, amount, *args)
    destination = address
    destination_to = args[0]
    return output('voucher', data={'payload': data, 'destination': destination, 'destination_to': destination_to})


def _withdraw_erc721(enum: FuncSel, address, amount, *args):
    data = withdraw_encoder(enum, address, amount, *args)
    destination = address
    destination_to = args[0]
    return output('voucher', data={'payload': data, 'destination': destination, 'destination_to': destination_to})


def _withdraw_wrapper(enum: FuncSel):
    factory = None
    if enum.name == 'ETHER':
        factory = _withdraw_ether
        return factory
    elif enum.name == 'ERC_20':
        factory = _withdraw_erc20
        return factory
    elif enum.name == 'ERC_20_DIFF':
        factory = _withdraw_erc20_to_another
        return factory
    elif enum.name == 'ERC_721':
        factory = _withdraw_erc721
        return factory
    else:
        raise TypeError(f"Expected FuncSel enum,got {type(enum).__name__}")


def withdraw(enum: FuncSel, address, amount, *args) -> output:
    obj = _withdraw_wrapper(enum)
    return obj(enum, address, amount, *args)


def _deposit_ether(**kwargs):
    sender_address = None
    amount = None
    data = kwargs['data']
    if 'sender_address' in data and 'amount' in data:
        sender_address = data['sender_address']
        amount = data['amount']
        arbitrary_data = data['arbitrary_data'] if data['arbitrary_data'] else None
        data = {'payload': {'sender_address': sender_address, 'amount': amount}}

        if arbitrary_data is not None:
            data['payload']['arbitrary_data'] = arbitrary_data

        return output('notice', data)


def _deposit_erc20(**kwargs):
    success = None
    token_address = None
    sender_address = None
    amount = None
    data = kwargs['data']
    if 'success' in data and 'token_address' in data and 'sender_address' in data and 'amount' in data:
        success = data['success']
        token_address = data['token_address']
        sender_address = data['sender_address']
        amount = data['amount']
        arbitrary_data = data['arbitrary_data'] if data['arbitrary_data'] else None
        data = {'payload': {'success': success, 'token_address': token_address, 'sender_address': sender_address,
                            'amount': amount}}
        if arbitrary_data is not None:
            data['payload']['arbitrary_data'] = arbitrary_data

        return output('notice', data)


def _deposit_erc721(**kwargs):
    token_address = None
    sender_address = None
    token_id = None
    data = kwargs['data']
    if 'token_address' in data and 'sender_address' in data and 'token_id' in data:
        token_address = data['token_address']
        sender_address = data['sender_address']
        token_id = data['token_id']
        arbitrary_data = data['arbitrary_data'] if data['arbitrary_data'] else None
        data = {'payload': {'token_address': token_address, 'sender_address': sender_address, 'token_id': token_id}}
        if arbitrary_data is not None:
            data['payload']['arbitrary_data'] = arbitrary_data

        return output('notice', data)


def _deposit_wrapper(token_type: str):
    if token_type == 'eth':
        return _deposit_ether
    elif token_type == 'erc20':
        return _deposit_erc20
    elif token_type == 'erc721':
        return _deposit_erc721
    else:
        raise ValueError('Incorrect value should be eth,erc20 or erc721 keyword')


def deposit(token_type: str, payload: json) -> output:
    try:
        unpacked_data = decode_packed_abi(token_type, payload)
        factory = _deposit_wrapper(token_type)
        return factory(data=unpacked_data)
    except ValueError as err:
        print(err)


def _get_ether(account: str):
    ether_amount = TokenManager(account)
    amount = ether_amount.ether

    return ether_amount.ether


def _get_erc20(account: str):
    erc_amount = TokenManager(account).erc20
    return erc_amount


def _get_erc721(account: str):
    nft_collections = TokenManager(account).erc721
    return nft_collections


def _get_total_crypto(account: str):
    return TokenManager(account).__dict__


def get_token(account: str, token_name: str):
    if token_name == 'eth':
        return _get_ether(account)
    elif token_name == 'erc20':
        return _get_erc20(account)
    elif token_name == 'erc721':
        return _get_erc721(account)


def get_all_tokens(account: str):
    return _get_total_crypto(account)


# TODO : write docs
# TODO: make the deposit function elegant

