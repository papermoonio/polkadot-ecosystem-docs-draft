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

For additional support and information, please reach out through [GitHub Issues](https://github.com/paritytech/asset-transfer-api/issues){target=_blank}.

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
    const { api, specName, safeXcmVersion } = await constructApiPromise('<INSERT_WEBSOCKET_URL>');

    const assetsApi = new AssetTransferApi(api, specName, safeXcmVersion);

    // Your code using assetsApi goes here
}

main();
```

!!!note
    The code examples are enclosed in an async main function to provide the necessary asynchronous context. However, if you're already working within an async environment, you can use the code directly. The key is to ensure you're in an async context when working with these asynchronous operations, regardless of your specific setup.


## Asset Transfer API Overview

The AssetTransferApi provides a powerful method for cross-chain asset transfers: `createTransferTransaction`. This function allows you to create XCM transactions for transferring assets or native tokens between different chains.
This method takes several parameters to specify the details of the transfer, including the destination chain, recipient address, assets to be transferred, their amounts and an optional parameter for further customization. It is able to infer what kind of transaction is necessary given the inputs. When sending cross-chain transfers, the API performs extensive validation to ensure the inputs are valid, and the assets either exist or don't.

!!! note
	The `createTransferTransaction` function is designed to be a utility that simplifies the creation of the transaction. It does not sign or submit the created transaction on the blockchain. It simply generates the transaction in the requested format (e.g., payload, call, or submittable). After obtaining the transaction from the `createTransferTransaction` function, you will need to handle the signing and submission process separately.

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
  
  If a token or assetId is provided as input, the API will resolve to using the `tokens` pallet. When no asset is passed in, the API will default to using the `balances` pallet.

- `amounts` ++"string[]"++ - Array of amounts corresponding to each asset in `assetIds`
- `opts` ++"TransferArgsOpts<T>"++ - Additional options for the transfer transaction

	??? code "Type `TransferArgsOpts`"

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

		- `format` ++"T extends Format"++ - Specifies the format for returning a transaction

			??? code "Type `Format`"
				```javascript
				export type Format = 'payload' | 'call' | 'submittable';
				```
		
		- `paysWithFeeOrigin` ++"string"++ - AssetId to pay fees on the current common good parachain

    		- Polkadot AssetHub - default DOT
    		- Kusama AssetHub - default KSM

		- `paysWithFeeDest` ++"string"++ - AssetId to pay fees on the destination parachain
		- `weightLimit` ++"{ refTime?: string, proofSize?: string }"++ - Custom weightLimit option

			If not inputted it will default to unlimited

		- `xcmVersion` ++"number"++ - Sets the xcmVersion for message construction

			If this is not present a supported version will be queried, and if there is no supported version a safe version will be queried

		- `keepAlive` ++"boolean"++ - Enables transferKeepAlive for local asset transfers
		
			For creating local asset transfers, if true this will allow for a `transferKeepAlive` as oppose to a `transfer`

		- `transferLiquidToken` ++"boolean"++ - Declares if this will transfer liquidity tokens
		
			Default is false

		- `assetTransferType` ++"string"++ - XCM TransferType used to transfer assets

			The `AssetTransferType` type defines the possible values for this parameter.
			??? code "Type `AssetTransferType`"
				```javascript
				export type AssetTransferType = LocalReserve | DestinationReserve | Teleport | RemoteReserve;
				```

			!!!note
				To use the `assetTransferType` parameter, which is a string, you should use the `AssetTransferType` type as if each of its variants are strings. For example, assetTransferType = 'LocalReserve'.

		- `remoteReserveAssetTransferTypeLocation` ++"string"++ - RemoteReserve location for XCM transfer

			Should be provided when specifying an `assetTransferType` of `RemoteReserve`.

		- `feesTransferType` ++"string"++ - XCM TransferType used to pay fees for XCM transfer
  
			The `AssetTransferType` type defines the possible values for this parameter.
			??? code "Type `AssetTransferType`"
				```javascript
				export type AssetTransferType = LocalReserve | DestinationReserve | Teleport | RemoteReserve;
				```

			!!!note
				To use the `feesTransferType` parameter, which is a string, you should use the `AssetTransferType` type as if each of its variants are strings. For example, feesTransferType = 'LocalReserve'.


		- `remoteReserveFeesTransferTypeLocation` ++"string"++ - RemoteReserve location for XCM transfer fees

			Should be provided when specfying a `feesTransferType` of `RemoteReserve`.

		- `customXcmOnDest` ++"string"++ - Optional custom XCM message to be executed on destination chain
		
			Should be provided if a custom xcm message is needed after transfering assets. Defaults to:
			```bash
			Xcm(vec![DepositAsset { assets: Wild(AllCounted(assets.len())), beneficiary }])
			```

### Return value

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
	
	??? code "Type `Format`"
		```javascript
		export type Format = 'payload' | 'call' | 'submittable';
		```

- `xcmVersion` ++"number | null"++ - The xcm version that was used to construct the tx
- `direction` ++"Direction | 'local'"++ - The direction of the cross chain transfer

	??? code "Type `Direction`"
		```javascript
		export enum Direction {
			Local = 'Local',
			SystemToPara = 'SystemToPara',
			SystemToRelay = 'SystemToRelay',
			SystemToSystem = 'SystemToSystem',
			SystemToBridge = 'SystemToBridge',
			ParaToPara = 'ParaToPara',
			ParaToRelay = 'ParaToRelay',
			ParaToSystem = 'ParaToSystem',
			RelayToSystem = 'RelayToSystem',
			RelayToPara = 'RelayToPara',
			RelayToBridge = 'RelayToBridge',
		}
		```

- `method` ++"Methods"++ - The method used in the transaction

	??? code "Type `Methods`"
  
		```javascript
		export type Methods =
			| LocalTransferTypes
			| 'transferAssets'
			| 'transferAssetsUsingTypeAndThen'
			| 'limitedReserveTransferAssets'
			| 'limitedTeleportAssets'
			| 'transferMultiasset'
			| 'transferMultiassets'
			| 'transferMultiassetWithFee'
			| 'claimAssets';
		```

		??? code "Type `LocalTransferTypes`"

			```javascript
			export type LocalTransferTypes =
				| 'assets::transfer'
				| 'assets::transferKeepAlive'
				| 'foreignAssets::transfer'
				| 'foreignAssets::transferKeepAlive'
				| 'balances::transfer'
				| 'balances::transferKeepAlive'
				| 'poolAssets::transfer'
				| 'poolAssets::transferKeepAlive'
				| 'tokens::transfer'
				| 'tokens::transferKeepAlive';
			```

- `tx` ++"ConstructedFormat<T>"++ - The constructed transaction

	??? code "Type `ConstructedFormat<T>`"

		```javascript
		export type ConstructedFormat<T> = T extends 'payload'
		? GenericExtrinsicPayload
		: T extends 'call'
		? `0x${string}`
		: T extends 'submittable'
			? SubmittableExtrinsic<'promise', ISubmittableResult>
			: never;
		```

		The `ConstructedFormat` type is a conditional type that returns a specific type based on the value of the TxResult `format` field.

		- Payload Format - if the format field is set to 'payload', the ConstructedFormat type will return a [GenericExtrinsicPayload](https://github.com/polkadot-js/api/blob/3b7b44f048ff515579dd233ea6964acec39c0589/packages/types/src/extrinsic/ExtrinsicPayload.ts#L48)
		- Call Format - if the format field is set to 'call', the ConstructedFormat type will return a hexadecimal string (0x${string}). This is the encoded representation of the extrinsic call
		- Submittable Format - if the format field is set to 'submittable', the ConstructedFormat type will return a [SubmittableExtrinsic](https://github.com/polkadot-js/api/blob/3b7b44f048ff515579dd233ea6964acec39c0589/packages/api-base/src/types/submittable.ts#L56). This is a Polkadot-JS type that represents a transaction that can be submitted to the blockchain

## Examples

### Relay to System Parachain

This example demonstrates how to initiate a cross-chain token transfer from a relay chain to a system parachain. Specifically, 1 WND will be transfered from a Westend (Relay Chain) account to a Westmint (System Parachain) account.

```javascript
import {
  AssetTransferApi,
  constructApiPromise,
} from "@substrate/asset-transfer-api";

