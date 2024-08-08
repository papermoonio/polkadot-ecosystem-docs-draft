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
    This documentation covers version `{{build_on_polkadot.xcm.asset_transfer_api.version}}` of Asset Transfer API.

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

main();
```

!!!note
    The code examples are enclosed in an async main function to provide the necessary asynchronous context. However, if you're already working within an async environment, you can use the code directly. The key is to ensure you're in an async context when working with these asynchronous operations, regardless of your specific setup.


## Asset Transfer API Overview

The AssetTransferApi provides a powerful method for cross-chain asset transfers: `createTransferTransaction`. This function allows you to create XCM transactions for transferring assets or native tokens between different chains.
This method takes several parameters to specify the details of the transfer, including the destination chain, recipient address, assets to be transferred, their amounts and an optional parameter for further customization.

```javascript
public async createTransferTransaction<T extends Format>(
  destChainId: string,
  destAddr: string,
  assetIds: string[],
  amounts: string[],
  opts: TransferArgsOpts<T> = {},
): Promise<TxResult<T>>
```

### Parameters

- `destChainId` ++"string"++ - ID of the destination chain ('0' for Relay chain, other values for parachains)
- `destAddr` ++"string"++ - Address of the recipient account on the destination chain
- `assetIds` ++"string[]"++ - Array of asset identifiers to be transferred
- `amounts` ++"string[]"++ - Array of amounts corresponding to each asset in `assetIds`
- `opts` ++"TransferArgsOpts<T>"++ - Additional options for the transfer transaction

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

<!-- TODO: Add more information regarding what the parameters do -->

- `format` ++"T"++ - Specifies the format for returning a transaction (payload, call, or submittable)

	```javascript
	export type Format = 'payload' | 'call' | 'submittable';
	```

	AssetTransferApi supports three formats to be returned:

	- payload - returns a Polkadot-js `ExtrinsicPayload` as a hex. Default
	- call - returns a Polkadot-js `Call` as a hex
	- submittable - returns a Polkadot-js `SubmittableExtrinsic`
  
- `paysWithFeeOrigin` ++"string"++ - AssetId to pay fees on the current common good parachain

        - Polkadot AssetHub - default DOT
        - Kusama AssetHub - default KSM

- `paysWithFeeDest` ++"string"++ - AssetId to pay fees on the destination parachain
- `weightLimit` ++{ refTime?: string, proofSize?: string }++ - Custom weightLimit option

		If not inputted it will default to `Unlimited`

- `xcmVersion` ++"number"++ - Sets the xcmVersion for message construction

		If this is not present a supported version will be queried, and if there is no supported version a safe version will be queried

- `keepAlive` ++"boolean"++ - Enables transferKeepAlive for local asset transfers
  
  		For creating local asset transfers, if true this will allow for a `transferKeepAlive` as oppose to a `transfer`

- `transferLiquidToken` ++"boolean"++ - Declares if this will transfer liquidity tokens
  
		Default is false

- `assetTransferType` ++"string"++ - XCM TransferType used to transfer assets
- `remoteReserveAssetTransferTypeLocation` ++"string"++ - RemoteReserve location for XCM transfer
- `feesTransferType` ++"string"++ - XCM TransferType used to pay fees for XCM transfer
- `remoteReserveFeesTransferTypeLocation` ++"string"++ - RemoteReserve location for XCM transfer fees
- `customXcmOnDest` ++"string"++ - Optional custom XCM message to be executed on destination chain
  
  		Should be provided if a custom xcm message is needed after transfering assets. Defaults to `Xcm(vec![DepositAsset { assets: Wild(AllCounted(assets.len())), beneficiary }])`

By utilizing these options, you can fine-tune your asset transfers to meet specific requirements, such as specifying custom XCM messages, handling different asset types, and managing fee payments across chains

### Result

```javascript
export interface TxResult<T> {
    dest: string;
    origin: string;
    format: Format | 'local';
    xcmVersion: number | null;
    direction: Direction | 'local';
    method: Methods;
    tx: ConstructedFormat<T>;
}
```

- `dest` ++"string"++ - The destination specName of the transaction
- `origin` ++"string"++ - The origin specName of the transaction
- `format` ++"Format | 'local'"++ - The format type the tx is outputted in
- `xcmVersion` ++"number | null"++ - The xcm version that was used to construct the tx
- `direction` ++"Direction | 'local'"++ - The direction of the cross chain transfer
- `method` ++"Methods"++ - The method used in the transaction
- `tx` ++"ConstructedFormat<T>"++ - The constructed transaction


## Asset Transfer Capabilities

The `AssetTransferApi.createTransferTransaction` is able to infer what kind of transaction is necessary given the inputs. When sending cross-chain transfers, the API performs extensive validation to ensure the inputs are valid, and the assets either exist or don't

Each possible transfer types can be initiated using the same `createTransferTransaction` method, with the API intelligently determining the appropriate transaction type based on the provided parameters and options.

## Examples

### Using xTokens pallet

When initiating a transfer from a parachain that implements the `xTokens` pallet, the API automatically detects this configuration and constructs the appropriate transaction. Depending on the transfer requirements, the API will generate one of three possible calls:

- [`transferMultiasset`](https://github.com/open-web3-stack/open-runtime-module-library/blob/144a9625bc0cbd1afb81088f4d8a79a931811b49/xtokens/src/lib.rs#L249){target=_blank}
- [`transferMultiassets`](https://github.com/open-web3-stack/open-runtime-module-library/blob/144a9625bc0cbd1afb81088f4d8a79a931811b49/xtokens/src/lib.rs#L383){target=_blank}
- [`transferMultiassetWithFee`](https://github.com/open-web3-stack/open-runtime-module-library/blob/144a9625bc0cbd1afb81088f4d8a79a931811b49/xtokens/src/lib.rs#L321){target=_blank}

```javascript

import { AssetTransferApi, constructApiPromise } from '@substrate/asset-transfer-api';

async function main() {
    const { api, specName, safeXcmVersion } = await constructApiPromise('<INSERT_PARACHAIN_ENDPOINT>');

    const assetsApi = new AssetTransferApi(api, specName, safeXcmVersion);

    assetsApi.createTransferTransaction(
		'1000',
		'0xc4db7bcb733e117c0b34ac96354b10d47e84a006b9e7e66a229d174e8ff2a063',
		['xcUSDT'],
		['1000000'],
	);
}

main();
```





