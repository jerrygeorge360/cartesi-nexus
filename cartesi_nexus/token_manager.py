import threading


class MultitonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        key = None
        if 'account' in kwargs:
            key = kwargs['account']
        elif len(args) >= 1:
            key = args[0]
        else:
            raise ValueError('address is expected')
        with cls._lock:
            if key not in cls._instances:
                cls._instances[key] = super().__call__(*args, **kwargs)
            return cls._instances[key]


class TokenManager(metaclass=MultitonMeta):
    def __init__(self, account: str, ether: float = 0.0, erc20: dict[str, float] = None, erc721: dict[str, set] = None):
        self._account = account
        self._ether = ether
        self._erc20 = erc20 if erc20 else {}  # stores multiple tokens
        self._erc721 = erc721 if erc721 else {}  # stores multiple nfts
        self._total = {'ether': self._ether, 'erc20 tokens': self.erc20, 'nfts': self._erc721}

    @property
    def ether(self):
        """
        :return:float.
        """
        return self._ether

    @ether.setter
    def ether(self, value):
        self._ether = value

    def ether_increase(self, amount: float):
        if amount <= 0.0:
            raise ValueError(f'failed to increase ether.', f'increment amount should be > 0.0')
        new_amount = self._ether + amount
        self._ether = new_amount

    def ether_decrease(self, amount: float):
        if amount <= 0.0:
            raise ValueError(f'failed to decrease ether.', f'decrement amount should be > 0.0')
        new_amount = self._ether - amount
        self._ether = new_amount

    @property
    def erc20(self):
        """

        :return: dict of all tokens
        """
        return self._erc20

    @erc20.setter
    def erc20(self, value):
        self._erc20 = value

    def _get_erc20_token_amount(self, erc20_name: str):
        """
        gets your specified token amount

        :param erc20_name
        :return: float
        """
        amount = self._erc20.get(erc20_name, 0.0)
        return amount

    def _set_erc20_token_amount(self, erc20_name: str, amount: float):
        self._erc20[erc20_name] = amount

    def erc20_increase(self, erc20_name: str, amount: float):
        """

        :type erc20_name: str
        """
        if amount <= 0.0:
            raise ValueError(f'failed to increase {erc20_name}.', f'increment amount should be > 0.0')
        new_amount = self._get_erc20_token_amount(erc20_name) + amount
        self._set_erc20_token_amount(erc20_name, new_amount)

    def erc20_decrease(self, erc20_name: str, amount: float):
        """

                :param amount:
                :type erc20_name: str
                """
        if amount <= 0.0:
            raise ValueError(f'failed to increase {erc20_name}.', f'increment amount should be > 0.0')
        new_amount = self._get_erc20_token_amount(erc20_name) - amount
        self._set_erc20_token_amount(erc20_name, new_amount)

    @property
    def erc721(self):
        return self._erc721

    @erc721.setter
    def erc721(self, value):
        self._erc721 = value

    def add_nft_token(self, nft_name: str, nft_id: str):
        if nft_name in self._erc721:
            self._erc721[nft_name].add(str(nft_id))
        else:
            self._erc721[nft_name] = {nft_id}

    def remove_nft_token(self, nft_name: str, nft_id: str):
        # Check if the nft_name exists in the dictionary
        if nft_name not in self._erc721:
            raise ValueError(f'NFT collection "{nft_name}" does not exist.')

        # Attempt to remove the nft_id from the set
        try:
            self._erc721[nft_name].remove(nft_id)
        except KeyError:
            raise ValueError(f'NFT ID "{nft_id}" does not exist in the collection "{nft_name}".')

        # If the set is empty after removal, optionally remove the collection
        if not self._erc721[nft_name]:
            del self._erc721[nft_name]

    @property
    def get_total(self):
        return self._total

