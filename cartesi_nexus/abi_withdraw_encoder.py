from eth_abi import encode
from eth_utils import decode_hex, to_checksum_address, keccak, to_hex
from enum import Enum


class FuncSel(Enum):
    ETHER = 'withdrawEther(address,uint256)'
    ERC_20 = 'transfer(address,uint256)'
    ERC_20_DIFF = 'transferFrom(address,address,uint256)'
    ERC_721 = 'safeTransferFrom(address,address,uint256)'


def _function_selector_encoder(enum: FuncSel) -> str:
    if not isinstance(enum, FuncSel):
        raise TypeError(f"Expected FuncSel enum,got {type(enum).__name__}")
    function_signature: str = str(enum.value)
    return keccak(text=function_signature)[:4].hex()


def _function_argument_encoder(enum: FuncSel, address, amount: int, *args):
    if enum.name == 'ETHER':
        address = address
        encoded_data = encode(types=['address', 'uint256'], args=[to_checksum_address(address), int(amount)])
        encoded_data_hex = to_hex(encoded_data)[2:]
        return encoded_data_hex
    elif enum.name == 'ERC_20':
        address = address
        encoded_data = encode(types=['address', 'uint256'], args=[to_checksum_address(address), int(amount)])
        return to_hex(encoded_data)[2:]
    elif enum.name == 'ERC_20_DIFF':
        address = address
        address1 = args[0]
        encoded_data = encode(types=['address', 'address', 'uint256'],
                              args=[to_checksum_address(address), to_checksum_address(address1), amount])
        return to_hex(encoded_data)[2:]
    elif enum.name == 'ERC_721':
        address = address
        address1 = args[0]
        encoded_data = encode(types=['address', 'address', 'uint256'],
                              args=[to_checksum_address(address), to_checksum_address(address1), amount])
        return to_hex(encoded_data)[2:]
    else:
        raise TypeError(f"Expected FuncSel enum,got {type(enum).__name__}")


def withdraw_encoder(enum: FuncSel, address, amount, *args):
    encoded_argument = _function_argument_encoder(enum, address, amount, *args)
    selector_signature = _function_selector_encoder(enum)
    final_encoding = selector_signature + encoded_argument
    return "0x" + final_encoding
