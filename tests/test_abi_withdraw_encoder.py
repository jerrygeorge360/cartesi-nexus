from unittest import TestCase, main
from cartesi_nexus.abi_withdraw_encoder import withdraw_encoder, FuncSel


class TestABIWithDrawEncoder(TestCase):

    def setUp(self) -> None:
        self.withdraw_erc_20 = '0xa9059cbb000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e0000000000000000000000000000000000000000000000000000000000000028 '.strip(' ')
        self.withdraw_erc_20_diff = '0x23b872dd000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e0000000000000000000000000000000000000000000000000000000000000028'.strip(' ')
        self.withdraw_erc_721 = '0x42842e0e000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e0000000000000000000000000000000000000000000000000000000000000028'.strip(' ')
        self.withdraw_ether = '0x522f6815000000000000000000000000742d35cc6634c0532925a3b844bc454e4438f44e0000000000000000000000000000000000000000000000000000000000000028'.strip(' ')

    def test_withdraw_ether_encoding(self):
        result = withdraw_encoder(FuncSel.ETHER, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 40,
                                  '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(result, self.withdraw_ether)

    def test_withdraw_ether20_encoding(self):
        result = withdraw_encoder(FuncSel.ERC_20, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 40,
                                  '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(result, self.withdraw_erc_20)

    def test_withdraw_ether20_diff_encoding(self):
        result = withdraw_encoder(FuncSel.ERC_20_DIFF, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 40,
                                  '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(result, self.withdraw_erc_20_diff)

    def test_withdraw_erc721_encoding(self):
        result = withdraw_encoder(FuncSel.ERC_721, '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 40,
                                  '0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        self.assertEqual(result, self.withdraw_erc_721)

    # def tearDown(self) -> None:



if __name__ == "__main__":
    main()
