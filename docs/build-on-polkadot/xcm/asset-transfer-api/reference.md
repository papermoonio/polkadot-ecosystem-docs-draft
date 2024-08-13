---
title: Asset Transfer API Reference
description: Explore the Asset Transfer API Reference for comprehensive details on methods, data types, and functionalities. Essential for cross-chain asset transfers.
---

# Asset Transfer API Reference 
# ( 🚧 WIP )

<br>
<div class="grid cards" markdown>
-   :octicons-download-16:{ .lg .middle } __Install the Asset Transfer API__

    ---

    Learn how to install [`asset-transfer-api`](#) into a new or existing project.

    <br>
    [:octicons-arrow-right-24: Get started](#)

-   :octicons-code-16:{ .lg .middle } __Dive in with a tutorial__

    ---

    Ready to start coding? Follow along with a step-by-step tutorial.

    <br>
    [:octicons-arrow-right-24: How to use the Asset Transfer API](#)
</div>
<br>


## Asset Transfer API Class

Holds open an API connection to a specified chain within the ApiPromise in order to help construct transactions for assets and estimate fees.

### Methods

#### createTransferTransaction

This function allows you to create XCM transactions to transfer assets or native tokens between different chains.

It takes several parameters to specify the transfer details, including the destination chain, recipient address, assets to be transferred, and their amounts, as well as an optional parameter for further customization. It can infer what kind of transaction is necessary given the inputs. When sending cross-chain transfers, the API performs extensive validation to ensure the inputs are valid and the assets either exist or don't.

!!! note
	The `createTransferTransaction` function is designed to be a utility that simplifies the creation of the transaction. It does not sign or submit the created transaction on the blockchain. It simply generates the transaction in the requested format (e.g., payload, call, or submittable). After obtaining the transaction from the `createTransferTransaction` function, you will need to handle the signing and submission process separately.

```ts
public async createTransferTransaction<T extends Format>(
  destChainId: string,
  destAddr: string,
  assetIds: string[],
  amounts: string[],
  opts: TransferArgsOpts<T> = {},
): Promise<TxResult<T>>
```

??? interface "Request parameters"

	`destChainId` ++"string"++ <span class="required" markdown>++"required"++</span>
	
	ID of the destination chain ('0' for Relay chain, other values for parachains)

	---

	`destAddr` ++"string"++ <span class="required" markdown>++"required"++</span>

	Address of the recipient account on the destination chain

	---

	`assetIds` ++"string[]"++ <span class="required" markdown>++"required"++</span>

	Array of asset IDs to be transferred
      
    If a token or asset ID is provided as input, the API will resolve to using the `tokens` pallet. When no asset is passed in, the API will default to using the `balances` pallet.

	---

	`amounts` ++"string[]"++ <span class="required" markdown>++"required"++</span>

	Array of amounts corresponding to each asset in `assetIds`

	---

	`opts` ++"TransferArgsOpts<T>"++

    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/transfer-arg-opts.md'

??? interface "Response parameters"

    ++"Promise<TxResult<T>"++

    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/tx-result.md'

??? interface "Example"

	***Request***

	```ts
	--8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ctt-example-request.ts'
	```

	***Response***

	--8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ctt-example-response.md'

#### claimAssets

Creates a local XCM transaction to retrieve trapped assets. This function can be used to claim assets either locally on a system parachain, on the relay chain, or on any chain that supports the pallet-xcm `claimAssets` runtime call.


```ts
public async claimAssets<T extends Format>(
	assetIds: string[],
	amounts: string[],
	beneficiary: string,
	opts: TransferArgsOpts<T>,
): Promise<TxResult<T>>
```

??? interface "Request parameters"

	`assetIds` ++"string[]"++ <span class="required" markdown>++"required"++</span>

	Array of asset IDs to be claimed from the AssetTrap

	---

	`amounts` ++"string[]"++ <span class="required" markdown>++"required"++</span>

	Array of amounts corresponding to each asset in `assetIds`

	---

	`beneficiary` ++"string"++ <span class="required" markdown>++"required"++</span>

	Address of the account to receive the trapped assets

	---

	`opts` ++"TransferArgsOpts<T>"++

    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/transfer-arg-opts.md'

??? interface "Response parameters"

    ++"Promise<TxResult<T>"++

    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/tx-result.md'

???+ interface "Example"

	***Request***

	```ts
	--8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ca-example-request.ts'
	```

	***Response***

	--8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ca-example-response.md'


#### fetchFeeInfo

#### decodeExtrinsic

#### initializeRegistry