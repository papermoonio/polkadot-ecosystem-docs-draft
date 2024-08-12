---
title: Asset Transfer API
description: Asset Transfer API is a library that simplifies the transfer of assets for Substrate based chains. It provides methods for cross-chain and local transfers.
---

# Asset Transfer API

[Asset Transfer API](https://github.com/paritytech/asset-transfer-api){target=_blank}, a tool developed and maintained by [Parity](https://www.parity.io/){target=_blank}, is a specialized library designed to streamline asset transfers for Substrate-based blockchains.

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

### Claim Assets: Option 1

Create an XCM transaction to retrieve trapped assets. This can be either locally on a systems parachain, on the relay chain, or any chain that supports the pallet-xcm `claimAssets` runtime call.

---

#### Parameters

`assetIds` ++"string[]"++ <span class="required" markdown>++"required"++</span>

An array of `assetId`'s to be claimed from the asset trap.

---

`amounts` ++"string[]"++ <span class="required" markdown>++"required"++</span>

An array of the amounts of each trapped asset to be claimed.

---

`beneficiary` ++"string"++ <span class="required" markdown>++"required"++</span>

Address of the account to receive the trapped assets.

---

`opts` ++"TransferArgsOpts<T>"++

Options for customizing the claim assets transaction. These options allow you to specify the transaction format, fee payment details, weight limits, XCM versions, and more.

??? child "Show more"

    `format` ++"T extends Format"++ 
        
    Specifies the format for returning a transaction

    ??? child "Type `Format`"

        ```javascript
        export type Format = 'payload' | 'call' | 'submittable';
        ```
    
    ---

    `paysWithFeeOrigin` ++"string"++
    
    The Asset ID to pay fees on the current common good parachain. The defaults are as follows:

      - Polkadot AssetHub - DOT
      - Kusama AssetHub - KSM

    ---

    `paysWithFeeDest` ++"string"++
    
    Asset ID to pay fees on the destination parachain.

    ---

    `weightLimit` ++"{ refTime?: string, proofSize?: string }"++
    
    Custom weight limit option. If not provided, it will default to unlimited

    ---

    `xcmVersion` ++"number"++
    
    Sets the XCM version for message construction. If this is not present a supported version will be queried, and if there is no supported version a safe version will be queried

    ---

    `keepAlive` ++"boolean"++
    
    Enables `transferKeepAlive` for local asset transfers. For creating local asset transfers, if true this will allow for a `transferKeepAlive` as opposed to a `transfer`

    ---

    `transferLiquidToken` ++"boolean"++
    
    Declares if this will transfer liquidity tokens. Default is false

    ---

    `assetTransferType` ++"string"++
    
    The XCM transfer type used to transfer assets. The `AssetTransferType` type defines the possible values for this parameter.

    ??? child "Type `AssetTransferType`"

        ```javascript
        export type AssetTransferType = LocalReserve | DestinationReserve | Teleport | RemoteReserve;
        ```

        !!! note
            To use the `assetTransferType` parameter, which is a string, you should use the `AssetTransferType` type as if each of its variants are strings. For example: `assetTransferType = 'LocalReserve'`.

    ---

    `remoteReserveAssetTransferTypeLocation` ++"string"++
    
    The remove reserve location for the XCM transfer. Should be provided when specifying an `assetTransferType` of `RemoteReserve`.

    ---

    `feesTransferType` ++"string"++
    
    XCM TransferType used to pay fees for XCM transfer. The `AssetTransferType` type defines the possible values for this parameter.

    ??? child "Type `AssetTransferType`"

        ```javascript
        export type AssetTransferType = LocalReserve | DestinationReserve | Teleport | RemoteReserve;
        ```

        !!! note
            To use the `feesTransferType` parameter, which is a string, you should use the `AssetTransferType` type as if each of its variants are strings. For example: `feesTransferType = 'LocalReserve'`.

    ---

    `remoteReserveFeesTransferTypeLocation` ++"string"++
    
    The remote reserve location for the XCM transfer fees. Should be provided when specifying a `feesTransferType` of `RemoteReserve`.

    ---

    `customXcmOnDest` ++"string"++
    
    A custom XCM message to be executed on the destination chain. Should be provided if a custom XCM message is needed after transferring assets. Defaults to:

    ```bash
    Xcm(vec![DepositAsset { assets: Wild(AllCounted(assets.len())), beneficiary }])
    ```

---

#### Returns

++"Promise<TxResult<T>"++

A promise containing the result of constructing the transaction.

??? child "Show more"

    `dest` ++"string"++

    The destination `specName` of the transaction.

    ---

    `origin` ++"string"++

    The origin `specName` of the transaction.

    ---

    `format` ++"Format | 'local'"++

    The format type the transaction is outputted in.

    ??? child "Type `Format`"

        ```js
        type Format = 'payload' | 'call' | 'submittable';
        ```

    ---

    `xcmVersion` ++"number | null"++

    The XCM version that was used to construct the transaction.

    ---

    `direction` ++"Direction | 'local'"++

    The direction of the cross-chain transfer.

    ??? child "Enum `Direction` values"

        `Local`

        Local transaction.

        ---

        `SystemToPara`

        System parachain to parachain.

        ---

        `SystemToRelay`

        System paracahin to system relay chain.

        ---

        ...     

    ---

    `method` ++"Methods"++

    The method used in the transaction.

    ??? child "Type `Methods`"

        ```js
        type Methods =
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

        ??? child "Type `LocalTransferTypes`"

            ```js
            type LocalTransferTypes =
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

    ---

    `tx` ++"ConstructedFormat<T>"++

    The constructed transaction.

    ??? child "Type `ConstructedFormat<T>`"

        ...

---

#### Example

```js
import { TxResult } from '@substrate/asset-transfer-api';

let callInfo: TxResult<'call'>;
try {
  callInfo = await assetsApi.claimAssets(
    [
      `{"parents":"0","interior":{"X2":[{"PalletInstance":"50"},{"GeneralIndex":"1984"}]}}`,
    ],
    ['1000000000000'],
    '0xf5d5714c084c112843aca74f8c498da06cc5a2d63153b825189baa51043b1f0b',
    {
      format: 'call',
      xcmVersion: 2,
    }
  );
} catch (e) {
  console.error(e);
  throw Error(e);
}
```

---

### Claim Assets: Option 2

Create an XCM transaction to retrieve trapped assets. This can be either locally on a systems parachain, on the relay chain, or any chain that supports the pallet-xcm `claimAssets` runtime call.

??? interface "Request parameters"

    `assetIds` ++"string[]"++ <span class="required" markdown>++"required"++</span>

    An array of `assetId`'s to be claimed from the asset trap.

    ---

    `amounts` ++"string[]"++ <span class="required" markdown>++"required"++</span>

    An array of the amounts of each trapped asset to be claimed.

    ---

    `beneficiary` ++"string"++ <span class="required" markdown>++"required"++</span>

    Address of the account to receive the trapped assets.

    ---

    `opts` ++"TransferArgsOpts<T>"++

    Options for customizing the claim assets transaction. These options allow you to specify the transaction format, fee payment details, weight limits, XCM versions, and more.

    ??? child "Show more"

        `format` ++"T extends Format"++ 
            
        Specifies the format for returning a transaction

        ??? child "Type `Format`"

            ```javascript
            export type Format = 'payload' | 'call' | 'submittable';
            ```
        
        ---

        `paysWithFeeOrigin` ++"string"++
        
        The Asset ID to pay fees on the current common good parachain. The defaults are as follows:

          - Polkadot AssetHub - DOT
          - Kusama AssetHub - KSM

        ---

        `paysWithFeeDest` ++"string"++
        
        Asset ID to pay fees on the destination parachain.

        ---

        `weightLimit` ++"{ refTime?: string, proofSize?: string }"++
        
        Custom weight limit option. If not provided, it will default to unlimited

        ---

        `xcmVersion` ++"number"++
        
        Sets the XCM version for message construction. If this is not present a supported version will be queried, and if there is no supported version a safe version will be queried

        ---

        `keepAlive` ++"boolean"++
        
        Enables `transferKeepAlive` for local asset transfers. For creating local asset transfers, if true this will allow for a `transferKeepAlive` as opposed to a `transfer`

        ---

        `transferLiquidToken` ++"boolean"++
        
        Declares if this will transfer liquidity tokens. Default is false

        ---

        `assetTransferType` ++"string"++
        
        The XCM transfer type used to transfer assets. The `AssetTransferType` type defines the possible values for this parameter.

        ??? child "Type `AssetTransferType`"

            ```javascript
            export type AssetTransferType = LocalReserve | DestinationReserve | Teleport | RemoteReserve;
            ```

            !!! note
                To use the `assetTransferType` parameter, which is a string, you should use the `AssetTransferType` type as if each of its variants are strings. For example: `assetTransferType = 'LocalReserve'`.

        ---

        `remoteReserveAssetTransferTypeLocation` ++"string"++
        
        The remove reserve location for the XCM transfer. Should be provided when specifying an `assetTransferType` of `RemoteReserve`.

        ---

        `feesTransferType` ++"string"++
        
        XCM TransferType used to pay fees for XCM transfer. The `AssetTransferType` type defines the possible values for this parameter.

        ??? child "Type `AssetTransferType`"

            ```javascript
            export type AssetTransferType = LocalReserve | DestinationReserve | Teleport | RemoteReserve;
            ```

            !!! note
                To use the `feesTransferType` parameter, which is a string, you should use the `AssetTransferType` type as if each of its variants are strings. For example: `feesTransferType = 'LocalReserve'`.

        ---

        `remoteReserveFeesTransferTypeLocation` ++"string"++
        
        The remote reserve location for the XCM transfer fees. Should be provided when specifying a `feesTransferType` of `RemoteReserve`.

        ---

        `customXcmOnDest` ++"string"++
        
        A custom XCM message to be executed on the destination chain. Should be provided if a custom XCM message is needed after transferring assets. Defaults to:

        ```bash
        Xcm(vec![DepositAsset { assets: Wild(AllCounted(assets.len())), beneficiary }])
        ```

??? interface "Response parameters"

    ++"Promise<TxResult<T>"++

    A promise containing the result of constructing the transaction.

    ??? child "Show more"

        `dest` ++"string"++

        The destination `specName` of the transaction.

        ---

        `origin` ++"string"++

        The origin `specName` of the transaction.

        ---

        `format` ++"Format | 'local'"++

        The format type the transaction is outputted in.

        ??? child "Type `Format`"

            ```js
            type Format = 'payload' | 'call' | 'submittable';
            ```

        ---

        `xcmVersion` ++"number | null"++

        The XCM version that was used to construct the transaction.

        ---

        `direction` ++"Direction | 'local'"++

        The direction of the cross-chain transfer.

        ??? child "Enum `Direction` values"

            `Local`

            Local transaction.

            ---

            `SystemToPara`

            System parachain to parachain.

            ---

            `SystemToRelay`

            System paracahin to system relay chain.

            ---

            ...     

        ---

        `method` ++"Methods"++

        The method used in the transaction.

        ??? child "Type `Methods`"

            ```js
            type Methods =
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

            ??? child "Type `LocalTransferTypes`"

                ```js
                type LocalTransferTypes =
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

        ---

        `tx` ++"ConstructedFormat<T>"++

        The constructed transaction.

        ??? child "Type `ConstructedFormat<T>`"

            ...

???+ interface "Example request"

    ```js
    import { TxResult } from '@substrate/asset-transfer-api';

    let callInfo: TxResult<'call'>;
    try {
      callInfo = await assetsApi.claimAssets(
        [
          `{"parents":"0","interior":{"X2":[{"PalletInstance":"50"},{"GeneralIndex":"1984"}]}}`,
        ],
        ['1000000000000'],
        '0xf5d5714c084c112843aca74f8c498da06cc5a2d63153b825189baa51043b1f0b',
        {
          format: 'call',
          xcmVersion: 2,
        }
      );
    } catch (e) {
      console.error(e);
      throw Error(e);
    }
    ```

???+ interface "Example response"

    ```js
    insert example response?
    ```

---

---

### Claim Assets: Option 3

Create an XCM transaction to retrieve trapped assets. This can be either locally on a systems parachain, on the relay chain, or any chain that supports the pallet-xcm `claimAssets` runtime call.

??? interface "Request parameters"

    `assetIds` ++"string[]"++ <span class="required" markdown>++"required"++</span>

    An array of `assetId`'s to be claimed from the asset trap.

    ---

    `amounts` ++"string[]"++ <span class="required" markdown>++"required"++</span>

    An array of the amounts of each trapped asset to be claimed.

    ---

    `beneficiary` ++"string"++ <span class="required" markdown>++"required"++</span>

    Address of the account to receive the trapped assets.

    ---

    `opts` ++"TransferArgsOpts<T>"++

    Options for customizing the claim assets transaction. These options allow you to specify the transaction format, fee payment details, weight limits, XCM versions, and more.

    ??? child "Show more"

        `format` ++"T extends Format"++ 
            
        Specifies the format for returning a transaction

        ??? child "Type `Format`"

            ```javascript
            export type Format = 'payload' | 'call' | 'submittable';
            ```
        
        ---

        `paysWithFeeOrigin` ++"string"++
        
        The Asset ID to pay fees on the current common good parachain. The defaults are as follows:

          - Polkadot AssetHub - DOT
          - Kusama AssetHub - KSM

        ---

        `paysWithFeeDest` ++"string"++
        
        Asset ID to pay fees on the destination parachain.

        ---

        `weightLimit` ++"{ refTime?: string, proofSize?: string }"++
        
        Custom weight limit option. If not provided, it will default to unlimited

        ---

        `xcmVersion` ++"number"++
        
        Sets the XCM version for message construction. If this is not present a supported version will be queried, and if there is no supported version a safe version will be queried

        ---

        `keepAlive` ++"boolean"++
        
        Enables `transferKeepAlive` for local asset transfers. For creating local asset transfers, if true this will allow for a `transferKeepAlive` as opposed to a `transfer`

        ---

        `transferLiquidToken` ++"boolean"++
        
        Declares if this will transfer liquidity tokens. Default is false

        ---

        `assetTransferType` ++"string"++
        
        The XCM transfer type used to transfer assets. The `AssetTransferType` type defines the possible values for this parameter.

        ??? child "Type `AssetTransferType`"

            ```javascript
            export type AssetTransferType = LocalReserve | DestinationReserve | Teleport | RemoteReserve;
            ```

            !!! note
                To use the `assetTransferType` parameter, which is a string, you should use the `AssetTransferType` type as if each of its variants are strings. For example: `assetTransferType = 'LocalReserve'`.

        ---

        `remoteReserveAssetTransferTypeLocation` ++"string"++
        
        The remove reserve location for the XCM transfer. Should be provided when specifying an `assetTransferType` of `RemoteReserve`.

        ---

        `feesTransferType` ++"string"++
        
        XCM TransferType used to pay fees for XCM transfer. The `AssetTransferType` type defines the possible values for this parameter.

        ??? child "Type `AssetTransferType`"

            ```javascript
            export type AssetTransferType = LocalReserve | DestinationReserve | Teleport | RemoteReserve;
            ```

            !!! note
                To use the `feesTransferType` parameter, which is a string, you should use the `AssetTransferType` type as if each of its variants are strings. For example: `feesTransferType = 'LocalReserve'`.

        ---

        `remoteReserveFeesTransferTypeLocation` ++"string"++
        
        The remote reserve location for the XCM transfer fees. Should be provided when specifying a `feesTransferType` of `RemoteReserve`.

        ---

        `customXcmOnDest` ++"string"++
        
        A custom XCM message to be executed on the destination chain. Should be provided if a custom XCM message is needed after transferring assets. Defaults to:

        ```bash
        Xcm(vec![DepositAsset { assets: Wild(AllCounted(assets.len())), beneficiary }])
        ```

??? interface "Response parameters"

    ++"Promise<TxResult<T>"++

    A promise containing the result of constructing the transaction.

    ??? child "Show more"

        `dest` ++"string"++

        The destination `specName` of the transaction.

        ---

        `origin` ++"string"++

        The origin `specName` of the transaction.

        ---

        `format` ++"Format | 'local'"++

        The format type the transaction is outputted in.

        ??? child "Type `Format`"

            ```js
            type Format = 'payload' | 'call' | 'submittable';
            ```

        ---

        `xcmVersion` ++"number | null"++

        The XCM version that was used to construct the transaction.

        ---

        `direction` ++"Direction | 'local'"++

        The direction of the cross-chain transfer.

        ??? child "Enum `Direction` values"

            `Local`

            Local transaction.

            ---

            `SystemToPara`

            System parachain to parachain.

            ---

            `SystemToRelay`

            System paracahin to system relay chain.

            ---

            ...     

        ---

        `method` ++"Methods"++

        The method used in the transaction.

        ??? child "Type `Methods`"

            ```js
            type Methods =
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

            ??? child "Type `LocalTransferTypes`"

                ```js
                type LocalTransferTypes =
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

        ---

        `tx` ++"ConstructedFormat<T>"++

        The constructed transaction.

        ??? child "Type `ConstructedFormat<T>`"

            ...

???+ interface "Example"

    === "Request"

        ```js
        import { TxResult } from '@substrate/asset-transfer-api';

        let callInfo: TxResult<'call'>;
        try {
          callInfo = await assetsApi.claimAssets(
            [
              `{"parents":"0","interior":{"X2":[{"PalletInstance":"50"},{"GeneralIndex":"1984"}]}}`,
            ],
            ['1000000000000'],
            '0xf5d5714c084c112843aca74f8c498da06cc5a2d63153b825189baa51043b1f0b',
            {
              format: 'call',
              xcmVersion: 2,
            }
          );
        } catch (e) {
          console.error(e);
          throw Error(e);
        }
        ```

    === "Response"

        ```js
        insert example response?
        ```

---


### Create Transfer Transaction

`createTransferTransaction`

### Decode Extrinsic

`decodeExtrinsic`

### Fetch Fee Information

`fetchFeeInfo`

### Initialize Registry

`initializeRegistry`

## Construct Polkadot.js ApiPromise

For a simpler setup process, you can leverage the `constructApiPromise` helper function provided by the library. It constructs a Polkadot.js ApiPromise, retrieves the connected chain's name, and fetches a safe XCM version. You can use this function to reduce boilerplate code and potential configuration errors.

**Parameters**
<a class="headerlink" href="#parameters" aria-describedby="__tooltip2_1" markdown>:material-link-variant:</a>

<div class="api-reference-link" markdown>:material-link-variant:</div>

`wsUrl` ++"string"++ <span class="required" markdown>++"required"++</span>

The WebSocket URL of the chain to connect to.

---

<div class="api-reference-link" markdown>:material-link-variant:</div>

`opts` ++"ApiOptions"++

A configuration object that allows developers to customize how the ApiPromise connects to and interacts with a blockchain node.

??? child "Show attributes"

    `derives` ++"DeriveCustom"++

    Add custom derives to be injected. These custom derivations allow developers to extend the API with additional methods that can be used to derive data from the blockchain.

    ??? child "Show more"

        `DerviceCustom` is a type used to define custom derivation functions that extend the Polkadot.js API.

        ```ts
        type DeriveCreator = (
          instanceId: string,
          api: unknown
        ) => (...args: unknown[]) => Observable<any>;

        export type DeriveCustom = Record<string, Record<string, DeriveCreator>>;
        ```

        ---

        **Attributes**

        ++"string"++

        A key representing the name of the module to which the custom derivation functions belong.
    
        ++"string"++

        A key representing the name of the custom derivation method within the module.

        ++"DeriveCreator"++

        A function that generates a derivation method. It receives `instanceId` and `api` as parameters and returns a function that takes additional arguments and returns an `Observable`.

        ---
    
    ---

    `initWasm` ++"boolean"++

    Control the initialization of the Wasm libraries. When not specified, it defaults to `true`, initializing the Wasm libraries, set to `false` to not initialize Wasm (no sr25519 support).

    ---

    `isPedanctic` ++"boolean"++

    Controls the checking of storage values once they have been constructed. When not specified this defaults to `true`. Set to `false` to forgo any checking on storage results.

    ---

    `metadata` ++"Record<string, HexString>"++

    Pre-bundles is a map of genesis hash and runtime spec version as key to a metadata hex string. If the genesis hash and runtime spec version match, then use metadata, else fetch it from the chain.

    ---

    `noInitWarn` ++"boolean"++

    Don't display any warnings on initialization (missing RPC methods and runtime calls).

    ---

---

**Returns**

<div class="api-reference-link" markdown>:material-link-variant:</div>

++"Promise<object>"++

An object containing the Polkadot.js `ApiPromise` and configuration required to instantiate the `AssetTransferApi` class.

??? child "Show attributes"

    `api` ++"ApiPromise"++

    A Polkadot.js ApiPromise.

    ---

    `specName` ++"string"++

    The name of the runtime specification of the blockchain to which the API is connected.

    ---

    `chainName` ++"string"++

    The human-readable name of the blockchain to which the API is connected.

    ---

    `safeXcmVersion` ++"number"++

    The safe version of the XCM format that can be used when interacting with the blockchain to which the API is connected.

---

**Example**

```javascript
import { constructApiPromise } from '@substrate/asset-transfer-api';

async function main() {
  const { 
    api,
    specName,
    chainName,
    safeXcmVersion 
  } = await constructApiPromise('INSERT_WEBSOCKET_URL');
}

main();
```

## 