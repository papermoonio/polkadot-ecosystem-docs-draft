---
title: Zombienet for Ephemeral Polkadot-SDK Networks
description: Diving deeper into Zombienet, a versatile tool enabling the creation of temporary substrate networks for testing purposes.
---

# Zombienet

## Introduction
Zombienet is a testing framework designed for Polkadot-SDK based blockchains. It provides a simple CLI tool for creating and testing blockchain environments locally or across networks. This allows developers to easily run blockchain nodes and interact with them in a controlled environment. Zombienet supports various backend providers, including Kubernetes, Podman, and native setups for running blockchain nodes. 

The framework enables developers to create tests using natural language tools to verify on-chain storage, metrics, logs, and custom interactions with the blockchain. It is particularly effective for setting up local relaychains with validators and parachains with collators.

[Parity Technologies](https://www.parity.io/){target=_blank} has designed and developed this framework, now maintained by the Zombienet team. For further support and information, refer to the following contact points:
    
- [Zombienet repository](https://github.com/paritytech/zombienet){target=_blank}
- [Element public channel](https://matrix.to/#/!FWyuEyNvIFygLnWNMh:parity.io?via=parity.io&via=matrix.org&via=web3.foundation){target=_blank}

## Installation

Zombienet releases can be found on the [Zombienet repository]( https://github.com/paritytech/zombienet ){target=_blank}.

In order to install Zombienet, there are multiple options available, depending on the user's preferences and the environment where it will be used. The following section will guide you through the installation process for each of the available options.

=== "Using the Executable" 

    Zombienet executables can be downloaded using the latest release uploaded on the [Zombienet repository]( https://github.com/paritytech/zombienet/releases ){target=_blank}. You can download the executable for your operating system and architecture and then move it to a directory in your PATH. Each release includes executables for Linux and Macos, which are generated using [pkg]( https://github.com/vercel/pkg ){target=_blank}. This allows the Zombienet CLI to operate without requiring Node.js to be installed. 

    Alternatively, you can also download the executable using either `curl` or `wget`:

    === "curl"
        ```bash
        curl -LO \
        https://github.com/paritytech/zombienet/releases/download/<INSERT_ZOMBIENET_VERSION>/<INSERT_ZOMBIENET_EXECUTABLE>
        ``` 
    === "wget"
        ```bash
        wget \
        https://github.com/paritytech/zombienet/releases/download/<INSERT_ZOMBIENET_VERSION>/<INSERT_ZOMBIENET_EXECUTABLE>
        ```
    !!! note
        Ensure to replace the URL with the `<INSERT_ZOMBIENET_VERSION>` that you want to download, as well as the `<INSERT_ZOMBIENET_EXECUTABLE>` with the name of the executable file that matches your operating system and architecture. This guide uses `v1.3.106` and `zombienet-macos-arm64`.

    Then, ensure the downloaded file executable:

    ```bash
    chmod +x zombienet-macos-arm64
    ```

    Finally, you can run the following command to check if the installation was successful, if so, it will display the version of the installed Zombienet:

    ```bash
    ./zombienet-macos-arm64 version
    ```

    !!! note
        If you want to add the `zombienet` executable to your PATH, you can move it to a directory in your PATH, such as `/usr/local/bin`:
        ```bash
        mv zombienet-macos-arm64 /usr/local/bin/zombienet
        ```

=== "Using Nix"

    For Nix users, the Zombienet repository provides a [`flake.nix`](https://github.com/paritytech/zombienet/blob/main/flake.nix){target=_blank} file that can be used to install Zombienet. This means that users can easily incorporate Zombienet into their Nix-based projects. 
    
    To install Zombienet utilizing Nix, users can run the following command, triggering the fetching of the flake and subsequently installing the Zombienet package:

    ```bash
    nix run github:paritytech/zombienet/<INSERT_ZOMBIENET_VERSION> -- \
    spawn <INSERT_ZOMBIENET_CONFIG_FILE_NAME>.toml
    ```

    !!! Warning
        To run the command above, you need to have [nix flakes enabled](https://nixos.wiki/wiki/Flakes#Enable_flakes){target=_blank}.

    Alternatively, you can also include the zombienet binary in the PATH for the current shell. This can be achieved by:
    
    ```bash
    nix shell github:paritytech/zombienet/<INSERT_ZOMBIENET_VERSION>
    ```

    !!! note
        Ensure to replace the `<INSERT_ZOMBIENET_VERSION>` with the desired version of Zombienet. Also, replace the `<INSERT_ZOMBIENET_CONFIG_FILE_NAME>` with the name of the configuration file you want to use.

=== "Using Docker"

    Zombienet can also be run using Docker. The Zombienet repository provides a Docker image that can be used to run the Zombienet CLI. To run Zombienet using Docker, you can use the following command:

    ```bash
    docker run -it --rm \
    -v $(pwd):/home/nonroot/zombie-net/host-current-files \
    paritytech/zombienet
    ```
    !!! note
        Command above will run the Zombienet CLI inside a Docker container and mount the current directory to the `/home/nonroot/zombie-net/host-current-files` directory inside the container. This allows Zombienet to access the configuration file and other files in the current directory. If you want to mount a different directory, replace `$(pwd)` with the desired directory path.

    Now, inside the Docker container, you can run the Zombienet CLI commands. First, you need to set up ZombieNet downloading the neccessary binaries:

    ```bash
    npm run zombie -- setup polkadot polkadot-parachain
    ```

    After that, you need to add those binaries to the PATH:

    ```bash
    export PATH=/home/nonroot/zombie-net:$PATH
    ```

    Finally, you can run the Zombienet CLI commands. For example, to spawn a network using a specific configuration file, you can run the following command:

    ```bash
    npm run zombie -- -p native spawn host-current-files/minimal.toml
    ```

    !!! warning
        The command above mounts the current directory to the `/workspace` directory inside the Docker container. This allows Zombienet to access the configuration file and other files in the current directory. If you want to mount a different directory, replace `$(pwd)` with the desired directory path.


## Providers

Zombienet is a JavaScript library designed to run on Node.js and support different backend providers to run the nodes. At this moment [Kubernetes]( https://kubernetes.io/ ){target=_blank}, [Podman]( https://podman.io/ ){target=_blank} and, native are supported.

It's important to note that each provider has specific requirements and associated features. The subsequent sections will guide you through the installation process for each provider and the requirements and features each provider offers.

### Kubernetes

=== "Requirements"

    Zombienet is designed to be compatible with a variety of Kubernetes clusters, including [Google Kubernets Engine (GKE)](https://cloud.google.com/kubernetes-engine){target=_blank}, [Docker Desktop](https://docs.docker.com/desktop/kubernetes/){target=_blank}, and [kind](https://kind.sigs.k8s.io/){target=_blank}. To effectively interact with your cluster, you'll need to ensure that [`kubectl`](https://kubernetes.io/docs/reference/kubectl/) is installed on your system, which is the Kubernetes command-line tool that allows you to run commands against Kubernetes clusters.

    Moreover, in order to create resources such as namespaces, pods, and cronJobs within the target cluster, you must have the appropriate permissions granted to your user or service account. These permissions are essential for managing and deploying applications effectively within Kubernetes.

=== "Features"
    In Kubernetes, Zombienet uses the Prometheus operator (if available) to oversee monitoring and visibility. This configuration ensures that only essential networking-related pods are deployed. By using the Prometheus operator, Zombienet improves its capability to efficiently monitor and manage network activities within the Kubernetes cluster.

### Podman

=== "Requirements"

    Zombienet supports Podman rootless as a provider. To use it, you simply need to have Podman installed on your system and specify it either in the network file or using the `--provider` flag in the CLI.

    !!! note
        Currently, Podman can only be used with Zombienet on Linux machines. Although Podman has support for macOS through an internal VM, the Zombienet provider code requires Podman to run natively on Linux.

=== "Features"
    
    Using Podman, Zombienet deploys additional pods to enhance the monitoring and visibility of the active network. Specifically, pods for Prometheus, Tempo, and Grafana are included in the deployment. Grafana is configured with Prometheus and Tempo as datasources.

    Upon launching Zombienet, access to these monitoring services is facilitated through specific URLs provided in the output:

    - Prometheus - [http://127.0.0.1:34123](http://127.0.0.1:34123){target=_blank}
    - Tempo - [http://127.0.0.1:34125](http://127.0.0.1:34125){target=_blank}
    - Grafana - [http://127.0.0.1:41461](http://127.0.0.1:41461){target=_blank}

    It's important to note that Grafana is deployed with default admin access.

    !!! note
        When the network operations cease—either by halting a running spawn with Ctrl+C or upon completion of the test—all associated pods, including those for Prometheus, Tempo, and Grafana, are automatically removed by Zombienet.

### Native

=== "Requirements"
    
    The Zombienet Native provider enables you to run nodes as local processes in your environments. You simply need to have the necessary binaries for your network (such as `polkadot` and `polkadot-parachain`). You can choose to set it up by configuring your network file or using the `--provider` flag in the CLI.

    !!! note
        The native provider exclusively utilizes the command config for nodes/collators, which supports both relative and absolute paths. You can employ the `default_command` config to specify the binary for spawning all nodes in the relaychain.

=== "Features"
    Currently, the Native provider does not execute any additional layers or processes.

## CLI Usage

Zombienet provides a CLI that allows interaction with the tool. The CLI can receive commands and flags to perform different kinds of operations. The following tables will guide you through the primary usage of the Zombienet CLI and the available commands and flags.

|  Command  |                                            Description                                             |                                                                                                                                                      Arguments                                                                                                                                                       |
| :-------: | :------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|  `spawn`  |                            Spawn the network defined in the config file                            |                                                            `<networkConfig>` - a file that declares the desired network to be spawned in `toml` or `json` format. For further information, check out [Configuration Files](#configuration-files) section                                                            |
|  `test`   |                                  Run test on the network spawned                                   |                                                                      `<testFile>` - a file that defines assertions and tests against the spawned network, using natural language expressions to evaluate metrics, logs, and built-in functions                                                                      |
|  `setup`  |                           Set up the dev environment of Zombienet ready.                           |                                                                                         `<binaries>` - executables that will be downloaded and prepared to be used by Zombienet. Options: `polkadot`, `polkadot-parachain`                                                                                          |
| `convert` | Transforms a (now deprecated) polkadot-launch configuration file to a zombienet configuration file | `<filePath>` - path to a [Polkadot Launch](https://github.com/paritytech/polkadot-launch){target=_blank} configuration file with a .js or .json extension defined by [this structure](https://github.com/paritytech/polkadot-launch/blob/295a6870dd363b0b0108e745887f51e7141d7b5f/src/types.d.ts#L10){target=_blank} |
| `version` |                                      Prints zombienet version                                      |                                                                                                                                                          -                                                                                                                                                           |
|  `help`   |                                      Prints help information                                       |                                                                                                                                                          -                                                                                                                                                           |


!!! warning
    For the `spawn` command to work on macOS, users need to be aware that the Polkadot binary is currently not compatible with macOS. As a result, macOS users will need to clone the [Polkadot repository](https://github.com/paritytech/polkadot-sdk){target=_blank}, build Polkadot binary, and manually add it to their PATH.

Then, you can use the following flags to customize the behavior of the CLI:

|                   Flag                    |                                                Description                                                |
| :---------------------------------------: | :-------------------------------------------------------------------------------------------------------: |
|            `-p`, `--provider`             |  Override provider to use (choices: `podman`, `default`, and, `native`). By default it uses `kubernetes`  |
|           `-d`, `--dir` <path>            | Directory path for placing the network files instead of random temp one (e.g. -d /home/user/my-zombienet) |
|              `-f`, `--force`              |                                    Force override all prompt commands                                     |
|        `-l`, `--logType` <logType>        |   Type of logging on the console (choices: `table`, `text`, and, `silent`). By default it uses `table`    |
|             `-m`, `--monitor`             |                              Start as monitor, do not auto clean up network                               |
| `-c`, `--spawn-concurrency` <concurrency> |                   Number of concurrent spawning process to launch. By default it is `1`                   |
|              `-h`, `--help`               |                                         Display help for command                                          |


## Configuration Files 

The network configuration can be given in either `json` or `toml` format. Zombienet repository also provides a [folder with some examples](https://github.com/paritytech/zombienet/tree/main/examples){target=_blank} of configuration files that can be used as a reference.

!!! note
    Each section may include provider-specific keys that are not recognized by other providers. For example, if you use the native provider, any references to images for nodes will be disregarded.

### Settings

Through the keyword `settings`, it's possible to define the general settings for the network. The following keys are available:

|                 Key                  |  Type   | Description                                                                                               | Default Value                            |
| :----------------------------------: | :-----: | :-------------------------------------------------------------------------------------------------------- | :--------------------------------------- |
|              `bootnode`              | Boolean | Add bootnode to network                                                                                   | `true`                                   |
|              `timeout`               | Number  | Global timeout to use for spawning the whole network                                                      | -                                        |
|              `provider`              | String  | Provider to use (e.g., kubernetes, podman)                                                                | kubernetes                               |
|            `backchannel`             | Boolean | Deploy an instance of backchannel server. Only available on kubernetes                                    | `false`                                  |
|       `polkadot_introspector`        | Boolean | Deploy an instance of polkadot-introspector. Only available on podman and kubernetes                      | `false`                                  |
|            `jaeger_agent`            | String  | The Jaeger agent endpoint passed to the nodes. Only available on kubernetes                               | -                                        |
|           `enable_tracing`           | Boolean | Enable the tracing system. Only available on kubernetes                                                   | `true`                                   |
|        `tracing_collator_url`        | String  | The URL of the tracing collator used to query by the tracing assertion (Should be tempo query compatible) | -                                        |
|   `tracing_collator_service_name`    | String  | Service name for tempo query frontend. Only available on kubernetes                                       | `tempo-tempo-distributed-query-frontend` |
| `tracing_collator_service_namespace` | String  | Namespace where tempo is running. Only available on kubernetes                                            | `tempo`                                  |
|   `tracing_collator_service_port`    | Number  | Port of the query instance of tempo. Only available on kubernetes                                         | `3100`                                   |
|         `node_spawn_timeout`         | Number  | Timeout to spawn pod/process                                                                              | `per provider`                           |
|              `local_ip`              | String  | IP used for exposing local services (rpc/metrics/monitors)                                                | `"127.0.0.1"`                            |
|           `node_verifier`            | String  | Allow managing how to verify node readiness or disable (None)                  | `Metric`                                 |

For example, the following configuration file defines a minimal example for the settings:

=== "base-example.toml"
    ```toml
    [settings]
    timeout = 1000
    bootnode = false
    provider = "kubernetes"
    backchannel = false
    ...
    ```

=== "base-example.json"
    ```json
    {
        "settings": {
            "timeout": 1000,
            "bootnode": false,
            "provider": "kubernetes",
            "backchannel": false,
            ...
        },
        ...
    }
    ```

### Relaychain

The `relaychain` keyword is used to define further parameters for the relaychain. The following keys are available:

|                 Key                  |       Type        | Description                                                                                                      | Default Value  |
| :----------------------------------: | :---------------: | :--------------------------------------------------------------------------------------------------------------- | :------------- |
|          `default_command`           |      String       | The default command to run                                                                                       | `polkadot`     |
|               `chain`                |      String       | The chain name                                                                                                   | `rococo-local` |
|          `chain_spec_path`           |      String       | Path to the chain spec file. It should be the plain version to allow customizations                              | -              |
|         `chain_spec_command`         |      String       | Command to generate the chain spec. It can't be used in combination with `chain_spec_path`                       | -              |
|            `default_args`            | Array of strings  | An array of arguments to use as default to pass to the command                                                   | -              |
| `default_substrate_cli_args_version` |    0 \| 1 \| 2    | Set the substrate cli args version                                                                               | -              |
|         `default_overrides`          | Array of objects  | An array of overrides to upload to the nodes                                                                     | -              |
|         `default_resources`          |      Object       | Only available in kubernetes, represent the resources limits/reservations needed by the nodes by default         | -              |
|     `default_prometheus_prefix`      |      String       | A parameter for customizing the metric's prefix                                                                  | `substrate`    |
|      `random_nominators_count`       | Number (optional) | If set and the stacking pallet is enabled, Zombienet will generate x nominators and inject them into the genesis | -              |
|          `max_nominations`           |      Number       | The max allowed number of nominations by a nominator. Should match the value set in the runtime                  | `24`           |

??? Nodes
    There is one specific key capable of receiving more subkeys: the `nodes` key. This key is used to define further parameters for the nodes. The following keys are available:

    | Key                          | Type             | Description                                                                                      | Default Value   |
    | :--------------------------- | :--------------- | :----------------------------------------------------------------------------------------------- | :-------------- |
    | `name`                       | String           | Name of the node. Any whitespace will be replaced with a dash (e.g., 'new alice' -> 'new-alice') | -               |
    | `image`                      | String           | Override default Docker image to use for this node                                               | -               |
    | `command`                    | String           | Override default command to run                                                                  | -               |
    | `command_with_args`          | String           | Override default command and arguments                                                           | -               |
    | `args`                       | Array of strings | Arguments to be passed to the command                                                            | -               |
    | `substrate_cli_args_version` | 0 \| 1 \| 2      | Set the Substrate CLI args version directly to skip binary evaluation overhead                   | -               |
    | `validator`                  | Boolean          | Pass the --validator flag to the command                                                         | `true`          |
    | `invulnerable`               | Boolean          | If true, add the node to invulnerables in the chain spec                                         | `false`         |
    | `balance`                    | Number           | Balance to set in balances for node's account                                                    | `2000000000000` |
    | `env`                        | Array of objects | Environment variables to set in the container                                                    | -               |
    | `env.name`                   | String           | Name of the environment variable                                                                 | -               |
    | `env.value`                  | String \| Number | Value of the environment variable                                                                | -               |
    | `bootnodes`                  | Array of strings | Array of bootnodes to use                                                                        | -               |
    | `overrides`                  | Array of objects | Array of overrides definitions                                                                   | -               |
    | `add_to_bootnodes`           | Boolean          | Add this node to the bootnode list                                                               | `false`         |
    | `resources`                  | Object           | Kubernetes-specific: represent the resources limits/reservations needed by the node              | -               |
    | `ws_port`                    | Number           | WS port to use                                                                                   | -               |
    | `rpc_port`                   | Number           | RPC port to use                                                                                  | -               |
    | `prometheus_port`            | Number           | Prometheus port to use                                                                           | -               |
    | `prometheus_prefix`          | String           | Customizing the metric's prefix for the specific node                                            | `substrate`     |
    | `keystore_key_types`         | String           | Defines which keystore keys should be created                                                    | -               |

    So, for example, the following configuration file defines a minimal example for the relaychain, including the `nodes` key:

    === "relaychain-example-nodes.toml"
        ```toml
        [relaychain]
        default_command = "polkadot"
        default_image = "polkadot-debug:master"
        chain = "rococo-local"
        chain_spec_path = "/path/to/chain-spec.json"
        default_args = ["--chain", "rococo-local"]

        [[relaychain.nodes]]
        name = "alice"
        validator = true
        balance = 1000000000000

        [[relaychain.nodes]]
        name = "bob"
        validator = true
        balance = 1000000000000
        ...
        ```

    === "relaychain-example-nodes.json"
        ```json
        {
            ...,
            "relaychain": {
                "default_command": "polkadot",
                "default_image": "polkadot-debug:master",
                "chain": "rococo-local",
                "chain_spec_path": "/path/to/chain-spec.json",
                "default_args": ["--chain", "rococo-local"],
                "nodes": [
                    {
                        "name": "alice",
                        "validator": true,
                        "balance": 1000000000000
                    },
                    {
                        "name": "bob",
                        "validator": true,
                        "balance": 1000000000000
                    }
                ],
                ...
            },
            ...
        }
        ```

??? "Node Groups"
    The `node_groups` key is used to define further parameters for the node groups. The following keys are available:

    | Key                          | Type             | Description                                                                                                                            | Default Value |
    | :--------------------------- | :--------------- | :------------------------------------------------------------------------------------------------------------------------------------- | :------------ |
    | `name`                       | String           | Group name, used for naming the nodes (e.g., `name-1`). Any whitespace will be replaced with a dash (e.g., 'new group' -> 'new-group') | -             |
    | `count`                      | Number           | Number of nodes to launch for this group                                                                                               | -             |
    | `image`                      | String           | Override default Docker image to use for this node                                                                                     | -             |
    | `command`                    | String           | Override default command to run.                                                                                                       | -             |
    | `args`                       | Array of strings | Arguments to be passed to the command                                                                                                  | -             |
    | `env`                        | Array of objects | Environment variables to set in the container                                                                                          | -             |
    | `env.name`                   | String           | Name of the environment variable                                                                                                       | -             |
    | `env.value`                  | String \| Number | Value of the environment variable                                                                                                      | -             |
    | `overrides`                  | Array of objects | Array of overrides definitions                                                                                                         | -             |
    | `prometheus_prefix`          | String           | A parameter for customizing the metric's prefix for the specific node group                                                            | `substrate`   |
    | `resources`                  | Object           | Kubernetes-specific: represent the resources limits/reservations needed by the node                                                    | -             |
    | `substrate_cli_args_version` | 0 \| 1 \| 2      | Set the Substrate CLI args version directly to skip binary evaluation overhead                                                         | -             |

    So, for example, the following configuration file defines a minimal example for the relaychain, including the `node_groups` key:
    
    === "relaychain-example-node-groups.toml"
        ```toml
        [relaychain]
        default_command = "polkadot"
        default_image = "polkadot-debug:master"
        chain = "rococo-local"
        chain_spec_path = "/path/to/chain-spec.json"
        default_args = ["--chain", "rococo-local"]

        [[relaychain.node_groups]]
        name = "group-1"
        count = 2
        image = "polkadot-debug:master"
        command = "polkadot"
        args = ["--chain", "rococo-local"]
        ...
        ```

    === "relaychain-example-node-groups.json"
        ```json
        {
            ...,
            "relaychain": {
                "default_command": "polkadot",
                "default_image": "polkadot-debug:master",
                "chain": "rococo-local",
                "chain_spec_path": "/path/to/chain-spec.json",
                "default_args": ["--chain", "rococo-local"],
                "node_groups": [
                    {
                        "name": "group-1",
                        "count": 2,
                        "image": "polkadot-debug:master",
                        "command": "polkadot",
                        "args": ["--chain", "rococo-local"]
                    }
                ],
                ...
            },
            ...
        }
        ```

### Parachain

The `parachain` keyword is used to define further parameters for the parachain. The following keys are available:

| Key                       | Type    | Description                                                                                                                            | Default Value |
| :------------------------ | :------ | :------------------------------------------------------------------------------------------------------------------------------------- | :------------ |
| `id`                      | Number  | The id to assign to this parachain. Must be unique                                                                                     | -             |
| `add_to_genesis`          | Boolean | Flag to add parachain to genesis or register in runtime                                                                                | `true`        |
| `cumulus_based`           | Boolean | Flag to use cumulus command generation                                                                                                 | `true`        |
| `genesis_wasm_path`       | String  | Path to the wasm file to use                                                                                                          | -             |
| `genesis_wasm_generator`  | String  | Command to generate the wasm file                                                                                                      | -             |
| `genesis_state_path`      | String  | Path to the state file to use                                                                                                         | -             |
| `genesis_state_generator` | String  | Command to generate the state file                                                                                                     | -             |
| `prometheus_prefix`       | String  | A parameter for customizing the metric's prefix for all parachain nodes/collators                                                      | `substrate`   |
| `onboard_as_parachain`    | Boolean | Flag to specify whether the para should be onboarded as a parachain or stay a parathread                                               | `true`        |
| `register_para`           | Boolean | Flag to specify whether the para should be registered. The `add_to_genesis` flag must be set to false for this flag to have any effect | `true`        |

For example, the following configuration file defines a minimal example for the parachain:

=== "parachain-example.toml"
    ```toml
    [parachain]
    id = 100
    add_to_genesis = true
    cumulus_based = true
    genesis_wasm_path = "/path/to/wasm"
    genesis_state_path = "/path/to/state"
    ...
    ```

=== "parachain-example.json"
    ```json
    {
      "parachain": {
        "id": 100,
        "add_to_genesis": true,
        "cumulus_based": true,
        "genesis_wasm_path": "/path/to/wasm",
        "genesis_state_path": "/path/to/state",
        ...
      },
      ...
    }
    ```

??? "Collator"
   
    There is one specific key capable of receiving more subkeys: the `collator` key. This key is used to define further parameters for the nodes. The following keys are available:

    | Key                          | Type             | Description                                                                                                     | Default Value        |
    | ---------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------- | -------------------- |
    | `name`                       | String           | Name of the collator. Any whitespace will be replaced with a dash (e.g., 'new alice' -> 'new-alice')            | -                    |
    | `image`                      | String           | Image to use for the collator                                                                                   | -                    |
    | `command`                    | String           | Command to run for the collator                                                                                 | `polkadot-parachain` |
    | `args`                       | Array of strings | An array of arguments to use as defaults to pass to the command                                                 | -                    |
    | `substrate_cli_args_version` | 0 \| 1           | By default zombienet evaluates the binary and sets the correct version. Set this key directly to skip overhead. | -                    |
    | `command_with_args`          | String           | Overrides both command and arguments for the collator                                                           | -                    |
    | `env`                        | Array of objects | Environment variables to set in the container for the collator                                                  | -                    |
    | `env.name`                   | String           | Name of the environment variable                                                                                | -                    |
    | `env.value`                  | String \| Number | Value of the environment variable                                                                               | -                    |
    | `keystore_key_types`         | String           | Defines which keystore keys should be created. For more details, refer to additional documentation              | -                    |

    For example, the following configuration file defines a minimal example for the collator:

    === "collator-example.toml"
        ```toml
        [parachain]
        id = 100
        add_to_genesis = true
        cumulus_based = true
        genesis_wasm_path = "/path/to/wasm"
        genesis_state_path = "/path/to/state"

        [[parachain.collators]]
        name = "alice"
        image = "polkadot-parachain"
        command = "polkadot-parachain"
        ...
        ```

    === "collator-example.json"
        ```json
        {
          "parachain": {
            "id": 100,
            "add_to_genesis": true,
            "cumulus_based": true,
            "genesis_wasm_path": "/path/to/wasm",
            "genesis_state_path": "/path/to/state",
            "collators": [
              {
                "name": "alice",
                "image": "polkadot-parachain",
                "command": "polkadot-parachain",
                ...
              },
            ],
          },
          ...
        }
        ```

??? "Collator Groups"
   
    The `collator_groups` key is used to define further parameters for the collator groups. The following keys are available:

    | Key                          | Type             | Description                                                                                                     | Default Value        |
    | ---------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------- | -------------------- |
    | `name`                       | String           | Name of the collator. Any whitespace will be replaced with a dash (e.g., 'new alice' -> 'new-alice')            | -                    |
    | `count`                      | Number           | Number of collators to launch for this group                                                                    | -                    |
    | `image`                      | String           | Image to use for the collators                                                                                  | -                    |
    | `command`                    | String           | Command to run for each collator                                                                                | `polkadot-parachain` |
    | `args`                       | Array of strings | An array of arguments to use as defaults to pass to the command                                                 | -                    |
    | `command_with_args`          | String           | Overrides both command and arguments for each collator                                                          | -                    |
    | `env`                        | Array of objects | Environment variables to set in the container for each collator                                                 | -                    |
    | `env.name`                   | String           | Name of the environment variable                                                                                | -                    |
    | `env.value`                  | String \| Number | Value of the environment variable                                                                               | -                    |
    | `substrate_cli_args_version` | 0 \| 1 \| 2      | By default zombienet evaluates the binary and sets the correct version. Set this key directly to skip overhead | -                    |

    For example, the following configuration file defines a minimal example for the collator groups:

    === "collator-groups-example.toml"
        ```toml
        [parachain]
        id = 100
        add_to_genesis = true
        cumulus_based = true
        genesis_wasm_path = "/path/to/wasm"
        genesis_state_path = "/path/to/state"

        [[parachain.collator_groups]]
        name = "group-1"
        count = 2
        image = "polkadot-parachain"
        command = "polkadot-parachain"
        ...
        ```
    
    === "collator-groups-example.json"
        ```json
        {
          "parachain": {
            "id": 100,
            "add_to_genesis": true,
            "cumulus_based": true,
            "genesis_wasm_path": "/path/to/wasm",
            "genesis_state_path": "/path/to/state",
            "collator_groups": [
              {
                "name": "group-1",
                "count": 2,
                "image": "polkadot-parachain",
                "command": "polkadot-parachain",
                ...
              },
            ],
          },
          ...
        }
        ```

### HRMP Channels

The `hrmp_channels` keyword is used to define further parameters for the HRMP channels. The following keys are available:

| Key                | Type             | Description                                      |
| ------------------ | ---------------- | ------------------------------------------------ |
| `hrmp_channels`    | Array of objects | Array of HRMP channel configurations             |
| `sender`           | Number           | Parachain ID of the sender                       |
| `recipient`        | Number           | Parachain ID of the recipient                    |
| `max_capacity`     | Number           | Maximum capacity of the HRMP channel             |
| `max_message_size` | Number           | Maximum message size allowed in the HRMP channel |

