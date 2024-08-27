---
title: Convert assets on Asset Hub
description: A guide detailing the step-by-step process of converting assets on Asset Hub, helping users navigate the asset management on the platform efficiently.
---

# Asset Conversion on Asset Hub

## Introduction

Asset Conversion is an Automated Market Maker (AMM) that utilizes [Uniswap V2](https://github.com/Uniswap/v2-core){target=\_blank} logic and is implemented as a pallet on Polkadot's AssetHub. For more details about this feature, please visit the [Asset Conversion on Asset Hub](https://wiki.polkadot.network/docs/learn-asset-conversion-assethub){target=\_blank} page. 

This guide will provide detailed information about the key functionalities offered by the
[Asset Conversion](https://github.com/paritytech/polkadot-sdk/tree/master/substrate/frame/asset-conversion){target=\_blank} pallet on Asset Hub, including: 

- Creating a liquidity pool
- Adding liquidity to a pool
- Swapping assets
- Withdrawing liquidity from a pool

## Prerequisites

Before converting assets on Asset Hub, you must ensure to have:

- Access the [Polkadot.Js App](https://polkadot.js.org/apps){target=\_blank} interface and connect it to the intended blockchain
- A funded wallet containing the assets you wish to convert, and that the wallet has enough balance to cover the transaction fees
- An asset registered on Asset Hub that you wish to convert. If you haven't created an asset on Asset Hub yet, you can refer either to the [Register a Local Asset](./docs/build-on-polkadot/parachains/asset-hub/register-a-foreign-asset.md){target=\_blank} or [Register a Foreign Asset](./docs/build-on-polkadot/parachains/asset-hub/register-a-local-asset.md){target=\_blank} documentation to create an asset.

## Creating a Liquidity Pool

If there is no existing liquidity pool for an asset on Asset Hub, the first step is to create a liquidity pool. 

The asset conversion pallet provides the `create_pool` extrinsic to create a new liquidity pool. It is used to create an empty liquidity pool along with a new `LP token` asset. 

For this example, a testing token with the asset ID `1112` and the name `PPM` was created.

As stated in the [Test Environment Setup](#test-environment-setup) section, this tutorial is based on the assumption that you have an instance of Polkadot Asset Hub running locally. Therefore, the creation of the liquidity pool will be between DOT and PPM tokens. However, the same steps can be applied to any other asset on Asset Hub.

From the Asset Hub perspective, the Multilocation that identifies the PPM token is the following:

```javascript
{
   parents: 0,
   interior: {
     X2: [{PalletInstance: 50}, {GeneralIndex: 1112}]
   }
}
```

!!!note 
    The PalletInstance of 50 represents the Assets pallet on Asset Hub and the GeneralIndex (1112) is the Asset ID of the PPM asset.

To create the liquidity pool, you can follow these steps:

1. Navigate to the **Extrinsics** tab on the Polkadot.Js App interface
   1. Select **Developer** from the top menu
   2. Click on **Extrinsics** from the dropdown menu

2. Select the **AssetConversion** pallet from the **Pallets** dropdown menu

3. Choose the `create_pool` extrinsic from the list of available extrinsics

4. Fill in the required fields:


## Adding Liquidity to a Pool

## Swapping Assets

## Withdrawing Liquidity from a Pool

## Test Environment Setup

To test the Asset Conversion pallet, you can set up a local test environment to simulate different scenarios. This guide uses Chopsticks to spin up an instance of Polkadot Asset Hub. For further details on using Chopsticks, please refer to the [Chopsticks documentation](./docs/dev-tools/chopsticks/overview.md){target=\_blank}.

To set up a local test environment, execute the following command:

```bash
npx @acala-network/chopsticks \
--config=https://raw.githubusercontent.com/AcalaNetwork/chopsticks/master/configs/polkadot-asset-hub.yml
```

!!! note 
    This command initiates a lazy fork of Polkadot Asset Hub, including the most recent block information from the network. For Kusama Asset Hub testing, simply switch out `polkadot-asset-hub.yml` with `kusama-asset-hub.yml` in the command.

You now have a local Asset Hub instance up and running, ready for you to test various asset conversion procedures. The process here mirrors what you'd do on MainNet. After completing a transaction on TestNet, you can apply the same steps to convert assets on MainNet.