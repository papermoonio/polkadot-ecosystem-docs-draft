---
title: Register a local asset
description: Comprehensive guide to registering a local asset on the Asset Hub system parachain, including step-by-step instructions.
---

# Register a local asset on Asset Hub

## Introduction
As detailed in the [Asset Hub Overview](./overview.md#local-assets){target=_blank} page, Asset Hub accommodates two types of assets: local and foreign. Local assets are those that were created in Asset Hub and are identifiable by an integer ID. This guide will take you through the steps of registering a local asset on the Asset Hub parachain.

## Prerequisites

Before you begin, ensure you have access to the [Polkadot.js Apps](https://polkadot.js.org/apps/){target=_blank} interface and a Polkadot.js account with a balance of DOT or KSM.

- For Polkadot Asset Hub, you would need a `deposit of 10 DOT` and around `0.201 DOT for the metadata`
- For Kusama Asset Hub, the `deposit is 0.1 KSM` and around `0.000669 KSM for the metadata`

You need to ensure that your Asset Hub account balance is a bit more than the sum of those two deposits, which should seamlessly account for the required deposits and transaction fees.

## Enviroment setup

It might be beneficial to set up a local parachain environment to test the asset registration process before deploying it on the live network. This guide uses `chopsticks` to simulate that process. For further information on chopsticks usage, refer to the [Chopsticks documentation](../../../dev-tools/chopsticks/overview.md){target=_blank}.

To set up a test enviroment then, execute the following command:

```bash
npx @acala-network/chopsticks \
--config=https://raw.githubusercontent.com/AcalaNetwork/chopsticks/master/configs/polkadot-asset-hub.yml
```

!!!note 
    The above command will spawn a lazy fork of Polkadot Asset Hub, with the latest block data from the network. If you need to test Kusama Asset Hub, replace `polkadot-asset-hub.yml` with `kusama-asset-hub.yml` in the command.

Now, an Asset Hub instance is running locally, and you can proceed with the asset registration process. Note that the local registering process does not differ from the live network process, so you can use the same steps for both.

## Steps to register a local asset

To register a local asset on the Asset Hub parachain, follow these steps:

1. Open the [Polkadot.js Apps](https://polkadot.js.org/apps/){target=_blank} interface and connect to the `Asset Hub` parachain.
      - For the local environment, connect to `Local Node (Chopsticks)`, available on `ws://localhost:8000`
      - For the live network, connect to the `Asset Hub` parachain. Either Polkadot or Kusama Asset Hub can be selected from the dropdown list.
    
2. Click on the `Network` tab on the left sidebar and select the `Asset Hub` parachain from the dropdown list.
      ![Access to Asset Hub through Polkadot.JS](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/registering-a-local-asset/registering-a-local-asset-1.webp) 

3. Now, you need to examine all the assets IDs that are already registered. This step is crucial to ensure that the asset ID you are about to register is unique. Assets IDs are displayed in the `assets` column.
      ![Asset IDs on Asset Hub](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/registering-a-local-asset/registering-a-local-asset-2.webp)

4. Once you have confirmed that the asset ID is unique, click on the `Create` button on the top right corner of the page.
   
      ![Create a new asset](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/registering-a-local-asset/registering-a-local-asset-3.webp)

5. Fill in the required fields in the `Create Asset` form:
   
    - `creator account`: The account to be used for creating this asset and setting up the initial metadata.
    - `asset name` - the descriptive name of the asset you are registering.
    - `asset symbol` - the symbol that will be used to represent the asset.
    - `asset decimals` - the number of decimal places for this token, with a maximum of 20 allowed through the user interface.
    - `minimum balance` - the minimum balance for the asset. This is specified in the units and decimals as requested.
    - `asset ID` - the selected id for the asset. This should not match an already-existing asset id.
 
    ![Create Asset Form](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/registering-a-local-asset/registering-a-local-asset-4.webp)
