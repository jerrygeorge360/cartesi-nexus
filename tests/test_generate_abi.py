import binascii
import binascii


def generate_ether_payload(sender_address, amount, arbitrary_data):
    # Convert sender address to 20 bytes (hex)
    sender_address_hex = binascii.unhexlify(sender_address[2:]).rjust(20, b'\x00')

    # Convert amount to 32 bytes (big-endian)
    amount_bytes = amount.to_bytes(32, 'big')

    # Pad arbitrary data to 32 bytes
    arbitrary_data_padded = arbitrary_data.ljust(64, '0')
    arbitrary_data_bytes = binascii.unhexlify(arbitrary_data_padded)

    # Concatenate all parts
    payload = sender_address_hex + amount_bytes + arbitrary_data_bytes
    return binascii.hexlify(payload).decode()


def generate_erc20_payload(success, token_address, sender_address, amount, arbitrary_data):
    # Convert success to 1 byte
    success_byte = success.to_bytes(1, 'big')

    # Convert addresses to 20 bytes each (hex)
    token_address_hex = binascii.unhexlify(token_address[2:]).rjust(20, b'\x00')
    sender_address_hex = binascii.unhexlify(sender_address[2:]).rjust(20, b'\x00')

    # Convert amount to 32 bytes (big-endian)
    amount_bytes = amount.to_bytes(32, 'big')

    # Pad arbitrary data to 32 bytes
    arbitrary_data_padded = arbitrary_data.ljust(64, '0')
    arbitrary_data_bytes = binascii.unhexlify(arbitrary_data_padded)

    # Concatenate all parts
    payload = success_byte + token_address_hex + sender_address_hex + amount_bytes + arbitrary_data_bytes
    return binascii.hexlify(payload).decode()


def generate_erc721_payload(token_address, sender_address, token_id, arbitrary_data):
    # Convert addresses to 20 bytes each (hex)
    token_address_hex = binascii.unhexlify(token_address[2:]).rjust(20, b'\x00')
    sender_address_hex = binascii.unhexlify(sender_address[2:]).rjust(20, b'\x00')

    # Convert token ID to 32 bytes (big-endian)
    token_id_bytes = token_id.to_bytes(32, 'big')

    # Pad arbitrary data to 32 bytes
    arbitrary_data_padded = arbitrary_data.ljust(64, '0')
    arbitrary_data_bytes = binascii.unhexlify(arbitrary_data_padded)

    # Concatenate all parts
    payload = token_address_hex + sender_address_hex + token_id_bytes + arbitrary_data_bytes
    return binascii.hexlify(payload).decode()


