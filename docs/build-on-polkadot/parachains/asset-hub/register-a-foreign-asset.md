---
title: Register a foreign asset
description: An in-depth guide to registering a foreign asset on the Asset Hub parachain, providing clear, step-by-step instructions.
---

# Register a foreign asset on Asset Hub

## Introduction

As outlined in the [Asset Hub Overview](./overview.md#foreign-assets){target=_blank}, Asset Hub supports two categories of assets: local and foreign. Foreign assets are originated outside of Asset Hub and are recognized by [`Multilocations`](https://wiki.polkadot.network/docs/learn/xcm/fundamentals/multilocation-summary){target=_blank}. This guide will walk you through the process of registering a foreign asset on the Asset Hub parachain.

In order to register a foreign asset on Asset Hub, it's important to notice that the process involves a communication between two parachains. Asset Hub parachain will be the destination of the foreign asset, while the source parachain will be the origin of the asset. The communication between the two parachains is facilitated by the [Cross-Chain Message Passing (XCMP)](https://wiki.polkadot.network/docs/learn-xcm){target=_blank} protocol.

## Prerequisites

Asset Hub parachain exists as a one of the system parachains on a relay chain, such as [Polkadot](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fpolkadot.api.onfinality.io%2Fpublic-ws#/explorer){target=\_blank} or [Kusama](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fkusama.api.onfinality.io%2Fpublic-ws#/explorer){target=\_blank}. To interact with those parachains, you can use the [Polkadot.js App](https://polkadot.js.org/apps/#/explorer){target=_blank} interface. For example:

- [Polkadot Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fasset-hub-polkadot-rpc.dwellir.com#/explorer){target=\_blank}
- [Kusama Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fsys.ibp.network%2Fstatemine#/explorer){target=\_blank}
- And for testing purposes, [Rococo Asset Hub](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fasset-hub-rococo-rpc.dwellir.com#/explorer){target=\_blank}

So, before you start, ensure that you have:

- Access to the Polkadot.js App interface and you are connected to the desired chain
- A parachain that supports the XCMP protocol and is able to send the foreign asset to Asset Hub
- A funded wallet to pay for the transaction fees and consequent registration of the foreign asset

This guide will focus on using Rococo and its Asset Hub instance spawned locally, as stated on the [Test Enviroment Setup](./register-a-foreign-asset.md/#enviroment-setup) section. However, the process is the same for other relay chains and their respective Asset Hub parachains, regardless of the network you are using.

## Steps to Register a Foreign Asset

1. Open the [Polkadot.js Apps](https://polkadot.js.org/apps/){target=_blank} interface and connect to the `Asset Hub` parachain

      - For the local environment, connect to `Local Node (Zombienet)`, available the link your terminal will provide
      - For the live network, connect to the `Asset Hub` parachain. You can use either Polkadot, Kusama or Rococo Asset Hub

2. Click on the **Developer** tab on the left sidebar and select the **Extrinsics** section

    ![Access to Developer Extrinsics section](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-1.webp)

3. Select the `Foreign Asset` pallet from the dropdown list and choose the `create` extrinsic

    ![Select the Foreign Asset pallet](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-2.webp)

4. Fill out the required fields

    - `id` - as this is a foreign asset, the ID will be represented with a `Multilocation` that reflects its origin.
    - `admin` - refers to the account that will be the admin of this asset. This account will be able to manage the asset, including updating its metadata. As the asset that is being registered corresponds to a native asset of the source parachain, the admin account should be the sovereign account of the source parachain. This account can be obtained through the [this utility](https://www.shawntabrizi.com/substrate-js-utilities/){target=\_blank}.

        ![Get parachain sovereign account](/polkadot-ecosystem-docs-draft/images/building-on-polkadot/parachains/asset-hub/register-a-foreign-asset/register-a-foreign-asset-3.webp)

    !!!note 
        Ensure that `Sibling` is selected and the `Parachain ID` is the one of the source parachain, in this case, as the guide is following the test setup stated on the [Test Enviroment Setup](./register-a-foreign-asset.md/#enviroment-setup) section, the `Parachain ID` should be `101`.


## Test Enviroment Setup

It might be beneficial to set up a local testing environment to first check out the asset registration process before deploying it on the live network. This guide uses `zombienet` to simulate that process. For further information on zombienet usage, refer to the [Zombienet](../../../dev-tools/zombienet/overview.md){target=\_blank} documentation.

To set up a test environment then, create a file named `minimal-config-asset-hub-rococo.toml` with the following content:

```toml
[relaychain]
chain = "rococo-local"

  [[relaychain.nodes]]
  name = "alice"
  validator = true

  [[relaychain.nodes]]
  name = "bob"
  validator = true

[[parachains]]
id = 100
chain = "asset-hub-rococo-local"

  [parachains.collator]
  name = "collator01"
  command = "polkadot-parachain"


[[parachains]]
id = 101

  [parachains.collator]
  name = "collator02"
  command = "polkadot-parachain"
```

Then, execute the following command:

```bash
./zombienet -p native spawn minimal-config-asset-hub-rococo.toml
```

!!!note 
    The above command will spawn a Rococo relay chain with two validators: alice and bob. Also, it will spawn an Asset Hub parachain instance with ID 100 and a collator named collator01. Finally, it will spawn another parachain instance with ID 101 and a collator named collator02, which will be used to simulate the source parachain of the foreign asset.
    
Now, you have a Rococo relay chain running locally and can proceed with the asset registration process. Note that the local registering process does not differ from the live network process, so you can use the same steps for both.

