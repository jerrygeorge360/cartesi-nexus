import json
from unittest import TestCase, main
from cartesi_nexus.abi_withdraw_encoder import FuncSel
from cartesi_nexus.token_manager import TokenManager
from cartesi_nexus.transactions import transfer_token
from cartesi_nexus.helpers import str2hex
from cartesi_nexus.transactions import transfer_decode_payload, withdraw, deposit, get_token, get_all_tokens


def test_generate_mock_transfer_data(method, sender_address, dest, amount, *args, **kwargs):
    # sender_address, destination_address, amount, *data = pythonic_payload
    payload = {'method': method,
               'payload': {'sender_address': sender_address, 'destination_address': dest, 'amount': amount,
                           'data': args}}
    json_payload = json.dumps(payload)
    return str2hex(json_payload)


def open_test_file(token_type):
    with open('../tests/test_details.json', 'r') as f:
        data = f.read()
    data = json.loads(data)
    if token_type == 'eth':
        return json.dumps(data[0])
    elif token_type == 'erc20':
        return json.dumps(data[1])
    elif token_type == 'erc721':
        return json.dumps(data[2])
    else:
        raise ValueError('value should be eth,erc20 or erc721')


class TestTransactions(TestCase):

    def setUp(self) -> None:
        self.expected_ether_hex = '0x7b227061796c6f6164223a207b2274797065223a202265' \
                                  '746865725f7472616e73666572222c202264617461223a207b2266726f' \
                                  '6d223a2022307864616461222c2022746f223a202230616461666168222' \
                                  'c2022616d6f756e74223a20343030307d7d7d '
        self.expected_erc20hex = '0x7b227061796c6f6164223a207b2274797065223a202265726332305f7472' \
                                 '616e73666572222c202264617461223a207b' \
                                 '22746f6b656e5f74797065223a2022617065222c202266726f6d223a20223078646164' \
                                 '61222c2022746f223a202230616461666' \
                                 '168222c2022616d6f756e74223a20343030307d7d7d'
        self.expected_erc721hex = '0x7b227061796c6f6164223a207b2274797065223a20' \
                                  '226572633732315f7472616e73666572222c202264617' \
                                  '461223a207b226e66745f6964223a2022333232222c202' \
                                  '26e66745f6e616d65223a2022616461646164222c202266' \
                                  '726f6d223a2022307864616461222c2022746f223a20223061646166616822' \
                                  '2c2022616d6f756e74223a20343030307d7d7d'
        self.transaction = transfer_token

        self.expected_deposit_erc20 = {'payload': {'amount': 1000000,
                                                   'arbitrary_data': 'Hello, World!',
                                                   'sender_address': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
                                                   'success': 1,
                                                   'token_address': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'}}

        self.expected_deposit_erc721 = {'payload': {'token_address': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
                                                    'sender_address': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
                                                    'token_id': 123456, 'arbitrary_data': 'NFT Traesfer'}}

        self.eth_transfer_data = test_generate_mock_transfer_data('get', '0xdada', '0adafah', 4000, 'adadad')
        self.erc20_transfer_data = test_generate_mock_transfer_data('get', '0xdada', '0adafah', 4000,
                                                                    {'token_type': 'ape'})
        self.erc721_transfer_data = test_generate_mock_transfer_data('get', '0xdada', '0adafah', 4000,
                                                                     {'nft_id': 322, 'nft_name': 'adadad'})

        self.withdraw_erc_20 = '0xa9059cbb000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e0000000000000000000000000000000000000000000000000000000000000028 '
        self.withdraw_erc_20_diff = '0x23b872dd000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e0000000000000000000000000000000000000000000000000000000000000028'
        self.withdraw_erc_721 = '0x42842e0e000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e0000000000000000000000000000000000000000000000000000000000000028'
        self.withdraw_ether = '0x522f6815000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e0000000000000000000000000000000000000000000000000000000000000028'

    def test_transfer_decoder(self):
        hex_data = test_generate_mock_transfer_data('transfer_ether', '0axakdd', '0xadjfa', 2000, '322', 'addd')
        test_data = ('0axakdd', '0xadjfa', 2000, ['322', 'addd'])
        self.assertEqual(transfer_decode_payload(hex_data), test_data)

    def test_transfer_eth(self):
        self.assertEqual(self.transaction('eth', payload=self.eth_transfer_data), self.expected_ether_hex.strip(' '))

    def test_transfer_erc20(self):
        self.assertEqual(self.transaction('erc20', payload=self.erc20_transfer_data), self.expected_erc20hex)

    def test_transfer_erc721(self):
        token_manager_sender = TokenManager(account='0xdada')
        token_manager_sender.add_nft_token('adadad', '322')
        self.assertEqual(self.transaction('erc721', payload=self.erc721_transfer_data), self.expected_erc721hex)

    def test_deposit_eth(self):
        data = deposit('eth', payload=open_test_file('eth'))
        self.assertEqual(data.python_payload, {'payload': {'amount': 1.0,
                                                           'sender_address': '0x70997970C51812dc3A010C7d01b50e0d17dc79C8'}})

    def test_deposit_erc20(self):
        data = deposit('erc20', payload=open_test_file('erc20'))
        self.assertEqual(data.python_payload, self.expected_deposit_erc20)

    def test_deposit_erc721(self):
        data = deposit('erc721', payload=open_test_file('erc721'))
        self.assertEqual(data.python_payload, self.expected_deposit_erc721)

    def test_withdraw_eth(self):
        data = withdraw(FuncSel.ETHER, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 40,
                        '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(data.payload, self.withdraw_ether.strip(' '))
        self.assertEqual(data.destination, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')

    def test_withdraw_erc20(self):
        data = withdraw(FuncSel.ERC_20, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 40,
                        '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(data.payload, self.withdraw_erc_20.strip(' '))

        self.assertEqual(data.destination, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')

    def test_withdraw_erc20_diff(self):
        data = withdraw(FuncSel.ERC_20_DIFF, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 40,
                        '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(data.payload, self.withdraw_erc_20_diff.strip(' '))
        self.assertEqual(data.destination_to, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(data.destination, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')

    def test_withdraw_erc721(self):
        data = withdraw(FuncSel.ERC_721, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 40,
                        '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(data.payload, self.withdraw_erc_721)
        self.assertEqual(data.destination, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(data.destination_to, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')

    def test_get_ether_balance(self):
        obj = get_token('0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 'eth')
        self.assertEqual(obj, 0)

    def test_get_erc20_balance(self):
        obj = get_token('0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 'erc20')
        self.assertEqual(obj, {})

    def test_get_erc721_balance(self):
        obj = get_token('0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 'erc721')
        self.assertEqual(obj, {})


if __name__ == "__main__":
    main()
