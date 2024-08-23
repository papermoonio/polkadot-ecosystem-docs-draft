---
title: Register a Foreign Asset on Asset Hub
description: An in-depth guide to registering a foreign asset on the Asset Hub parachain, providing clear, step-by-step instructions.
---

# Register a Foreign Asset on Asset Hub

## Introduction

As outlined in the [Asset Hub Overview](./overview.md#foreign-assets){target=\_blank}, Asset Hub supports two categories of assets: local and foreign. Foreign assets originated outside of Asset Hub are recognized by [Multilocations](https://wiki.polkadot.network/docs/learn/xcm/fundamentals/multilocation-summary){target=\_blank}. This guide will walk you through the process of registering a foreign asset on the Asset Hub parachain.

When registering a foreign asset on Asset Hub, it's essential to notice that the process involves communication between two parachains. The Asset Hub parachain will be the destination of the foreign asset, while the source parachain will be the origin of the asset. The communication between the two parachains is facilitated by the [Cross-Chain Message Passing (XCMP)](https://wiki.polkadot.network/docs/learn-xcm){target=\_blank} protocol.

## Prerequisites

The Asset Hub parachain is one of the system parachains on a relay chain, such as [Polkadot](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fpolkadot.api.onfinality.io%2Fpublic-ws#/explorer){target=\_blank} or [Kusama](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fkusama.api.onfinality.io%2Fpublic-ws#/explorer){target=\_blank}. To interact with these parachains, you can use the [Polkadot.js Apps](https://polkadot.js.org/apps/#/explorer){target=\_blank} interface for:

- [Polkadot Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fasset-hub-polkadot-rpc.dwellir.com#/explorer){target=\_blank}
- [Kusama Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fsys.ibp.network%2Fstatemine#/explorer){target=\_blank}

For testing purposes, you can also interact with the Asset Hub instance on the following test networks:

- [Rococo Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fasset-hub-rococo-rpc.dwellir.com#/explorer){target=\_blank}
- [Paseo Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fpas-rpc.stakeworld.io%2Fassethub#/explorer){target=\_blank}

Before you start, ensure that you have: 

- Access to the Polkadot.js App interface, and you are connected to the desired chain
- A parachain that supports the XCMP protocol to interact with the Asset Hub parachain
- A funded wallet to pay for the transaction fees and subsequent registration of the foreign asset

This guide will focus on using Polkadot, its local Asset Hub instance, and the [Astar](https://astar.network/){target=\_blank} parachain (`ID` 2006), as stated in the [Test Environment Setup](#test-environment-setup) section. However, the process is the same for other relay chains and their respective Asset Hub parachains, regardless of the network you are using and the parachain owner of the foreign asset.

## Steps to Register a Foreign Asset

1. Open the [Polkadot.js Apps](https://polkadot.js.org/apps/){target=\_blank} interface and connect to the `Asset Hub` parachain

      - For the local environment, connect to Local Node (Chopsticks), check the [Test Environment Setup](#test-environment-setup) section for more details
      - For the live networks, connect to the `Asset Hub` parachain. You can use either Polkadot, Kusama, Rococo, or Paseo Asset Hub

2. Click on the **Developer** tab on the left sidebar and select the **Extrinsics** section

    ![Access to Developer Extrinsics section](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-1.webp)

3. Select the **foreignAssets** pallet from the dropdown list and choose the **create** extrinsic

    ![Select the Foreign Asset pallet](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-2.webp)

4. Fill out the required fields and click on the copy icon to copy the **encoded call data** to your clipboard. The fields to be filled are:

    - **id** - as this is a foreign asset, the ID will be represented by a Multilocation that reflects its origin. For this case, the Multilocation of the asset will be from the source parachain perspective:
  
        ```javascript
        MultiLocation {parents: 1, interior: X1(Parachain(2006))};
        ```

    - **admin** - refers to the account that will be the admin of this asset. This account will be able to manage the asset, including updating its metadata. As the registered asset corresponds to a native asset of the source parachain, the admin account should be the sovereign account of the source parachain
      
        ??? note
            The sibling account can be obtained through [Substrate Utilities](https://www.shawntabrizi.com/substrate-js-utilities/){target=\_blank}

            ![Get parachain sovereign account](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-4.webp)

            Ensure that **Sibling** is selected and that the **Parachain ID** corresponds to the source parachain. In this case, since the guide follows the test setup stated in the [Test Environment Setup](./register-a-foreign-asset.md/#test-enviroment-setup) section, the **Parachain ID** is `2006`.

    - **minBalance** - the minimum balance required to hold this asset

    ![Fill out the required fields](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-3.webp)

    ??? note
        If you want an example of the encoded call data, you can copy the following: `0x3500010100591f007369626cd6070000000000000000000000000000000000000000000000000000a0860100000000000000000000000000`

5. With the Polkadot.js interface connected to the parachain that will send the foreign asset to Asset Hub, navigate to the **Developer > Extrinsics** section. Create the following call, and paste the **encoded call data** copied in the previous step. After filling out the required fields, click the **Submit Transaction** button

    ![Register foreign asset through XCM](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-5.webp)

    First, DOT will be withdrawn from the sibling account of the parachain. Then, the DOT will be used to initiate an execution. The transaction will be carried out with the origin kind as XCM, and the transaction will be the hex-encoded call for creating a foreign asset on Asset Hub for the specified parachain asset multilocation. Any surplus will be refunded, and the asset will be deposited into the sibling account.

    !!! warning
        Note that the sovereign account on the Asset Hub parachain must have a sufficient balance to cover the XCM `BuyExecution` instruction. If the account does not have enough balance, the transaction will fail.

    ???note
        If you want to have the whole XCM call ready to be copied, go to the **Developer > Extrinsics > Decode** section and paste the following hex-encoded call data: `0x6300330003010100a10f030c000400010000070010a5d4e81300010000070010a5d4e80006030700b4f13501419ce03500010100591f007369626cd607000000000000000000000000000000000000000000000000000000000000000000000000000000000000`

        Ensure to replace the encoded call data with the one you copied in the previous step.

After the transaction is successfully executed, the foreign asset will be registered on the Asset Hub parachain. 

## Asset Registration Verification

To confirm that a foreign asset has been successfully accepted and registered on the Asset Hub parachain, you can navigate to the `Network > Explorer` section of the Polkadot.js App interface. You should be able to see an event that includes the following details:

![Asset registration event](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-6.webp)

In the image above, the **success** field indicates whether the asset registration was successful.

## Test Environment Setup

To test the foreign asset registration process before deploying it on the live network, you can set up a local parachain environment. This guide uses `chopsticks` to simulate that process. For more information on using chopsticks, please refer to the [Chopsticks documentation](../../../dev-tools/chopsticks/overview.md){target=\_blank}.

To set up a test environment, run the following command:

```bash
npx @acala-network/chopsticks xcm \
--r polkadot \
--p polkadot-asset-hub \
--p astar
```

!!! note
    The above command will create a lazy fork of Polkadot as the relay chain, its Asset Hub instance, and the Astar parachain. The `xcm` parameter enables communication through the XCMP protocol between the relay chain and the parachains, allowing the registration of foreign assets on Asset Hub. For further information on the chopsticks usage of the XCMP protocol, refer to the [XCM Testing](../../../dev-tools/chopsticks/overview.md#xcm-testing){target=\_blank} section of the Chopsticks documentation.

After executing the command, the terminal will display the subsequent output:

--8<-- 'code/build-on-polkadot/parachains/asset-hub/register-a-foreign-asset/terminal/chopstick-test-env-output.md'

According to the output, the Polkadot relay chain, the Polkadot Asset Hub, and the Astar parachain are running locally and connected through XCM. They can be accessed via the Polkadot.js Apps interface:

- [Polkadot Relay Chain](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Flocalhost%3A8002#/explorer){target=\_blank}
- [Polkadot Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Flocalhost%3A8000#/explorer){target=\_blank}
- [Astar Parachain](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Flocalhost%3A8001#/explorer){target=\_blank}