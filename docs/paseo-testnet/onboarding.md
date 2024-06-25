---
title: How to Deploy a Parachain on Polkadot's Paseo TestNet
description: This guide walks through the entire process of deploying a parachain on Polkadot's Paseo TestNet.
---

# Deploying a Parachain on Paseo TestNet

## Introduction

Paseo is a community-run TestNet designed for parachain teams and dApp developers to build and test their solutions. The Paseo network is open, allowing anyone to launch an appchain (parachain) as part of their process for eventual deployment onto the Polkadot MainNet.

It provides dedicated parachain slots to maintainers, with the lease period duration varying based on the following criteria:

- Maintainers of live parachains on the Polkadot or Kusama MainNets will be granted a dedicated Paseo parachain slot for a one-year lease period

- Maintainers of parachains under active development, or those that have not yet secured a parachain slot on Kusama or Polkadot, will be assigned a shorter Paseo lease period of two weeks

This guide will walk you through the process of deploying your blockchain as a parachain on the Paseo TestNet. We'll cover generating a customized chain spec, securing a dedicated parachain slot, and finally, setting up and running your parachain.

## Prerequisites

Before you can deploy your parachain on the Paseo TestNet, you'll need to meet the following requirements:

[//]: <> (//TODO: Add links to the following items)

- [Wallet]() - a Substrate-supported wallet to deploy and manage your parachain
- [PAS Tokens]() - the native currency of the Paseo TestNet to pay for transaction fees
- [Parachain Runtime]() - a fully operational blockchain capable of operating as a parachain

## Select a Parachain ID

To deploy your parachain, you'll first need to select a unique parachain ID on the Paseo TestNet.

1. Visit [Polkadot.js]({{ polkadot_js.paseo_rpc.explorer }}){target=_blank} and ensure you're connected to the Paseo TestNet

2. Navigate to the **Network** dropdown, then select the **Parachains** option from the menu that appears
    ![The Network menu for the Paseo TestNet on Polkadot.js Apps](/images/paseo-testnet/onboarding/onboarding-1.webp)

3. Review the list of active parachains and select an available parachain ID for your chain. Ensure the ID you choose is not currently used by examining the **parachains column** in the table below. Save the selected ID for future reference
    ![The Parachains section on Polkadot.js Apps](/images/paseo-testnet/onboarding/onboarding-6.webp)


## Generate and Customize the Chain Spec

This guide demonstrates the process using the [generic template]({{ repositories.open_zeppelin.polkadot_runtime_generic_template }}){target=_blank} from [OpenZeppelin Substrate Parachain Runtimes]({{ repositories.open_zeppelin.parachain_runtime_template
}}){target=_blank}. Most of the time, you will use your own custom runtime. The steps outlined here are adaptable to your specific runtime with minor adjustments.

Before starting, clone the repository and execute the build command:
```bash
git clone -b v1.0.0 {{ repositories.open_zeppelin.polkadot_runtime_template }}
cd polkadot-runtime-templates
cargo build --release
```

!!!note
    The `cargo build --release` command will take a considerable amount of time to complete, depending on your system's specifications. This is normal for Substrate-based projects due to their complexity.

1. Generate a plain chain spec:

    ```bash
    ./target/release/parachain-template-node build-spec \
    --disable-default-bootnode > plain-parachain-chainspec.json
    ```

2. Edit the `plain-parachain-chainspec.json` file:
    - Update the `name`, `id` and `protocolId` fields to unique values for your parachain
    - Change the `relay_chain` field to `paseo`
    - Change `para_id` and `parachainInfo.parachainId` from 1000 to the parachain ID you selected in the previous steps
    - Modify the `sudo` value to specify the account that will have sudo access to the parachain

    ```json
    {
        "name": "INSERT_NAME",
        "id": "INSERT_ID",
        "chainType": "Local",
        "bootNodes": [],
        "telemetryEndpoints": null,
        "protocolId": "INSERT_PROTOCOL_ID",
        "properties": {
            "ss58Format": 42,
            "tokenDecimals": 12,
            "tokenSymbol": "UNIT"
        },
        "relay_chain": "paseo",
        "para_id": INSERT_SELECTED_PARA_ID,
        "codeSubstitutes": {},
        "genesis": {
            "runtimeGenesis": {
                "code": "...",
                "patch": {
                    "balances": {...},
                    "collatorSelection": {...},
                    "parachainInfo": {
                        "parachainId": INSERT_SELECTED_PARA_ID
                    },
                    "polkadotXcm": {
                        "safeXcmVersion": 4
                    },
                    "session": {...},
                    "sudo": {
                        "key": "INSERT_SUDO_ACCOUNT"
                    }
                }
            }
        }
    }
    ```

    !!!note
        For more detailed information on customizing your chain spec, please check the section [Customizing Chain Specifications]()

3. Generate a raw chain spec:

    ```bash
    ./target/release/parachain-template-node build-spec --chain plain-parachain-chainspec.json \
    --disable-default-bootnode --raw > raw-parachain-chainspec.json
    ```

## Obtain a Parachain Slot

Before securing a dedicated parachain slot, you'll need to generate a genesis state and Wasm for your chain.

!!!note
    Replace `<INSERT_SELECTED_PARA_ID>` with the actual parachain ID you reserved earlier when executing the following commands:

1. Generate a genesis state:

    ```bash
    ./target/release/parachain-template-node export-genesis-state \
    --chain raw-parachain-chainspec.json para-<INSERT_SELECTED_PARA_ID>-genesis-state
    ```

2. Generate a genesis Wasm:

    ```bash
    ./target/release/parachain-template-node export-genesis-wasm \
    --chain raw-parachain-chainspec.json para-<INSERT_SELECTED_PARA_ID>-wasm
    ```

3. Create an issue in the Paseo support repository using the [Paseo Parachain Onboarding issue template]({{ repositories.paseo_network.onboarding_issue_template }}){target=_blank}

    ![Paseo Support Issue Templates](/images/paseo-testnet/onboarding/onboarding-7.webp)

4. Ensure you fill in all the necessary information, including your parachain name, selected parachain ID, manager account, genesis state, and genesis Wasm files from the previous steps. After filling in the required details, submit the issue
    ![Paseo Parachain Onboarding Issue Template](/images/paseo-testnet/onboarding/onboarding-8.webp)

5. Once your request is reviewed and approved, you'll be allocated a dedicated parachain slot

## Set Up Your Parachain

With a parachain slot secured, you can now set up and run your parachain on the Paseo TestNet.

1. Download the [Paseo spec](https://github.com/paseo-network/runtimes/blob/main/chain-specs/paseo.raw.json){target=_blank}

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