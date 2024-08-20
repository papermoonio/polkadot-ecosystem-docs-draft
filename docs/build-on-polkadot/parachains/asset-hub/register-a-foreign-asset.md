---
title: Register a foreign asset
description: An in-depth guide to registering a foreign asset on the Asset Hub parachain, providing clear, step-by-step instructions.
---

# Register a foreign asset on Asset Hub

## Introduction

As outlined in the [Asset Hub Overview](./overview.md#foreign-assets){target=_blank}, Asset Hub supports two categories of assets: local and foreign. Foreign assets originated outside of Asset Hub and are recognized by [`Multilocations`](https://wiki.polkadot.network/docs/learn/xcm/fundamentals/multilocation-summary){target=_blank}. This guide will walk you through the process of registering a foreign asset on the Asset Hub parachain.

To register a foreign asset on Asset Hub, it's essential to notice that the process involves communication between two parachains. Asset Hub parachain will be the destination of the foreign asset, while the source parachain will be the origin of the asset. The communication between the two parachains is facilitated by the [Cross-Chain Message Passing (XCMP)](https://wiki.polkadot.network/docs/learn-xcm){target=_blank} protocol.

## Prerequisites

The Asset Hub parachain is one of the system parachains on a relay chain, such as [Polkadot](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fpolkadot.api.onfinality.io%2Fpublic-ws#/explorer){target=\_blank} or [Kusama](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fkusama.api.onfinality.io%2Fpublic-ws#/explorer){target=\_blank}. To interact with these parachains, you can use the [Polkadot.js App](https://polkadot.js.org/apps/#/explorer){target=_blank} interface. For example:

- [Polkadot Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fasset-hub-polkadot-rpc.dwellir.com#/explorer){target=\_blank}
- [Kusama Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fsys.ibp.network%2Fstatemine#/explorer){target=\_blank}

For testing purposes, you can also interact with the Asset Hub instance of the following test networks:

- [Rococo Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fasset-hub-rococo-rpc.dwellir.com#/explorer){target=\_blank}
- [Paseo Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fpas-rpc.stakeworld.io%2Fassethub#/explorer){target=\_blank}

Before you start, ensure that you have: 

- Access to the Polkadot.js App interface, and you are connected to the desired chain
- A parachain that supports the XCMP protocol to register foreign assets in Asset Hub
- A funded wallet to pay for the transaction fees and subsequent registration of the foreign asset

This guide will focus on using Polkadot, its locally spawned Asset Hub instance, and the [Astar](https://astar.network/){taget=\_blank} parachain, as stated in the [Test Environment Setup](./register-a-foreign-asset.md/#test-enviroment-setup) section. However, the process is the same for other relay chains and their respective Asset Hub parachains, regardless of the network you are using.

## Steps to Register a Foreign Asset

1. Open the [Polkadot.js Apps](https://polkadot.js.org/apps/){target=_blank} interface and connect to the `Asset Hub` parachain

      - For the local environment, connect to `Local Node (Chopsticks)`, check the [Test Environment Setup](./register-a-foreign-asset.md/#test-enviroment-setup) section for more details
      - For the live network, connect to the `Asset Hub` parachain. You can use either Polkadot, Kusama or Rococo Asset Hub

2. Click on the **Developer** tab on the left sidebar and select the **Extrinsics** section

    ![Access to Developer Extrinsics section](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-1.webp)

3. Select the `Foreign Asset` pallet from the dropdown list and choose the `create` extrinsic

    ![Select the Foreign Asset pallet](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-2.webp)

4. Fill out the required fields and click on the copy icon to copy the **encoded call** to your clipboard

    ![Fill out the required fields](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-4.webp)

    ??? note
        If you want an encoded call example, you can copy the following: `0x35000101009501007369626c6500000000000000000000000000000000000000000000000000000000000000000000000000000000000000`

    The fields to be filled are:

    - `id` - as this is a foreign asset, the ID will be represented with a `Multilocation` that reflects its origin. For this case, the multilocation of the asset will be from the source parachain perspective:
  
        ```javascript
        MultiLocation {parents: 1, interior: X1(Parachain(101))};
        ```

    - `admin` - refers to the account that will be the admin of this asset. This account will be able to manage the asset, including updating its metadata. As the asset that is being registered corresponds to a native asset of the source parachain, the admin account should be the sovereign account of the source parachain. This account can be obtained through the [this utility](https://www.shawntabrizi.com/substrate-js-utilities/){target=\_blank}.

        ![Get parachain sovereign account](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-3.webp)

        !!!note 
            Ensure that `Sibling` is selected and the `Parachain ID` is the one of the source parachain, in this case, as the guide is following the test setup stated on the [Test Enviroment Setup](./register-a-foreign-asset.md/#enviroment-setup) section, the `Parachain ID` should be `101`.

5. Now, the Polkadot.js interface connected to the the parachain that will send the foreign asset to Asset Hub, go to the `Developer > Extrinsics` section and craft the following call. Ensure to paste the **encoded call** copied in the previous step and click on the **Submit Transaction** button after filling out the required fields.

    ![Register foreign asset through XCM](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-5.webp)

    First, DOT will be withdrawn from the sibling account of the parachain. Then, the DOT will be used to initiate an execution. The transaction will be carried out with the origin kind as XCM, and the transaction will be the hex-encoded call for creating a foreign asset on Asset Hub for the specified parachain asset multilocation. Any surplus will be refunded, and the asset will be deposited back into the sibling account.

    ???note
        If you want to have the whole XCM call ready to be copied, go to go to the `Developer > Extrinsics > Decode` section and paste the following hex-encoded call: `0x020033000301010091010314000400010000070010a5d4e81300010000070010a5d4e80006030700b4f13501419ce035000101009501007369626c6500000000000000000000000000000000000000000000000000000000000000000000000000000000000000140d01000001009501`

        Ensure to replace the encoded call with the one you copied in the previous step.


## Test Enviroment Setup

To test the foreign asset registration process before deploying it on the live network, you can set up a local parachain environment. This guide uses `chopsticks` to simulate that process. For more information on using chopsticks, please refer to the [Chopsticks documentation](../../../dev-tools/chopsticks/overview.md){target=_blank}.

To set up a test environment, run the following command:

```bash
npx @acala-network/chopsticks xcm \
--r polkadot \
--p polkadot-asset-hub \
--p astar
```
!!! note
    The above command will create a lazy fork of Polkadot as the relay chain, its Asset Hub instance, and the Astar parachain. The `xcm` parameter enables communication through the XCMP protocol between the relay chain and the parachains, allowing the registration of foreign assets on Asset Hub. For further information on the chopsticks usage of the XCMP protocol, refer to the [XCM Testing](../../../dev-tools/chopsticks/overview.md#xcm-testing){target=_blank} section of the Chopsticks documentation.