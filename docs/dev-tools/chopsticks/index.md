---
title: Using chopsticks for Substrate based chains.
description: Configure and fork Substrate-based blockchains locally with Chopsticks. Learn installation, configuration, and usage for streamlined blockchain development.
---

# Chopsticks

## Introduction

[Chopsticks](https://github.com/AcalaNetwork/chopsticks/){target=_blank} is a powerful tool designed to enhance the development process for Substrate-based blockchains. It offers developers a user-friendly method to locally fork existing chains, enabling them to:

- Replay blocks and analyze how extrinsics affect state
- Fork multiple blocks for comprehensive XCM testing
- Experiment with custom blockchain configurations in a local environment

With Chopsticks, developers can simulate and test complex blockchain scenarios without deploying to a live network. This tool significantly reduces the complexity of building blockchain applications on Substrate, making it more accessible to developers of varying experience levels. Ultimately, Chopsticks aims to accelerate innovation in the Substrate ecosystem by providing a robust, flexible testing framework.

!!!note
    Chopsticks currently does not support Ethereum JSON-RPC calls, so you cannot use it to fork your chain and connect Metamask.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/en/){target=_blank}
- Package manager - [npm](https://www.npmjs.com/){target=_blank} should be installed with Node.js by default. Alternatively, you can use other package managers like [Yarn](https://yarnpkg.com/){target=_blank}

## Getting Started

You can install Chopsticks either globally or locally in your project. Choose the option that best fits your development workflow.

### Global Installation

To install Chopsticks globally, allowing you to use it across multiple projects, run:

```bash
npm i -g @acala-network/chopsticks@latest
```

Now you should be able to run the `chopsticks` command from your terminal.

### Local Installation

To use Chopsticks in a specific project, first create a new directory and initialize a Node.js project:

```bash
mkdir my-chopsticks-project
cd my-chopsticks-project
npm init -y
```

Then, install Chopsticks as a local dependency:

```bash
npm i @acala-network/chopsticks@latest
```

Finally, you can run Chopsticks using the `npx` command:

```bash
npx @acala-network/chopsticks@latest
```

## Configuration

To run Chopsticks, you need to configure some parameters. This can be set either through using a configuration file or the command line interface (CLI).

### Using a Configuration File

The Chopsticks source repository includes a collection of [YAML](https://yaml.org/) files that can be used to set up various Substrate chains locally. You can download these configuration files from the [repository's `configs` folder](https://github.com/AcalaNetwork/chopsticks/tree/master/configs).

An example of a configuration file for Moonbeam is as follows:

```yaml
endpoint: wss://wss.api.moonbeam.network
mock-signature-host: true
db: ./db.sqlite

import-storage:
  System:
    Account:
      -
        -
          - "0xf24FF3a9CF04c71Dbc94D0b566f7A27B94566cac"
        - data:
            free: "100000000000000000000000"
  TechCommitteeCollective:
    Members: ["0xf24FF3a9CF04c71Dbc94D0b566f7A27B94566cac"]
  CouncilCollective:
    Members: ["0xf24FF3a9CF04c71Dbc94D0b566f7A27B94566cac"]
  TreasuryCouncilCollective:
    Members: ["0xf24FF3a9CF04c71Dbc94D0b566f7A27B94566cac"]
  AuthorFilter:
    EligibleRatio: 100
    EligibleCount: 100
```

This file can include the following settings:

|           Option           |                                                 Description                                                  |
| :------------------------: | :----------------------------------------------------------------------------------------------------------: |
|         `genesis`          |          The link to a parachain's raw genesis file to build the fork from, instead of an endpoint.          |
|        `timestamp`         |                                     Timestamp of the block to fork from.                                     |
|         `endpoint`         |                                    The endpoint of the parachain to fork.                                    |
|          `block`           |                       Use to specify at which block hash or number to replay the fork.                       |
|      `wasm-override`       |             Path of the WASM to use as the parachain runtime, instead of an endpoint's runtime.              |
|            `db`            |               Path to the name of the file that stores or will store the parachain's database.               |
|          `config`          |                                       Path or URL of the config file.                                        |
|           `port`           |                                      The port to expose an endpoint on.                                      |
|     `build-block-mode`     |                       How blocks should be built in the fork: batch, manual, instant.                        |
|      `import-storage`      |              A pre-defined JSON/YAML storage file path to override in the parachain's storage.               |
| `allow-unresolved-imports` |              Whether to allow WASM unresolved imports when using a WASM to build the parachain.              |
|           `html`           |                           Include to generate storage diff preview between blocks.                           |
|   `mock-signature-host`    | Mock signature host so that any signature starts with `0xdeadbeef` and filled by `0xcd` is considered valid. |

For the `--config` flag, you can use a raw GitHub URL of the default configuration files, a path to a local configuration file, or simply the chain's name. For example, the following commands all use Moonbeam's configuration in the same way:

=== "Chain Name"

    ```bash
    npx @acala-network/chopsticks@latest --config=moonbeam
    ```

=== "GitHub URL"

    ```bash
    npx @acala-network/chopsticks@latest \
    --config=https://raw.githubusercontent.com/AcalaNetwork/chopsticks/master/configs/moonbeam.yml
    ```

=== "Local File Path"

    ```bash
    npx @acala-network/chopsticks@latest --config=configs/moonbeam.yml
    ```

!!! note
    If using a file path, make sure you've downloaded the [Moonbeam configuration file](https://github.com/AcalaNetwork/chopsticks/blob/master/configs/moonbeam.yml){target=_blank}, or have created your own.

### Using Command Line Interface (CLI)

Alternatively, all settings (except for genesis and timestamp) can be configured via command-line flags, providing a comprehensive method to set up the environment. For example, the following command forks Moonbase Alpha at block 100.

```bash
npx @acala-network/chopsticks@latest --endpoint wss://wss.api.moonbase.moonbeam.network --block 100
```

## WebSocket Commands

Chopstick's internal WebSocket server has special endpoints that allow the manipulation of the local Substrate chain.

These are the methods that can be invoked and their parameters:

???+ function "**dev_newBlock** (newBlockParams) — Generates one or more new blocks"

    === "Parameters"

        |            Name            |                         Type                        | Description |
        | :------------------------: | :-------------------------------------------------: | :---------: |
        | `count`| number | The number of blocks to build|
        | `dmp`| { msg: 0x${string} ; sentAt: number }[] | The downward messages to include in the block|
        | `hrmp` | Record < string \| number, { data: 0x${string} ; sentAt: number }[] > |The horizontal messages to include in the block|
        | `to` | number | The block number to build to|
        | `transactions` | 0x${string}[] |The transactions to include in the block|
        | `ump` | Record < number, 0x${string}[] > | The upward messages to include in the block|
        | `unsafeBlockHeight` | number | Build block using a specific block height (unsafe)|

    === "Example"

        ```js
        import { ApiPromise, WsProvider } from '@polkadot/api';
        async function main() {
          const wsProvider = new WsProvider('ws://localhost:8000');
          const api = await ApiPromise.create({ provider: wsProvider });
          await api.rpc('dev_newBlock',{ count:1 })
        }
        main()
        ```

??? function "**dev_setBlockBuildMode** (buildBlockMode) — Sets block build mode"

    === "Parameter"

        |            Name            |                         Type                        | Description |
        | :------------------------: | :-------------------------------------------------: | :---------: |
        | `buildBlockMode`| "Batch" \| "Instant" \| "Manual" | Build mode|

    === "Example"

        ```js
        import { ApiPromise, WsProvider } from '@polkadot/api';
        async function main() {
          const wsProvider = new WsProvider('ws://localhost:8000');
          const api = await ApiPromise.create({ provider: wsProvider });
          await api.rpc('dev_setBlockBuildMode', "Instant")
        }
        main()
        ```

??? function "**dev_setHead** (hashOrNumber) — Sets the head of the blockchain to a specific hash or number"

    === "Parameter"      

        |            Name            |                         Type                        | Description |
        | :------------------------: | :-------------------------------------------------: | :---------: |
        | hashOrNumber | number \| 0x${string}| The block hash or number to set as head|

    === "Example"

        ```js
        import { ApiPromise, WsProvider } from '@polkadot/api';
        async function main() {
          const wsProvider = new WsProvider('ws://localhost:8000');
          const api = await ApiPromise.create({ provider: wsProvider });
          await api.rpc('dev_setHead', 500)
        }
        main()
        ```

??? function "**dev_setRuntimeLogLevel** (runtimeLogLevel) — Sets the runtime log level"

    === "Parameter"

        |            Name            |                         Type                        | Description |
        | :------------------------: | :-------------------------------------------------: | :---------: |
        |runtimeLogLevel | number | The runtime log level to set|

    === "Example"

        ```js
        import { ApiPromise, WsProvider } from '@polkadot/api';
        async function main() {
          const wsProvider = new WsProvider('ws://localhost:8000');
          const api = await ApiPromise.create({ provider: wsProvider });
          await api.rpc('dev_setRuntimeLogLevel', 1)
        }
        main()
        ```

??? function "**dev_setStorage** (values, blockHash) — Creates or overwrites the value of any storage"

    === "Parameters"

        |            Name            |                         Type                        | Description |
        | :------------------------: | :-------------------------------------------------: | :---------: |
        |values| Object | JSON object resembling the path to a storage value |
        |blockHash| 0x${string} | The block hash to set the storage value |

    === "Example"

        ```js
        import { ApiPromise, WsProvider } from '@polkadot/api';
        import { Keyring } from '@polkadot/keyring'
        async function main() {
            const wsProvider = new WsProvider('ws://localhost:8000');
            const api = await ApiPromise.create({ provider: wsProvider });
            const keyring = new Keyring({ type: 'ed25519' })
            const bob = keyring.addFromUri('//Bob')
            const storage = {
              System: {
                Account: [[[bob.address], { data: { free: 100000 }, nonce: 1 }]],
              },
            }
            await api.rpc('dev_setStorage', storage)
          }
        main()

        ```

??? function "**dev_timeTravel** (date) — Sets the timestamp of the block to a specific date"

    === "Parameter"
        
        |            Name            |                         Type                        | Description |
        | :------------------------: | :-------------------------------------------------: | :---------: |
        |date | string \| number | Timestamp or date string to set. All future blocks will be sequentially created after this point in time |

    === "Example"

        ```js
        import { ApiPromise, WsProvider } from '@polkadot/api';
        async function main() {
          const wsProvider = new WsProvider('ws://localhost:8000');
          const api = await ApiPromise.create({ provider: wsProvider });
          await api.rpc('dev_timeTravel', "2030-08-15T00:00:00")
        }
        main()
        ```

## Tutorials

//TODO

- [Testing runtime upgrades using Chopsticks](./tutorials/chopsticks-runtime-upgrades.md)
- [Chopsticks and XCM](./tutorials//chopsticks-xcm.md)
- [Track governance proposals through Chopsticks](./tutorials/chopsticks-open-gov.md)