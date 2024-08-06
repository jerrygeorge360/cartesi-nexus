import unittest
from cartesi_nexus.token_manager import TokenManager


class TestTokenManager(unittest.TestCase):

    def setUp(self) -> None:
        TokenManager._instances = {}
        address = '0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e'  # dapp address
        self.token_manager = TokenManager(address)

    def test_check_multiton(self):
        tm1 = TokenManager('account1')
        tm2 = TokenManager('account1')
        tm3 = TokenManager('account2')
        self.assertIs(tm1, tm2, "TokenManager should be a multiton")
        self.assertIsNot(tm3, tm2)

    def test_ether_increase(self):
        self.token_manager.ether_increase(1.0)
        self.assertEqual(self.token_manager._ether, 1.0)

    def test_ether_decrease(self):
        self.token_manager.ether_decrease(1.0)
        self.assertEqual(self.token_manager._ether, -1.0)

    def test_get_erc20(self):
        self.assertEqual(self.token_manager._erc20, {})

    def test_erc20_increase(self):
        self.token_manager.erc20_increase('ape', 20.0)
        self.assertEqual(self.token_manager._get_erc20_token_amount('ape'), 20.0)

    def test_erc20_decrease(self):
        self.token_manager.erc20_increase('ape', 25.0)
        self.token_manager.erc20_decrease('ape', 10.0)
        self.assertEqual(self.token_manager._get_erc20_token_amount('ape'), 15.0)

    def test_get_erc721(self):
        self.assertEqual(self.token_manager._erc721, {})

    def test_erc721_add(self):
        self.token_manager.add_nft_token('ape', '0xsdhfhaafk')
        self.token_manager.add_nft_token('ape', '0xkhfaidhi')
        self.assertEqual(self.token_manager.erc721['ape'], {'0xsdhfhaafk', '0xkhfaidhi'})

    def test_erc721_remove(self):
        self.token_manager.add_nft_token('ape', '0xsdhfhaafk')
        self.token_manager.add_nft_token('ape', '0xkhfaidhi')
        self.token_manager.remove_nft_token('ape', '0xkhfaidhi')
        self.assertEqual(self.token_manager.erc721['ape'], {'0xsdhfhaafk'})
