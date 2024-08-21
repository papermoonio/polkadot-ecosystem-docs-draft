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

        ```ts
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

        `SystemToSystem`

        System parachain to System parachain chain.

        ---

        `SystemToBridge`

        System parachain to an external `GlobalConsensus` chain.
        
        ---

        `ParaToPara`

        Parachain to Parachain.

        ---

        `ParaToRelay`

        Parachain to Relay chain.

        ---
        
        `ParaToSystem`

        Parachain to System parachain.

        ---

        `RelayToSystem`

        Relay to System Parachain.

        ---

        `RelayToPara`

        Relay chain to Parachain.

        ---

        `RelayToBridge`

        Relay chain to an external `GlobalConsensus` chain.

    `method` ++"Methods"++

    The method used in the transaction.

    ??? child "Type `Methods`"

        ```ts
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

            ```ts
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

        - Payload format - if the format field is set to `'payload'`, the `ConstructedFormat` type will return a [`GenericExtrinsicPayload`](https://github.com/polkadot-js/api/blob/3b7b44f048ff515579dd233ea6964acec39c0589/packages/types/src/extrinsic/ExtrinsicPayload.ts#L48){target=\_blank}
        - Call format - if the format field is set to `'call'`, the `ConstructedFormat` type will return a hexadecimal string (`0x${string}`). This is the encoded representation of the extrinsic call
        - Submittable format - if the format field is set to `'submittable'`, the `ConstructedFormat` type will return a [`SubmittableExtrinsic`](https://github.com/polkadot-js/api/blob/3b7b44f048ff515579dd233ea6964acec39c0589/packages/api-base/src/types/submittable.ts#L56){target=\_blank}. This is a Polkadot.js type that represents a transaction that can be submitted to the blockchain