async function main() {
  const { api, specName, safeXcmVersion } = await constructApiPromise(
    "wss://westend-rpc.polkadot.io"
  );
  const assetApi = new AssetTransferApi(api, specName, safeXcmVersion);
  let callInfo;
  try {
    callInfo = await assetApi.createTransferTransaction(
      "1000",
      "5EWNeodpcQ6iYibJ3jmWVe85nsok1EDG8Kk3aFg8ZzpfY1qX",
      ["WND"],
      ["1000000000000"],
      {
        format: "call",
        xcmVersion: safeXcmVersion,
      }
    );

    console.log(`Call data:\n${JSON.stringify(callInfo, null, 4)}`);
  } catch (e) {
    console.error(e);
    throw Error(e as string);
  }

  const decoded = assetApi.decodeExtrinsic(callInfo.tx, "call");
  console.log(
    `\nDecoded tx:\n ${JSON.stringify(JSON.parse(decoded), null, 4)}`
  );
}

main()
  .catch((err) => console.error(err))
  .finally(() => process.exit());
```

<div id="termynal" data-termynal>
    <span data-ty="input"><span class="file-path"></span>ts-node relayToSystem.ts</span>
    <br>
	<span data-ty>Call data:</span>
	<span data-ty>{</span>
	<span data-ty>    "origin": "westend",</span>
	<span data-ty>    "dest": "westmint",</span>
	<span data-ty>    "direction": "RelayToSystem",</span>
	<span data-ty>    "xcmVersion": 3,</span>
	<span data-ty>    "method": "transferAssets",</span>
	<span data-ty>    "format": "call",</span>
	<span data-ty>    "tx": "0x630b03000100a10f03000101006c0c32faf970eacb2d4d8e538ac0dab3642492561a1be6f241c645876c056c1d030400000000070010a5d4e80000000000"</span>
	<span data-ty>}</span>
	<span data-ty></span>
	<span data-ty>Decoded tx:</span>
	<span data-ty> {</span>
	<span data-ty>    "args": {</span>
	<span data-ty>        "dest": {</span>
	<span data-ty>            "V3": {</span>
	<span data-ty>                "parents": "0",</span>
	<span data-ty>                "interior": {</span>
	<span data-ty>                    "X1": {</span>
	<span data-ty>                        "Parachain": "1,000"</span>
	<span data-ty>                    }</span>
	<span data-ty>                }</span>
	<span data-ty>            }</span>
	<span data-ty>        },</span>
	<span data-ty>        "beneficiary": {</span>
	<span data-ty>            "V3": {</span>
	<span data-ty>                "parents": "0",</span>
	<span data-ty>                "interior": {</span>
	<span data-ty>                    "X1": {</span>
	<span data-ty>                        "AccountId32": {</span>
	<span data-ty>                            "network": null,</span>
	<span data-ty>                            "id": "0x6c0c32faf970eacb2d4d8e538ac0dab3642492561a1be6f241c645876c056c1d"</span>
	<span data-ty>                        }</span>
	<span data-ty>                    }</span>
	<span data-ty>                }</span>
	<span data-ty>            }</span>
	<span data-ty>        },</span>
	<span data-ty>        "assets": {</span>
	<span data-ty>            "V3": [</span>
	<span data-ty>                {</span>
	<span data-ty>                    "id": {</span>
	<span data-ty>                        "Concrete": {</span>
	<span data-ty>                            "parents": "0",</span>
	<span data-ty>                            "interior": "Here"</span>
	<span data-ty>                        }</span>
	<span data-ty>                    },</span>
	<span data-ty>                    "fun": {</span>
	<span data-ty>                        "Fungible": "1,000,000,000,000"</span>
	<span data-ty>                    }</span>
	<span data-ty>                }</span>
	<span data-ty>            ]</span>
	<span data-ty>        },</span>
	<span data-ty>        "fee_asset_item": "0",</span>
	<span data-ty>        "weight_limit": "Unlimited"</span>
	<span data-ty>    },</span>
	<span data-ty>    "method": "transferAssets",</span>
	<span data-ty>    "section": "xcmPallet"</span>
	<span data-ty>}</span>
</div>

### Local Parachain Transfer

The following example demonstrates a local transfer using the `balances` pallet on a parachain.

```javascript
import {
  AssetTransferApi,
  constructApiPromise,
} from "@substrate/asset-transfer-api";

