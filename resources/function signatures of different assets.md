---
# Function Signatures of Different Assets [according to Cartesi documentation](https://docs.cartesi.io/cartesi-rollups/1.3/development/asset-handling/)

## Withdrawal Operations

### Ether
- **Function Signature**: `withdrawEther(address, uint256)`

### ERC20
- **Function Signature**: `transfer(address, uint256)`

### ERC20 (Transferring to a Different Address)
- **Function Signature**: `transferFrom(address, address, uint256)`

### ERC721
- **Function Signature**: `safeTransferFrom(address, address, uint256)`

### ERC721 (with additional data)
- **Function Signature**: `safeTransferFrom(address, address, uint256, bytes)`

---