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
    ![The Parachains section on Polkadot.js Apps](/images/paseo-testnet/onboarding/onboarding-2.webp)

## Generate customs keys for your collators

To securely deploy your parachain, it is essential to generate custom keys specifically for your collators. You should generate two set of keys for each collator:

- Account keys - used to interact with the network and manage funds. Should be protected carefully and should never exist on the filesystem of the collator node

- Session keys - used in block production. These identify your node and its blocks on the network. Stored in the parachain keystore, these are disposable "hot wallet" keys. If leaked, they could be used to impersonate your node, potentially leading to fund slashing. To mitigate risks, rotate these keys frequently. Treat them with the same caution as a hot wallet to protect your node security

To perform this step you can use [subkey]({{ tools.subkey }}){target=_blank}, a command-line tool for generating and managing keys.

```bash
docker run -it parity/subkey:latest generate --scheme sr25519
```

!!!note
    Several methods can be used to generate your keys. This tutorial opts for using the [subkey Docker image]({{ docker_images.parity.subkey }}){target=_blank} for simplicity.

The output should look similar to the following:

```bash
Secret phrase:     lemon play remain picture leopard frog mad bridge hire hazard best buddy
Network ID:        substrate
Secret seed:       0xb748b501de061bae1fcab1c0b814255979d74d9637b84e06414a57a1a149c004
Public key (hex):  0xf4ec62ec6e70a3c0f8dcbe0531e2b1b8916cf16d30635bbe9232f6ed3f0bf422
Account ID:        0xf4ec62ec6e70a3c0f8dcbe0531e2b1b8916cf16d30635bbe9232f6ed3f0bf422
Public key (SS58): 5HbqmBBJ5ALUzho7tw1k1jEgKBJM7dNsQwrtfSfUskT1a3oe
SS58 Address:      5HbqmBBJ5ALUzho7tw1k1jEgKBJM7dNsQwrtfSfUskT1a3oe
```

Ensure to execute this command twice to generate the keys for both the account and session keys. Save them for future reference.

## Generate and Customize the Chain Spec

This guide demonstrates the process using the [generic template]({{ repositories.open_zeppelin.polkadot_runtime_generic_template }}){target=_blank} from [OpenZeppelin Substrate Parachain Runtimes]({{ repositories.open_zeppelin.parachain_runtime_template
}}){target=_blank}. Most of the time, you will use your own custom runtime. The steps outlined here are adaptable to your specific runtime with minor adjustments.

Before starting, clone the repository and execute the build command:
```bash 
git clone -b {{ repositories.open_zeppelin.release_tag}} {{ repositories.open_zeppelin.polkadot_runtime_template }}
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
    - Insert the account IDs and session keys in SS58 format generated for your collators in the `collatorSelection.invulnerables` and `session.keys` fields
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
      "para_id": 1,
      "codeSubstitutes": {},
      "genesis": {
        "runtimeGenesis": {
          "code": "...",
          "patch": {
            "balances": {},
            "collatorSelection": {
              "candidacyBond": 16000000000,
              "invulnerables": [
                "INSERT_ACCOUNT_ID_COLLATOR_1",
                "INSERT_ACCOUNT_ID_COLLATOR_2"
              ]
            },
            "parachainInfo": {
              "parachainId": 1
            },
            "polkadotXcm": {
              "safeXcmVersion": 4
            },
            "session": {
              "keys": [
                [
                  "INSERT_ACCOUNT_ID_COLLATOR_1",
                  "INSERT_ACCOUNT_ID_COLLATOR_1",
                  {
                    "aura": "INSERT_SESSION_KEY_COLLATOR_1"
                  }
                ],
                [
                  "INSERT_ACCOUNT_ID_COLLATOR_2",
                  "INSERT_ACCOUNT_ID_COLLATOR_2",
                  {
                    "aura": "INSERT_SESSION_KEY_COLLATOR_2"
                  }
                ]
              ]
            },
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

    ![Paseo Support Issue Templates](/images/paseo-testnet/onboarding/onboarding-3.webp)

4. Ensure you fill in all the necessary information, including your parachain name, selected parachain ID, manager account, genesis state, and genesis Wasm files from the previous steps. After filling in the required details, submit the issue
    ![Paseo Parachain Onboarding Issue Template](/images/paseo-testnet/onboarding/onboarding-4.webp)

5. Once your request is reviewed and approved, you'll be allocated a dedicated parachain slot

## Set Up Your Parachain

With a parachain slot secured, you can now set up and run your parachain on the Paseo TestNet.
 
1. Download the [Paseo spec]({{ repositories.paseo_network.paseo_specs }}){target=_blank}

2. Start your parachain collator node by running the command with the appropriate flags and options for your setup. For example:

    ```bash
    ./target/release/parachain-template-node \
    --collator \
    --force-authoring \
    --chain raw-parachain-chainspec.json \
    --base-path ./data \
    --port 40333 \
    --rpc-port 8845 \
    -- \
    --sync warp \
    --execution wasm \
    --chain paseo.raw.json \
    --port 30343 \
    --rpc-port 9977
    ```

    !!!note
        For more information on the available command-line arguments you can provide to your collator node, execute the following command:

        ```bash
        ./target/release/parachain-template-node -h
        ```

3. Insert the session key previously generated in your collator keystore by running the following command with the appropriate values:

    ```bash
    curl -H "Content-Type: application/json" \
    --data '{
      "jsonrpc":"2.0",
      "method":"author_insertKey",
      "params":[
        "aura",
        "INSERT_SECRET_PHRASE",
        "INSERT_PUBLIC_KEY_HEX_FORMAT"
      ],
      "id":1
    }' \
    http://localhost:8845
    ```

    If successful, you should see the following response:

    ```json
    {"jsonrpc":"2.0","result":null,"id":1}
    ```
    
    !!!note
		Replace the port number `8845` with the RPC port you specified when starting your collator node. Also, replace `INSERT_SECRET_PHRASE` and `INSERT_PUBLIC_KEY_HEX_FORMAT` with the session key generated for your collator.
        

4. Once your collator is synced with the Paseo relay chain, it will begin producing blocks for your parachain. This process may take some time. You'll see log messages indicating when your parachain starts participating in block production

Congratulations! You've successfully deployed your parachain on the Paseo TestNet. You can now test and iterate on your blockchain project within the Paseo ecosystem.