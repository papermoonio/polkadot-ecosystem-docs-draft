---
title: How to Deploy a Parachain on Polkadot's Paseo TestNet
description: This comprehensive guide walks through the entire process of deploying your blockchain as a parachain on Polkadot's Paseo TestNet. Learn how to reserve a Parachain ID, generate a customized chain spec, register a parathread, obtain a dedicated parachain slot, and set up your parachain collator node. Leverage Paseo for parachain development and testing before launching on Polkadot MainNet.
---

# Deploying a Parachain on Paseo TestNet

## Introduction

Paseo is a community run TestNet designed for parachain teams and dApp developers to build and test their solutions. The Paseo network is open, allowing anyone to launch an appchain (parachain) as part of their process for eventual deployment onto the Polkadot MainNet.

It provides dedicated parachain slots to maintainers, with the lease period duration varying based on the following criteria:

- Maintainers of live parachains on the Polkadot or Kusama mainnets will be granted a dedicated Paseo parachain slot for a one year lease period

- Maintainers of parachains under active development, or those that have not yet secured a parachain slot on Kusama or Polkadot, will be assigned a shorter Paseo lease period of two weeks

This guide will walk you through the process of deploying your blockchain as a parachain on the Paseo TestNet. We'll cover reserving a Parachain ID, generating a customized chain spec, registering a parathread, securing a dedicated parachain slot, and finally, setting up and running your parachain.

## Prerequisites

Before you can deploy your parachain on the Paseo TestNet, you'll need to meet the following requirements:

[//]: <> (//TODO: Add links to the following items)

- [Wallet]() - a Substrate-supported wallet to deploy and manage your parachain
- [PAS Tokens]() - the native currency of the Paseo TestNet to pay for transaction fees
- [Parachain Runtime]() - a fully operational blockchain capable of operating as a parachain

## Reserve a Parachain ID

To deploy your parachain, you'll first need to reserve a unique Parachain ID on the Paseo TestNet.

1. Visit [Polkadot.js](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fpaseo-rpc.dwellir.com#/explorer){target=_blank} and ensure you're connected to the Paseo TestNet.

2. Navigate to the **Network** dropdown, then select the **Parachains** option from the menu that appears
    ![The Network menu for the Paseo TestNet on Polkadot.js Apps](/images/paseo-testnet/onboarding/onboarding-1.webp)

3. Switch to the **Parathreads** tab and click the **+ParaId** button.
    ![The Parathreads section on Polkadot.js Apps](/images/paseo-testnet/onboarding/onboarding-2.webp)

4. Submit the transaction and save the assigned Parachain ID for future reference.
    ![Parachain reservation form](/images/paseo-testnet/onboarding/onboarding-3.webp)

    !!! note
        In this example, the Parachain ID assigned is 4018.

## Generate and Customize the Chainspec

In this guide, the [generic template](https://github.com/OpenZeppelin/polkadot-runtime-templates/tree/v1.0.0){target=_blank} from [OpenZeppelin Substrate Parachain Runtimes](https://docs.openzeppelin.com/substrate-runtimes/1.0.0/){target=_blank} will be used to quickly bootstrap a Substrate project for the Paseo TestNet.

Before starting, clone the repository and execute the build command:
```bash
git clone -b v1.0.0 https://github.com/OpenZeppelin/polkadot-runtime-templates.git
cd polkadot-runtime-templates
cargo build --release
```

1. Generate a plain chain spec:

    ```bash
    ./target/release/parachain-template-node build-spec \
    --disable-default-bootnode > plain-parachain-chainspec.json
    ```

2. Edit the `plain-parachain-chainspec.json` file:
    - Update the `name`, `id`, and `protocolId` to unique values for your parachain.
    - Change `relay_chain` to `paseo`.
    - Change `para_id` and `parachainInfo.parachainId` from 1000 to the Parachain ID you reserved in step 1.

    ```json
    {
        "name": "My Parachain Name",
        "id": "my_parachain",
        "chainType": "Local",
        "bootNodes": [],
        "telemetryEndpoints": null,
        "protocolId": "my_para",
        "properties": {
            "ss58Format": 42,
            "tokenDecimals": 12,
            "tokenSymbol": "UNIT"
        },
        "relay_chain": "paseo",
        "para_id": 4018,
        "codeSubstitutes": {},
        "genesis": {
            "runtimeGenesis": {
                "code": "...",
                "patch": {
                    "balances": {...},
                    "collatorSelection": {...},
                    "parachainInfo": {
                        "parachainId": 4018
                    },
                    "polkadotXcm": {
                        "safeXcmVersion": 4
                    },
                    "session": {...},
                    "sudo": {...}
                }
            }
        }
    }
    ```

3. Generate a raw chain spec:

    ```bash
    ./target/release/parachain-template-node build-spec --chain plain-parachain-chainspec.json \ 
    --disable-default-bootnode --raw > raw-parachain-chainspec.json
    ```

## Register a Parathread

Before securing a dedicated parachain slot, you'll need to register a parathread on the Paseo TestNet. 

!!!note
    Replace `INSERT_PARA_ID` with the actual Parachain ID you reserved earlier when executing the following commands:

1. Generate a genesis state:

    ```bash
    ./target/release/parachain-template-node export-genesis-state \
    --chain raw-parachain-chainspec.json para-<INSERT_PARA_ID>-genesis-state
    ```

2. Generate a genesis Wasm:

    ```bash
    ./target/release/parachain-template-node export-genesis-wasm \
    --chain raw-parachain-chainspec.json para-<INSERT_PARA_ID>-wasm
    ```

3. Visit [Polkadot.js](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fpaseo-rpc.dwellir.com#/explorer){target=_blank}, navigate to the **Network** dropdown and then select the **Parachains** option.
    ![The Network menu for the Paseo TestNet on Polkadot.js Apps](/images/paseo-testnet/onboarding/onboarding-1.webp)

4. Click the **+ParaThread** button.
    ![The Parathreads section on Polkadot.js Apps](/images/paseo-testnet/onboarding/onboarding-4.webp)

5. Submit the generated genesis state and genesis Wasm files.
    ![Form to register a parathread](/images/paseo-testnet/onboarding/onboarding-5.webp)

[//]: <> (//TODO: This last extrinsic is failing with Insufficient balance. Need to investigate further.)

## Obtain a Parachain Slot

To upgrade your parathread to a full parachain, you must secure a dedicated parachain slot.

1. Submit an issue via the [Paseo Support repository](https://github.com/paseo-network/support){target=_blank} using the [Paseo Parachain Onboarding issue template](https://github.com/paseo-network/support/issues/new/choose){target=_blank}.

2. Once your request is reviewed and approved, you'll be allocated a dedicated parachain slot.


## Set Up Your Parachain

With a parachain slot secured, you can now set up and run your parachain on the Paseo TestNet.

1. Download the [Paseo Spec](https://github.com/paseo-network/runtimes/blob/main/chain-specs/paseo.raw.json){target=_blank}.

2. Start your parachain collator node by running the command with the appropriate flags and options for your setup. For example:

    ```bash
    ./target/release/parachain-template-node \
    --alice \
    --collator \
    --force-authoring \
    --chain raw-parachain-chainspec.json \
    --base-path ./data \
    --port 40333 \
    --rpc-port 8845 \
    -- \
    --execution wasm \
    --chain paseo.raw.json \
    --port 30343 \
    --rpc-port 9977
    ```

Congratulations! You've successfully deployed your parachain on the Paseo TestNet. You can now test and iterate on your blockchain project within the Paseo ecosystem.