async function main() {
  const { api, specName, safeXcmVersion } = await constructApiPromise(
    "wss://wss.api.moonbeam.network"
  );
  const assetApi = new AssetTransferApi(api, specName, safeXcmVersion);

  let callInfo;
  try {
    callInfo = await assetApi.createTransferTransaction(
      "2004",
      "0xF977814e90dA44bFA03b6295A0616a897441aceC",
      [],
      ["100000"],
      {
        format: "call",
        keepAlive: true,
      }
    );

    console.log(`Call data:\n${JSON.stringify(callInfo, null, 4)}`);
  } catch (e) {
    console.error(e);
    throw Error(e as string);
  }

  const decoded = assetApi.decodeExtrinsic(callInfo.tx, "call");
  console.log(
    `\nDecoded tx:\n ${JSON.stringify(JSON.parse(decoded), null, 4)}`
  );
}

main()
  .catch((err) => console.error(err))
  .finally(() => process.exit());
```
<div id="termynal" data-termynal>
    <span data-ty="input"><span class="file-path"></span>ts-node localParachainTx.ts</span>
    <br>
	<span data-ty>Call data:</span>
	<span data-ty>{</span>
	<span data-ty>    "origin": "moonbeam",</span>
	<span data-ty>    "dest": "moonbeam",</span>
	<span data-ty>    "direction": "local",</span>
	<span data-ty>    "xcmVersion": null,</span>
	<span data-ty>    "method": "balances::transferKeepAlive",</span>
	<span data-ty>    "format": "call",</span>
	<span data-ty>    "tx": "0x0a03f977814e90da44bfa03b6295a0616a897441acec821a0600"</span>
	<span data-ty>}</span>
	<span data-ty></span>
	<span data-ty>Decoded tx:</span>
	<span data-ty> {</span>
	<span data-ty>    "args": {</span>
	<span data-ty>        "dest": "0xF977814e90dA44bFA03b6295A0616a897441aceC",</span>
	<span data-ty>        "value": "100,000"</span>
	<span data-ty>    },</span>
	<span data-ty>    "method": "transferKeepAlive",</span>
	<span data-ty>    "section": "balances"</span>
	<span data-ty>}</span>
</div>

