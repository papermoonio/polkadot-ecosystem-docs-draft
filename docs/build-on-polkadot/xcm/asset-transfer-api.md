---
title: Asset Transfer API
description: Asset Transfer API is a library that simplifies the transfer of assets for Substrate based chains. It provides methods for cross-chain and local transfers.
---

# Asset Transfer API

## Introduction

[Asset Transfer API](https://github.com/paritytech/asset-transfer-api){target=_blank}, a tool developed and maintained by [Parity](https://www.parity.io/){target=_blank}, is a specialized library designed to streamline asset transfers for Substrate-based blockchains. This API provides a simplified set of methods for users to:

- Execute asset transfers to other parachains or locally within the same chain
- Facilitate transactions involving system parachains like Asset Hub (Polkadot and Kusama)

The Asset Transfer API supports Parachain to Parachain transfers, currently limited to XCM V2, except for primary asset transactions. 

By using this API, developers can manage asset transfers more efficiently, reducing the complexity associated with cross-chain transactions and enabling smoother operations within the ecosystem.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/en/){target=_blank} (recommended version 21 or greater)
- Package manager - [npm](https://www.npmjs.com/){target=_blank} should be installed with Node.js by default. Alternatively, you can use other package managers like [Yarn](https://yarnpkg.com/){target=_blank}

## Install Asset Transfer API

To use `asset-transfer-api`, you need a JavaScript project. If you don't have one, you can create a new one:

1. Create a new directory for your project:
    ```bash
    mkdir my-asset-transfer-project \
    && cd my-asset-transfer-project
    ```

2. Initialize a new project:
    ```bash
    npm init -y
    ```

Once you have a project set up, you can install the asset-transfer-api package:

```bash
npm install @substrate/asset-transfer-api@{{build_on_polkadot.xcm.asset_transfer_api.version}}
```

!!!note
    This documentation covers version {{build_on_polkadot.xcm.asset_transfer_api.version}} of Asset Transfer API.

## Set Up Asset Transfer API

To initialize the Asset Transfer API, you need three key components:

- A Polkadot.js API instance
- The `specName` of the chain
- The XCM version to use

<!-- You can set up the API in two ways. Choose the option that best fits your project's structure and requirements. Both methods will result in a fully initialized AssetTransferApi instance ready for use:

### Using an Existing Polkadot.js API

If you already have an initialized Polkadot.js API instance, you can use it to set up the Asset Transfer API:

```javascript
// Assuming 'api' is your initialized Polkadot.js API instance
const { specName } = await api.rpc.state.getRuntimeVersion();
const safeXcmVersion = await fetchSafeXcmVersion(api);

const assetsApi = new AssetTransferApi(api, specName, safeXcmVersion);
```
-->

### Using helper function from library

For a simpler setup process, you can leverage the `constructApiPromise` helper function provided by the library. 

<!-- This method automatically initializes the Polkadot.js API, retrieves the specName, and determines the safe XCM version. -->

```javascript
import { AssetTransferApi, constructApiPromise } from '@substrate/asset-transfer-api';

async function main() {
    const { api, specName, safeXcmVersion } = await constructApiPromise('wss://westmint-rpc.polkadot.io');

    const assetsApi = new AssetTransferApi(api, specName, safeXcmVersion);

    // Your code using assetsApi goes here
}

main()
```

!!!note
    The code examples are enclosed in an async main function to provide the necessary asynchronous context. However, if you're already working within an async environment, you can use the code directly. The key is to ensure you're in an async context when working with these asynchronous operations, regardless of your specific setup.


## Asset Transfer API Overview

The AssetTransferApi provides a powerful method for cross-chain asset transfers: `createTransferTransaction`. This function allows you to create XCM transactions for transferring assets or native tokens between different chains in the Polkadot ecosystem.

```javascript
/**
 * Create an XCM transaction to transfer Assets, or native tokens from one
 * chain to another.
 *
 * @param destChainId ID of the destination (para) chain ('0' for Relaychain)
 * @param destAddr Address of destination account
 * @param assetIds Array of assetId's to be transferred
 * @param amounts Array of the amounts of each token to transfer
 * @param opts Options
 */
AssetTransferApi.createTransferTransaction(
  destChainId: string,
  destAddr: string,
  assetIds: string[],
  amounts: string[],
  opts?: TransferArgsOpts<T>
)
```

This method takes several parameters to specify the details of the transfer, including the destination chain, recipient address, assets to be transferred, and their amounts. Additionally, it accepts an optional `opts` parameter for further customization.

<!-- It can be configured with various options to tailor its behavior to your specific needs. These options include the ability to inject custom registry values, override existing registry data, and specify the registry type.

```javascript
type AssetTransferApiOpts = {
  injectedRegistry?: RequireAtLeastOne<ChainInfoRegistry>;
  overrideRegistry?: RequireAtLeastOne<ChainInfoRegistry<InjectedChainInfoKeys>>;
  registryType?: RegistryTypes;
};
``` 
-->

The `TransferArgsOpts` interface provides a wide range of options for customizing the transfer transaction. These options allow you to specify the transaction format, fee payment details, weight limits, XCM versions, and more.

```javascript
interface TransferArgsOpts<T extends Format> {
  format?: T;
  paysWithFeeOrigin?: string;
  paysWithFeeDest?: string;
  weightLimit?: { refTime?: string, proofSize?: string };
  xcmVersion?: number;
  keepAlive?: boolean;
  transferLiquidToken?: boolean;
  assetTransferType?: string;
  remoteReserveAssetTransferTypeLocation?: string;
  feesTransferType?: string;
  remoteReserveFeesTransferTypeLocation?: string;
  customXcmOnDest?: string;
}
```

By utilizing these options, you can fine-tune your asset transfers to meet specific requirements, such as specifying custom XCM messages, handling different asset types, and managing fee payments across chains.


## Asset Transfer Capabilities

The `AssetTransferApi.createTransferTransaction` is able to infer what kind of transaction is necessary given the inputs. When sending cross-chain transfers, the API performs extensive validation to ensure the inputs are valid, and the assets either exist or don't.

Each possible transfer types can be initiated using the same `createTransferTransaction` method, with the API intelligently determining the appropriate transaction type based on the provided parameters and options.

There are different types of transfers supported by the API:



