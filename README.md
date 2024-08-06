---
# CartesiNexus

**CartesiNexus** is a Python library for handling blockchain-related operations, particularly focused on Cartesi ecosystem. It provides utilities for creating and managing various types of blockchain outputs and managing token transactions(withdrawing,transferring and depositing of assets).

# Why this?
This library was created to give me an insight of how the cartesi ecosystem works at a certain level,also it was created due to the small number of cartesi library  that is available,hence this library quickly get you up to speed. At the moment the library covers most operations on ether,erc20 and erc721 tokens.

## Features
- Handle Ether, ERC20, and ERC721 token operations(more tokens would soon be supported)
- Manages assets for different token types
- Create and manage outputs(Notices,Reports,Vouchers)
- Encode and decode ABI payloads for token transactions


## Installation

### Using pip

```
     
     pip install cartesi-nexus

```

### From GitHub
To get started with cartesi-nexus , clone this repository and install the required dependencies.

```
git clone https://github.com/jerrygeorge360/cartesi-nexus
cd cartesi_nexus
pip install -r requirements.txt
```


## Usage
To import the necessary methods

`from cartesi-nexus import str2hex,hex2str,withdraw,get_token,deposit,get_all_token`

### Checking Balance

To retrieve the balance information for a specific asset, use the `get_token` method,for all the assets for a specific address use `get_all_token`. This method should be called within the inspect function:


```python
data = get_token(account:str,token_name:str)
```
to get all tokens related to an address

```data = get_all_token(account:str)```
## Asset Handling Methods

For operations such as deposits, transfers and withdrawals, use the methods inside the handle_advance function.


### Deposits

To process a deposit, ensure the sender is the designated portals smart contract (e.g., the default ERC20Portal smart contract from sunodo or nonodo when running locally). You might need to adjust the smart contract address based on your deployment or dynamically retrieve it from a resource file:

### Withdrawal
To withdraw an asset



```python 
    withdraw_ether = withdraw_obj(FuncSel.ETHER,'0xadress',200)
    withdraw_erc20 = withdraw(FuncSel.ERC_20,'0xaddress',200)
    withdraw_20_to = withdraw(FuncSel.ERC_20_DIFF,'0xaddress',200,'0xaddress1')
    withdraw_erc721 = withdraw(FuncSel.ERC_721,'0xaddress',200,'0xaddress1')
```
where FuncSel is an enum that provides the type of asset
- FuncSel.ETHER
- FuncSel.ERC20
- FuncSel.ERC721
- FuncSel.ERC_20_DIFF
### Transfer
This operation transfers tokens within the Dapp ecosystem.
The method transfer is used to initiate the operation
the payload should be formatted in the form and then converted to a hex string

`payload = {'method': 'transfer',
'payload': {'sender_address': sender_address, 'destination_address': dest, 'amount': amount,
'data': args}}`

`transfer(token_type: str, payload) where token type is the asset(eth,erc20,erc721) where payload is in hex format.`
``` python
transfer('eth',payload)
transfer('erc20',payload)
transfer('erc721,payload) 
```



### Hex to String Conversions
The two methods for this are:
`str2hex` and `hex2str`

```python
from cartesi_nexus.helpers import str2hex,hex2str

converted_string = hex2str(payload)
converted_hex = str2hex(payload)

```