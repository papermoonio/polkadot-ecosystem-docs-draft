---
title: Asset Transfer API Reference
description: Explore the Asset Transfer API Reference for comprehensive details on methods, data types, and functionalities. Essential for cross-chain asset transfers.
---

# Asset Transfer API Reference

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

Holds open an API connection to a specified chain within the `ApiPromise` to help construct transactions for assets and estimate fees.

For a more in-depth explanation of the Asset Transfer API class structure, check the [source code](https://github.com/paritytech/asset-transfer-api/blob/f2aa50db83882f23492f975221dd5501c35a26d5/src/AssetTransferApi.ts#L106){target=_blank}.

### Methods

#### Create Transfer Transaction

Generates an XCM transaction for transferring assets between chains. It simplifies the process by inferring what type of transaction is required given the inputs, ensuring that the assets are valid, and that the transaction details are correctly formatted.

After obtaining the transaction, you must handle the signing and submission process separately.

```ts
--8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ctt-fn-signature.ts'
```

??? interface "Request parameters"

    `destChainId` ++"string"++ <span class="required" markdown>++"required"++</span>
    
    ID of the destination chain (`'0'` for relay chain, other values for parachains).

    ---

    `destAddr` ++"string"++ <span class="required" markdown>++"required"++</span>

    Address of the recipient account on the destination chain.

    ---

    `assetIds` ++"string[]"++ <span class="required" markdown>++"required"++</span>

    Array of asset IDs to be transferred.

    When asset IDs are provided, the API dynamically selects the appropriate pallet for the current chain to handle these specific assets. If the array is empty, the API defaults to using the `balances` pallet.

    ---

    `amounts` ++"string[]"++ <span class="required" markdown>++"required"++</span>

    Array of amounts corresponding to each asset in `assetIds`.

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

#### Claim Assets

Creates a local XCM transaction to retrieve trapped assets. This function can be used to claim assets either locally on a system parachain, on the relay chain, or on any chain that supports the `claimAssets` runtime call.


```ts
--8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ca-fn-signature.ts'
```

??? interface "Request parameters"

    `assetIds` ++"string[]"++ <span class="required" markdown>++"required"++</span>

    Array of asset IDs to be claimed from the `AssetTrap`.

    ---

    `amounts` ++"string[]"++ <span class="required" markdown>++"required"++</span>

    Array of amounts corresponding to each asset in `assetIds`.

    ---

    `beneficiary` ++"string"++ <span class="required" markdown>++"required"++</span>

    Address of the account to receive the trapped assets.

    ---

    `opts` ++"TransferArgsOpts<T>"++

    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/transfer-arg-opts.md'

??? interface "Response parameters"

    ++"Promise<TxResult<T>>"++

    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/tx-result.md'

??? interface "Example"

    ***Request***

    ```ts
    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ca-example-request.ts'
    ```

    ***Response***

    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ca-example-response.md'


#### Decode Extrinsic

Decodes the hex of an extrinsic into a string readable format.

```ts
--8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/de-fn-signature.ts'
```

??? interface "Request parameters"

    `encodedTransaction` ++"string"++ <span class="required" markdown>++"required"++</span>

    A hex encoded extrinsic.

    ---

    `format` ++"T extends Format"++ <span class="required" markdown>++"required"++</span>
    
    Specifies the format for returning a transaction.

    ??? child "Type `Format`"

        ```ts
        export type Format = 'payload' | 'call' | 'submittable';
        ```

??? interface "Response parameters"

    ++"string"++

    Decoded extrinsic in string readable format.

??? interface "Example"

    ***Request***

    ```ts
    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/de-example-request.ts'
    ```

    ***Response***

    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/de-example-response.md'

#### Fetch Fee Info

Fetch estimated fee information for an extrinsic.

```ts
--8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ffi-fn-signature.ts'
```

??? interface "Request parameters"

    `tx` ++"ConstructedFormat<T>"++ <span class="required" markdown>++"required"++</span>

    The constructed transaction.

    ??? child "Type `ConstructedFormat<T>`"

        ```ts
        export type ConstructedFormat<T> = T extends 'payload'
        ? GenericExtrinsicPayload
        : T extends 'call'
        ? `0x${string}`
        : T extends 'submittable'
          ? SubmittableExtrinsic<'promise', ISubmittableResult>
          : never;
        ```

        The `ConstructedFormat` type is a conditional type that returns a specific type based on the value of the TxResult `format` field.

        - Payload Format - if the format field is set to 'payload', the ConstructedFormat type will return a [GenericExtrinsicPayload](https://github.com/polkadot-js/api/blob/3b7b44f048ff515579dd233ea6964acec39c0589/packages/types/src/extrinsic/ExtrinsicPayload.ts#L48){target=_blank}
        - Call Format - if the format field is set to 'call', the `ConstructedFormat` type will return a hexadecimal string (`0x${string}`). This is the encoded representation of the extrinsic call
        - Submittable Format - if the format field is set to `'submittable'`, the `ConstructedFormat` type will return a [`SubmittableExtrinsic`](https://github.com/polkadot-js/api/blob/3b7b44f048ff515579dd233ea6964acec39c0589/packages/api-base/src/types/submittable.ts#L56){target=_blank}. This is a Polkadot.js type that represents a transaction that can be submitted to the blockchain

    ---

    `format` ++"T extends Format"++ <span class="required" markdown>++"required"++</span>

    Specifies the format for returning a transaction.

    ??? child "Type `Format`"

        ```ts
        export type Format = 'payload' | 'call' | 'submittable';
        ```

??? interface "Response parameters"

    ++"Promise<RuntimeDispatchInfo | RuntimeDispatchInfoV1 | null>"++

    A promise containing the estimated fee information for the provided extrinsic.

    ??? child "Type `RuntimeDispatchInfo`"

        ```ts
        export interface RuntimeDispatchInfo extends Struct {
          readonly weight: Weight;
          readonly class: DispatchClass;
          readonly partialFee: Balance;
        }
        ```

        For more information on the underlying types and fields of `RuntimeDispatchInfo`, check the [RuntimeDispatchInfo](https://github.com/polkadot-js/api/blob/2329af239eaf194696daeaa58ebf89f0080a5e0d/packages/types/src/interfaces/payment/types.ts#L21){target=_blank} source code.


    ??? child "Type `RuntimeDispatchInfoV1`"

        ```ts
        export interface RuntimeDispatchInfoV1 extends Struct {
          readonly weight: WeightV1;
          readonly class: DispatchClass;
          readonly partialFee: Balance;
        }
        ```

        For more information on the underlying types and fields of `RuntimeDispatchInfoV1`, check the [RuntimeDispatchInfoV1](https://github.com/polkadot-js/api/blob/2329af239eaf194696daeaa58ebf89f0080a5e0d/packages/types/src/interfaces/payment/types.ts#L28){target=_blank} source code.

??? interface "Example"

    ***Request***

    ```ts
    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ffi-example-request.ts'
    ```

    ***Response***

    --8<-- 'code/build-on-polkadot/xcm/asset-transfer-api/reference/ffi-example-response.md'