---
# Deposit Input Payloads

Deposit input payloads are always specified as packed ABI-encoded parameters. For more details, refer to the [documentation](https://docs.cartesi.io/cartesi-rollups/1.3/development/asset-handling/).

## Ether Deposit

**Payload:**
- **Sender Address:** 20 bytes
- **Amount:** 32 bytes
- **Arbitrary Data:** For the dapp

## ERC20 Deposit

**Payload:**
- **Success:** 1 byte
- **Token Address:** 20 bytes
- **Sender Address:** 20 bytes
- **Amount:** 32 bytes
- **Arbitrary Data:** For the dapp

## ERC721 Deposit

**Payload:**
- **Token Address:** 20 bytes
- **Sender Address:** 20 bytes
- **Token ID:** 32 bytes
- **Arbitrary Data:** For the dapp

Address(address)
Amount/ID(uint256)
---