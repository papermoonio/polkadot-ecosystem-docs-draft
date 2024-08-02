---
title: Zombienet for Ephemeral Polkadot SDK Networks
description: Diving deeper into Zombienet, a versatile tool enabling the creation of temporary Substrate networks for testing purposes.
---

# Zombienet

## Introduction

Zombienet is a testing framework designed for Polkadot SDK-based blockchains. It provides a simple CLI tool for creating and testing blockchain environments locally or across networks. This allows developers to easily run and interact with blockchain nodes in a controlled environment. Zombienet is a JavaScript library designed to run on Node.js and supports various backend providers, including Kubernetes, Podman, and local setups for running blockchain nodes. 

The framework enables developers to create tests using natural language tools to verify on-chain storage, metrics, logs, and custom interactions with the blockchain. It is particularly effective for setting up local relaychains with validators and parachains with collators.

[Parity Technologies](https://www.parity.io/){target=_blank} has designed and developed this framework, now maintained by the Zombienet team. For further support and information, refer to the following contact points:
    
- [Zombienet repository](https://github.com/paritytech/zombienet){target=_blank}
- [Element public channel](https://matrix.to/#/!FWyuEyNvIFygLnWNMh:parity.io?via=parity.io&via=matrix.org&via=web3.foundation){target=_blank}

## Installation

Zombienet releases are available on the [Zombienet repository](https://github.com/paritytech/zombienet){target=_blank}.

In order to install Zombienet, there are multiple options available, depending on the user's preferences and the environment where it will be used. The following section will guide you through the installation process for each of the available options.

=== "Using the Executable" 

    Zombienet executables can be downloaded using the latest release uploaded on the [Zombienet repository](https://github.com/paritytech/zombienet/releases){target=_blank}. You can download the executable for your operating system and architecture and then move it to a directory in your PATH. Each release includes executables for Linux and macOS, which are generated using [pkg](https://github.com/vercel/pkg){target=_blank}. This allows the Zombienet CLI to operate without requiring Node.js to be installed. 

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

    Then, ensure the downloaded file is executable:

    ```bash
    chmod +x zombienet-macos-arm64
    ```

    Finally, you can run the following command to check if the installation was successful. If so, it will display the version of the installed Zombienet:

    ```bash
    ./zombienet-macos-arm64 version
    ```

    If you want to add the `zombienet` executable to your PATH, you can move it to a directory in your PATH, such as `/usr/local/bin`:
    ```bash
    mv zombienet-macos-arm64 /usr/local/bin/zombienet
    ```

    So then, you can refer to the `zombienet` executable directly:

    ```bash
    zombienet version
    ```

=== "Using Nix"

    For Nix users, the Zombienet repository provides a [`flake.nix`](https://github.com/paritytech/zombienet/blob/main/flake.nix){target=_blank} file that can be used to install Zombienet. This means that users can easily incorporate Zombienet into their Nix-based projects. 
    
    To install Zombienet utilizing Nix, users can run the following command, triggering the fetching of the flake and subsequently installing the Zombienet package:

    ```bash
    nix run github:paritytech/zombienet/<INSERT_ZOMBIENET_VERSION> -- \
    spawn <INSERT_ZOMBIENET_CONFIG_FILE_NAME>.toml
    ```

    To run the command above, you need to have [Flakes](https://nixos.wiki/wiki/Flakes#Enable_flakes){target=_blank} enabled.

    Alternatively, you can also include the Zombienet binary in the PATH for the current shell. This can be achieved by:
    
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
    The command above will run the Zombienet CLI inside a Docker container and mount the current directory to the `/home/nonroot/zombie-net/host-current-files` directory inside the container. This allows Zombienet to access the configuration file and other files in the current directory. If you want to mount a different directory, replace `$(pwd)` with the desired directory path.

    Inside the Docker container, you can run the Zombienet CLI commands. First, you need to set up Zombienet downloading the necessary binaries:

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

    The command above mounts the current directory to the `/workspace` directory inside the Docker container. This allows Zombienet to access the configuration file and other files in the current directory. If you want to mount a different directory, replace `$(pwd)` with the desired directory path.


## Providers

Zombienet supports different backend providers in running the nodes. At this moment, [Kubernetes](https://kubernetes.io/){target=_blank}, [Podman](https://podman.io/){target=_blank}, and local are supported.

To use a particular provider, you can specify it in the network file or use the `--provider` flag in the CLI:
    
```bash
zombienet spawn network.toml --provider <provider>
```

Alternatively, you can set the provider in the network file:

```toml
[settings]
provider = "<provider>"
...
```

At the moment, Zombienet supports the following providers: `kubernetes`, `podman`, and `native` (local).

It's important to note that each provider has specific requirements and associated features. The subsequent sections will guide you through the installation process for each provider and the requirements and features each provider offers.

### Kubernetes

#### Requirements

Zombienet is designed to be compatible with a variety of Kubernetes clusters, including [Google Kubernets Engine (GKE)](https://cloud.google.com/kubernetes-engine){target=_blank}, [Docker Desktop](https://docs.docker.com/desktop/kubernetes/){target=_blank}, and [kind](https://kind.sigs.k8s.io/){target=_blank}. To effectively interact with your cluster, you'll need to ensure that [`kubectl`](https://kubernetes.io/docs/reference/kubectl/){target=_blank} is installed on your system, which is the Kubernetes command-line tool that allows you to run commands against Kubernetes clusters. If you don't have `kubectl` installed, you can follow the instructions provided on the [Kubernetes website](https://kubernetes.io/docs/tasks/tools/#kubectl){target=_blank}.

Moreover, in order to create resources such as namespaces, pods, and cronJobs within the target cluster, you must have the appropriate permissions granted to your user or service account. These permissions are essential for managing and deploying applications effectively within Kubernetes.

#### Features

In Kubernetes, Zombienet uses the Prometheus operator (if available) to oversee monitoring and visibility. This configuration ensures that only essential networking-related pods are deployed. Using the Prometheus operator, Zombienet improves its ability to efficiently monitor and manage network activities within the Kubernetes cluster. 

### Podman

#### Requirements

Zombienet supports Podman rootless as a provider. To use Podman as a provider, you need to have Podman installed on your system. Podman is a daemonless container engine for developing, managing, and running Open Container Initiative (OCI) containers and container images on Linux-based systems. You can install Podman by following the instructions provided on the [Podman website](https://podman.io/getting-started/installation){target=_blank}.

!!! warning
    Currently, Podman can only be used with Zombienet on Linux machines. Although Podman has support for macOS through an internal VM, the Zombienet provider code requires Podman to run natively on Linux.

#### Features
    
Using Podman, Zombienet deploys additional pods to enhance the monitoring and visibility of the active network. Specifically, pods for [Prometheus](https://prometheus.io/){target=_blank}, [Tempo](https://grafana.com/docs/tempo/latest/operations/monitor/){target=_blank}, and [Grafana](https://grafana.com/){target=_blank} are included in the deployment. Grafana is configured with Prometheus and Tempo as data sources.

Upon launching Zombienet, access to these monitoring services is facilitated through specific URLs provided in the output:

- Prometheus - [http://127.0.0.1:34123](http://127.0.0.1:34123){target=_blank}
- Tempo - [http://127.0.0.1:34125](http://127.0.0.1:34125){target=_blank}
- Grafana - [http://127.0.0.1:41461](http://127.0.0.1:41461){target=_blank}

It's important to note that Grafana is deployed with default admin access.

!!! note
    When network operations cease—either by halting a running spawn with Ctrl+C or upon completion of the test—Zombienet automatically removes all associated pods.

### Local

#### Requirements
    
The Zombienet local provider, also referred to as native, enables you to run nodes as local processes in your environment. You must have the necessary binaries for your network (such as `polkadot` and `polkadot-parachain`). These binaries should be available in your PATH, allowing Zombienet to spawn the nodes as local processes.

To install the necessary binaries, you can use the Zombienet CLI command:

```bash
zombienet setup polkadot polkadot-parachain
```

This command will download and prepare the necessary binaries for Zombienet’s use.

!!! warning 
    The `polkadot` and `polkadot-parachain` binaries releases are not compatible with macOS. As a result, macOS users will need to clone the [Polkadot repository](https://github.com/paritytech/polkadot-sdk){target=_blank}, build the Polkadot binary, and manually add it to their PATH for `polkadot` and `polkadot-parachain` to work.

If you need to use a custom binary, ensure the binary is available in your PATH. You can also specify the binary path in the network configuration file. To showcase this, this guide will use the custom [Open Zeppelin template](https://github.com/OpenZeppelin/polkadot-runtime-templates){target=_blank} as an example.

First, clone the Open Zeppelin template repository:

```bash
git clone https://github.com/OpenZeppelin/polkadot-runtime-templates \
&& cd polkadot-runtime-templates/generic-template

Then, build the custom binary:

```bash
cargo build --release
```

After that, add the custom binary to your PATH:

```bash
export PATH=$PATH:/path/to/polkadot-runtime-templates/parachain-template-node/target/release
```

Alternatively, you can specify the binary path in the network configuration file:

```toml
[relaychain]
chain = "rococo-local"
default_command = "./bin-v1.6.0/polkadot"

[parachain]
id = 1000

	[parachain.collators]
	name = "collator01"
	command = "./target/release/parachain-template-node"
```

!!! note
    The local provider exclusively utilizes the command config for nodes/collators, which supports both relative and absolute paths. You can employ the `default_command` config to specify the binary for spawning all nodes in the relay chain.

#### Features

Currently, the local provider does not execute any additional layers or processes.

## CLI Usage

Zombienet provides a CLI that allows interaction with the tool. The CLI can receive commands and flags to perform different kinds of operations. These operations can be initiated using the following syntax:

```bash
zombienet <arguments> <commands>
```

The following sections will guide you through the primary usage of the Zombienet CLI and the available commands and flags.

### CLI Commands

??? function "`spawn` - spawn the network defined in the config file"

    === "Argument"

        - `<networkConfig>` - a file that declares the desired network to be spawned in `toml` or `json` format. For further information, check out the [Configuration Files](#configuration-files) section

??? function "`test` - run test on the network spawned"

    === "Argument"

        - `<testFile>` - a file that defines assertions and tests against the spawned network, using natural language expressions to evaluate metrics, logs, and built-in functions

??? function "`setup` - set up the Zombienet development environment"

    === "Argument"

        - `<binaries>` - executables that will be downloaded and prepared to be used by Zombienet. Options: `polkadot`, `polkadot-parachain`

??? function "`convert` - transforms a (now deprecated) polkadot-launch configuration file to a Zombienet configuration file"

    === "Argument"

        - `<filePath>` - path to a [polkadot-launch](https://github.com/paritytech/polkadot-launch){target=_blank} configuration file with a `.js` or `.json` extension defined by [the `LaunchConfig` interface](https://github.com/paritytech/polkadot-launch/blob/295a6870dd363b0b0108e745887f51e7141d7b5f/src/types.d.ts#L10){target=_blank}

??? function "`version` - prints Zombienet version"

    === "Argument"

        - none 

??? function "`help` - prints help information"

    === "Argument"

        - none 

!!! warning
    For the `spawn` command to work on macOS, users need to be aware that the Polkadot binary is currently not compatible with macOS. As a result, macOS users will need to clone the [Polkadot repository](https://github.com/paritytech/polkadot-sdk){target=_blank}, build Polkadot binary, and manually add it to their PATH.

### CLI Flags

You can use the following flags to customize the behavior of the CLI:

??? function "`-p`, `--provider` - override provider to use"
    
    === "Options"

        - `podman`
        - `kubernetes` (default)
        - `native`

??? function "`-d`, `--dir` - directory path for placing the network files instead of random temp one"

    === "Options"

        - `<path>` 
        - example: `-d /home/user/my-zombienet`

??? function "`-f`, `--force` - force override all prompt commands"

    === "Options"

        - none

??? function "`-l`, `--logType` - type of logging on the console"

    === "Options"

        - `table` (default)
        - `text`
        - `silent`

??? function "`-m`, `--monitor` - start as monitor, do not auto clean up network"

    === "Options"

        - none

??? function "`-c`, `--spawn-concurrency` - number of concurrent spawning processes to launch"

    === "Options"

        - defaults to `1`

??? function "`-h`, `--help` - display help for command"

    === "Options"

        - none

## Configuration Files 

The network configuration can be given in either `json` or `toml` format. The Zombienet repository also provides a [folder with some examples](https://github.com/paritytech/zombienet/tree/main/examples){target=_blank} of configuration files that can be used as a reference.

!!! note
    Each section may include provider-specific keys that are not recognized by other providers. For example, if you use the local provider, any references to images for nodes will be disregarded.

### Settings

Through the keyword `settings`, it's possible to define the general settings for the network. The available keys are:

??? function "`bootnode` - add bootnode to network"

    === "Type"

        - Boolean

    === "Default Value"

        - `true`

??? function "`timeout` - global timeout to use for spawning the whole network"

    === "Type"

        - Number

    === "Default Value"

        - none

??? function "`provider` - provider to use (e.g., Kubernetes, Podman)"

    === "Type"

        - String

    === "Default Value"

        - `kubernetes`

??? function "`backchannel` - deploy an instance of backchannel server. Only available on Kubernetes"

    === "Type"

        - Boolean

    === "Default Value"

        - `false`

??? function "`polkadot_introspector` - Deploy an instance of polkadot-introspector. Only available on Podman and Kubernetes"

    === "Type"

        - Boolean

    === "Default Value"

        - `false`

??? function "`jaeger_agent` - the Jaeger agent endpoint passed to the nodes. Only available on Kubernetes"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`enable_tracing` - enable the tracing system. Only available on Kubernetes"

    === "Type"

        - Boolean

    === "Default Value"

        - `true`

??? function "`tracing_collator_url` - the URL of the tracing collator used to query by the tracing assertion"

    === "Type"

        - String
        - Should be tempo query compatible

    === "Default Value"

        - none

??? function "`tracing_collator_service_name` - service name for tempo query frontend. Only available on Kubernetes"

    === "Type"

        - String

    === "Default Value"

        - `tempo-tempo-distributed-query-frontend`

??? function "`tracing_collator_service_namespace` - namespace where tempo is running. Only available on Kubernetes"

    === "Type"

        - String

    === "Default Value"

        - `tempo`

??? function "`tracing_collator_service_port` - port of the query instance of tempo. Only available on Kubernetes"

    === "Type"

        - Number
        
    === "Default Value"
    
        - `3100`

??? function "`node_spawn_timeout` - timeout to spawn pod/process"

    === "Type"

        - Number
        
    === "Default Value"
    
        - `per provider`

??? function "`local_ip` - IP used for exposing local services (rpc/metrics/monitors)"

    === "Type"

        - String
        
    === "Default Value"
    
        - `"127.0.0.1"`

??? function "`node_verifier` - allow managing how to verify node readiness or disable by using `none`"

    === "Type"

        - String
        
    === "Default Value"
    
        - `Metric`

For example, the following configuration file defines a minimal example for the settings:

=== "TOML"

    ```toml title="base-example.toml"
    [settings]
    timeout = 1000
    bootnode = false
    provider = "kubernetes"
    backchannel = false
    ...
    ```

=== "JSON"

    ```json title="base-example.json"
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

### Relay Chain Configuration

You can use the `relaychain` keyword to define further parameters for the relay chain at start-up. The available keys are:

??? function "`default_command` - the default command to run"

    === "Type" 

        - String

    === "Default Value"

        - `polkadot`

??? function "`chain` - the chain name"

    === "Type" 

        - String

    === "Default Value"

        - `rococo-local`

??? function "`chain_spec_path` - path to the chain spec file"

    === "Type" 

        - String
        - Should be the plain version to allow customizations

    === "Default Value"

        - none

??? function "`chain_spec_command` - command to generate the chain spec. It can't be used in combination with `chain_spec_path`"

    === "Type" 

        - String

    === "Default Value"

        - none

??? function "`default_args` - an array of arguments to use as default to pass to the command"

    === "Type" 

        - Array of strings

    === "Default Value"

        - none

??? function "`default_substrate_cli_args_version` - set the Substrate CLI args version"

    === "Type" 

        - 0 \| 1 \| 2

    === "Default Value"

        - none

??? function "`default_overrides` - an array of overrides to upload to the nodes"

    === "Type" 

        - Array of objects

    === "Default Value"

        - none

??? function "`default_resources` - represents the resources limits/reservations needed by the nodes by default. Only available on Kubernetes"

    === "Type" 

        - Object

    === "Default Value"

        - none

??? function "`default_prometheus_prefix` - a parameter for customizing the metric's prefix"

    === "Type" 

        - String

    === "Default Value"

        - `substrate`

??? function "`random_nominators_count` - if set and the stacking pallet is enabled, Zombienet will generate the input quantity of nominators and inject them into the genesis"

    === "Type" 

        - Number (optional)

    === "Default Value"

        - none

??? function "`max_nominations` - the max number of nominations allowed by a nominator"

    === "Type" 

        - Number

    === "Default Value"

        - `24`
        - should match the value set in the runtime

### Node Configuration

There is one specific key capable of receiving more subkeys: the `nodes` key. This key is used to define further parameters for the nodes. The available keys:

??? function "`name` - name of the node"

    === "Type"

        - String
        -  Any whitespace will be replaced with a dash (e.g., 'new alice' -> 'new-alice')

    === "Default Value"

        - none

??? function "`image` - override default Docker image to use for this node"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`command` - override default command to run"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`command_with_args` - override default command and arguments"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`args` - arguments to be passed to the command"

    === "Type"

        - Array of strings

    === "Default Value"

        - none

??? function "`substrate_cli_args_version` - set the Substrate CLI args version directly to skip binary evaluation overhead"

    === "Type"

        - | 0 \| 1 \| 2

    === "Default Value"

        - none

??? function "`validator` - pass the `--validator` flag to the command"

    === "Type"

        - Boolean

    === "Default Value"

        - `true`

??? function "`invulnerable` - if true, add the node to invulnerables in the chain spec"

    === "Type"

        - Boolean

    === "Default Value"

        - `false`

??? function "`balance` - balance to set in balances for node's account"

    === "Type"

        - Number

    === "Default Value"

        - `2000000000000`

??? function "`env` - environment variables to set in the container"

    === "Type"

        - Array of objects

    === "Default Value"

        - none

??? function "`env.name` - name of the environment variable"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`env.value` - value of the environment variable"

    === "Type"

        - String \| Number

    === "Default Value"

        - none

??? function "`bootnodes` - array of bootnodes to use"

    === "Type"

        - Array of strings

    === "Default Value"

        - none

??? function "`overrides` - array of overrides definitions"

    === "Type"

        - Array of objects

    === "Default Value"

        - none

??? function "`add_to_bootnodes` - add this node to the bootnode list"

    === "Type"

        - Boolean

    === "Default Value"

        - `false`

??? function "`resources` - represent the resources limits/reservations needed by the node. Only available on Kubernetes"

    === "Type"

        - Object

    === "Default Value"

        - none

??? function "`ws_port` - WS port to use"

    === "Type"

        - Number

    === "Default Value"

        - none

??? function "`rpc_port` - RPC port to use"

    === "Type"

        - Number

    === "Default Value"

        - none

??? function "`prometheus_port` - Prometheus port to use"

    === "Type"

        - Number

    === "Default Value"

        - none

??? function "`prometheus_prefix` - customizes the metric's prefix for the specific node"

    === "Type"

        - String

    === "Default Value"

        - `substrate`

??? function "`keystore_key_types` - defines which keystore keys should be created"

    === "Type"

        - String

    === "Default Value"

        - none
    
The following configuration file defines a minimal example for the relay chain, including the `nodes` key:

=== "TOML"
        
    ``` toml title="relaychain-example-nodes.toml"

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

=== "JSON"

    ``` json title="relaychain-example-nodes.json"

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

### Node Group Configuration

The `node_groups` key is used to define further parameters for the node groups. The available keys are:

??? function "`name` - Group name, used for naming the nodes"

    === "Type"

        - String (e.g., `name-1`)
        - any whitespace will be replaced with a dash (e.g., 'new group' -> 'new-group')

    === "Default Value"

        - none

??? function "`count` - number of nodes to launch for this group"

    === "Type"

        - Number

    === "Default Value"

        - none

??? function "`image` - override default Docker image to use for this node"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`command` - override default command to run"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`args` - arguments to be passed to the command"

    === "Type"

        - Array of strings

    === "Default Value"

        - none

??? function "`env` - environment variables to set in the container"

    === "Type"

        - Array of objects

    === "Default Value"

        - none

??? function "`env.name` - name of the environment variable"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`env.value` - value of the environment variable"

    === "Type"

        - String \| Number

    === "Default Value"

        - none

??? function "`overrides` - array of overrides definitions"

    === "Type"

        - Array of objects

    === "Default Value"

        - none

??? function "`prometheus_prefix` - a parameter for customizing the metric's prefix for the specific node group"

    === "Type"

        - String

    === "Default Value"

        - `substrate`

??? function "`resources` - represent the resources limits/reservations needed by the node. Only available on Kubernetes"

    === "Type"

        - Object

    === "Default Value"

        - none

??? function "`substrate_cli_args_version` - set the Substrate CLI args version directly to skip binary evaluation overhead"

    === "Type"

        - | 0 \| 1 \| 2

    === "Default Value"

        - none


The following configuration file defines a minimal example for the relay chain, including the `node_groups` key:
    
=== "TOML"

    ```toml title="relaychain-example-node-groups.toml"
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

=== "JSON"

    ```json title="relaychain-example-node-groups.json"
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

### Parachain Configuration

The `parachain` keyword is used to define further parameters for the parachain. The available keys are:

??? function "`id` - the id to assign to this parachain. Must be unique"

    === "Type"

        - Number

    === "Default Value"

        - none

??? function "`add_to_genesis` - flag to add parachain to genesis or register in runtime"

    === "Type"

        - Boolean

    === "Default Value"

        - `true`

??? function "`cumulus_based` - flag to use cumulus command generation"

    === "Type"

        - Boolean

    === "Default Value"

        - `true`

??? function "`genesis_wasm_path` - path to the wasm file to use"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`genesis_wasm_generator` - command to generate the wasm file"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`genesis_state_path` - path to the state file to use"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`genesis_state_generator` - command to generate the state file"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`prometheus_prefix` - parameter for customizing the metric's prefix for all parachain nodes/collators"

    === "Type"

        - String

    === "Default Value"

        - `substrate`

??? function "`onboard_as_parachain` - flag to specify whether the para should be onboarded as a parachain or stay a parathread"

    === "Type"

        - Boolean

    === "Default Value"

        - `true`

??? function "`register_para` - flag to specify whether the para should be registered."

    === "Type"

        - Boolean

    === "Default Value"

        - `true`
        - The `add_to_genesis` flag must be set to false for this flag to have any effect

For example, the following configuration file defines a minimal example for the parachain:

=== "TOML"

    ```toml title="parachain-example.toml"
    [parachain]
    id = 100
    add_to_genesis = true
    cumulus_based = true
    genesis_wasm_path = "/path/to/wasm"
    genesis_state_path = "/path/to/state"
    ...
    ```

=== "JSON"

    ```json title="parachain-example.json"
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

### Collator Configuration
   
One specific key capable of receiving more subkeys is the `collator` key. This key is used to define further parameters for the nodes. The available keys are:

??? function "`name` - name of the collator"

    === "Type"

        - String
        - Any whitespace will be replaced with a dash (e.g., 'new alice' -> 'new-alice')

    === "Default Value"

        - none

??? function "`image` - image to use for the collator"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`command` - command to run for the collator"

    === "Type"

        - String

    === "Default Value"

        - `polkadot-parachain`

??? function "`args` - an array of arguments to use as defaults to pass to the command"

    === "Type"

        - Array of strings

    === "Default Value"

        - none

??? function "`substrate_cli_args_version` - sets the version directly to skip default Zombienet behavior of evaluating the binary to determine and set the correct version"

    === "Type"

        - | 0 \| 1

    === "Default Value"

        - none

??? function "`command_with_args` - overrides both command and arguments for the collator"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`env` - environment variables to set in the container for the collator"

    === "Type"

        - Array of objects

    === "Default Value"

        - none

??? function "`env.name` - name of the environment variable"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`env.value` - value of the environment variable"

    === "Type"

        - String \| Number

    === "Default Value"

        - none

??? function "`keystore_key_types` - defines which keystore keys should be created. For more details, refer to additional documentation"

    === "Type"

        - String

    === "Default Value"

        - none

The configuration file below defines a minimal example for the collator:

=== "TOML"

    ```toml title="collator-example.toml"
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

=== "JSON"

    ```json title="collator-example.json"
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

### Collator Groups
   
The `collator_groups` key is used to define further parameters for the collator groups. The available keys are:

??? function "`name`  - name of the collator"

    === "Type"

        - String
        - Any whitespace will be replaced with a dash (e.g., 'new alice' -> 'new-alice')

    === "Default Value"

        - none

??? function "`count`  - number of collators to launch for this group"

    === "Type"

        - Number

    === "Default Value"

        - none

??? function "`count`  - number of collators to launch for this group"

    === "Type"

        - Number

    === "Default Value"

        - none

??? function "`image`  - image to use for the collators"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`command`  - command to run for each collator"

    === "Type"

        - String

    === "Default Value"

        - `polkadot-parachain`

??? function "`args`  - an array of arguments to use as defaults to pass to the command"

    === "Type"

        - Array of strings

    === "Default Value"

        - none

??? function "`args`  - an array of arguments to use as defaults to pass to the command"

    === "Type"

        - Array of strings

    === "Default Value"

        - none

??? function "`command_with_args`  - overrides both command and arguments for each collator"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`env`  - environment variables to set in the container for each collator"

    === "Type"

        - Array of objects

    === "Default Value"

        - none

??? function "`env.name`  - name of the environment variable"

    === "Type"

        - String

    === "Default Value"

        - none

??? function "`env.value`  - value of the environment variable"

    === "Type"

        - String \| Number

    === "Default Value"

        - none

??? function "`substrate_cli_args_version`  - sets the version directly to skip default Zombienet behavior of evaluating the binary to determine and set the correct version"

    === "Type"

        - | 0 \| 1 \| 2

    === "Default Value"

        - none

For instance, the configuration file below defines a minimal example for the collator groups:

=== "TOML"

    ```toml title="collator-groups-example.toml"
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
    
=== "JSON"

    ```json title="collator-groups-example.json"
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

### XCM Configuration

You can use the `hrmp_channels` keyword to define further parameters for the XCM channels at start-up. The available keys are:

??? function "`hrmp_channels` - array of HRMP channel configurations"

    === "Type"

        - Array of objects

??? function "`sender` - parachain ID of the sender"

    === "Type"

        - Number

??? function "`recipient` - parachain ID of the recipient"

    === "Type"

        - Number

??? function "`max_capacity` - maximum capacity of the HRMP channel"

    === "Type"

        - Number

??? function "`max_message_size` - maximum message size allowed in the HRMP channel"

    === "Type"

        - Number

