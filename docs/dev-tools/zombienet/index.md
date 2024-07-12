---
title: Using Zombienet to spawn ephemeral substrate based networks
description: Diving depper into zombienet, a tool that allows spawning ephemeral substrate networks.
---

# Zombienet

## Introduction

Zombienet is a testing framework designed for Substrate-based blockchains. It provides a simple CLI tool for creating and testing blockchain environments locally or across networks. It supports various backend providers, including Kubernetes, Podman, and native setups for running blockchain nodes. 

The framework enables developers to create tests using natural language tools, allowing them to verify on-chain storage, metrics, logs, and custom interactions with the blockchain. It is particularly effective for setting up local relay chains with validators and parachains with collators.

This framework has been designed and developed by [Parity Technologies]({{ https://www.parity.io/ }}){target=_blanket}, now mantained by the Zombienet team. For further support and information, please refer to the following contact points:
    
- [Zombienet repository]( https://github.com/paritytech/zombienet ){target=_blanket}
- [Element public channel]( https://matrix.to/#/!FWyuEyNvIFygLnWNMh:parity.io?via=parity.io&via=matrix.org&via=web3.foundation ){target=_blanket}

## Installation


Zombienet releases can be found on the [Zombienet repository]( https://github.com/paritytech/zombienet ){target=_blanket}. Each release includes executables for Linux and Macos, which are generated using [pkg]( https://github.com/vercel/pkg ){target=_blanket}. This allows the Zombienet CLI to operate without requiring Node.js to be installed. 

In order to install Zombienet, there are some options available, depending on the user's preferences and the environment where it will be used. The following sections will guide you through the installation process for each of the available options.

=== "Using the executable" 

    Zombienet can be downloaded using the latest release uploaded on the [Zombienet repository]( https://github.com/paritytech/zombienet/releases ){target=_blanket}. You can download the executable for your operating system and architecture, and then move it to a directory in your PATH. Or you can either dowlonad it directly from the command line using `curl` or `wget`:

    === "Curl"
        ```bash
        curl -LO \\
        https://github.com/paritytech/zombienet/releases/download/<INSERT_ZOMBIENET_VERSION>/<INSERT_ZOMBIENET_EXECUTABLE>
        ``` 
    === "Wget"
        ```bash
        wget \\
        https://github.com/paritytech/zombienet/releases/download/<INSERT_ZOMBIENET_VERSION>/<INSERT_ZOMBIENET_EXECUTABLE>
        ```
    !!! note
        Ensure to replace the URL with the `<INSERT_ZOMBIENET_VERSION>` that you want to download, as well as the `<INSERT_ZOMBIENET_EXECUTABLE>` with the name of the executable file that matches your operating system and architecture. This tutorial uses v1.3.106 and zombienet-macos-arm64 as an example.

    Then, you should make the downloaded file executable:

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

    For Nix users, Zombienet repository provides a [`flake.nix`](https://github.com/paritytech/zombienet/blob/main/flake.nix){target=_blanket} file that can be used to install Zombienet using the Nix package manager. To install Zombienet using Nix, you can run the following command, that will fetch the flake and install the Zombienet package:

    ```bash
    nix run github:paritytech/zombienet/<INSERT_ZOMBIENET_VERSION> -- \
    spawn <INSERT_ZOMBIENET_CONFIG_FILE_NAME>.toml
    ```

    !!! Warning
        To run the command above, you need to have [nix flakes enabled](https://nixos.wiki/wiki/Flakes#Enable_flakes){target=_blanket}.

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

Internally, Zombienet is a Javascript library, designed to run on Node.js and support different backend providers to run the nodes; at this moment [Kubernetes]( https://kubernetes.io/ ){target=_blanket}, [Podman]( https://podman.io/ ){target=_blanket} and, native are supported.

It's important to note that each provider has its own specific requirements and associated features. The following sections will guide you through the installation process for each provider and the necessary requirements, as well as the features that each provider offers.

### Kubernetes

#### Requirements
Zombienet is designed to be compatible with a variety of Kubernetes clusters, including [Google Kubernets Engine (GKE)](https://cloud.google.com/kubernetes-engine){target=_blanket}, [Docker Desktop](https://docs.docker.com/desktop/kubernetes/){target=_blanket}, and [kind](https://kind.sigs.k8s.io/){target=_blanket}. To effectively interact with your cluster, you'll need to ensure that [`kubectl`](https://kubernetes.io/docs/reference/kubectl/) is installed on your system, which is the Kubernetes command-line tool that allows you to run commands against Kubernetes clusters.

Moreover, in order to create resources such as namespaces, pods, and cronJobs within the target cluster, you must have the appropriate permissions granted to your user or service account. These permissions are essential for managing and deploying applications effectively within Kubernetes.

#### Features
In Kubernetes, Zombienet uses the Prometheus operator (if available) to oversee monitoring and visibility. This configuration ensures that only essential networking-related pods are deployed. By using the Prometheus operator, Zombienet improves its capability to efficiently monitor and manage network activities within the Kubernetes cluster.

### Podman

#### Requirements
Zombienet supports Podman rootless as a provider. To use it, you simply need to have Podman installed on your system and specify it either in the network file or using the `--provider` flag in the CLI.

!!! note
    Currently, Podman can only be used with Zombienet on Linux machines. Although Podman has support for macOS through an internal VM, the Zombienet provider code requires Podman to run natively on Linux.

#### Features
Using Podman, Zombienet deploys additional pods to enhance the monitoring and visibility of the active network. Specifically, pods for Prometheus, Tempo, and Grafana are included in the deployment. Grafana is configured with Prometheus and Tempo as datasources.

Upon launching Zombienet, access to these monitoring services is facilitated through specific URLs provided in the output:

- Prometheus - [http://127.0.0.1:34123](http://127.0.0.1:34123){target=_blanket}
- Tempo - [http://127.0.0.1:34125](http://127.0.0.1:34125){target=_blanket}
- Grafana - [http://127.0.0.1:41461](http://127.0.0.1:41461){target=_blanket}

It's important to note that Grafana is deployed with default admin access.

!!! note
    When the network operations cease—either by halting a running spawn with Ctrl+C or upon completion of the test—all associated pods, including those for Prometheus, Tempo, and Grafana, are automatically removed by Zombienet.

### Native

#### Requirements
The Zombienet Native provider enables you to run nodes as local processes in your environments. You simply need to have the necessary binaries for your network (such as `polkadot` and `polkadot-parachain`). You can choose to set it up by configuring your network file or using the `--provider` flag in the CLI.

!!! note
    The native provider exclusively utilizes the command config for nodes/collators, which supports both relative and absolute paths. You can employ the `default_command` config to specify the binary for spawning all nodes in the relay chain.

#### Features
Currently, the Native provider does not execute any additional layers or processes.

## CLI Usage

Zombienet provides a CLI tool that allows interaction with the tool. The CLI can receive commands and flags to perform different kinds of operations. The following sections will guide you through the primary usage of the Zombienet CLI and the available commands and flags.

| Command      | Arguments    | Description                          |
| :---------:  | :---------:  | :----------------------------------: |
| `spawn`      |  `<networkConfig>` - a file that declares the desired network to be spawned in `toml` or `json` format. For further information, check out [Configuration Files](#configuration-files) section. | Spawn the network defined in the config file |
| `test`       |  `<testFile>` - a file that defines assertions and tests against the network spawned, by using a set of `natural language expressions`. This helps to make assertiosn metrics, logs, and built-in functions.   | Run test on the network spawned |
| `setup`      | `<binaries>` - executables that will be downloaded and prepared to be used by Zombienet. Options: `polkadot`, `polkadot-parachain`. | Setup is meant for downloading and making dev environment of Zombienet ready. |
| `convert`    | `<filePath>` - path to a [Polkadot Launch](https://github.com/paritytech/polkadot-launch){target=_blanket} configuration file with a .js or .json extension defined by [this structure](https://github.com/paritytech/polkadot-launch/blob/295a6870dd363b0b0108e745887f51e7141d7b5f/src/types.d.ts#L10){target=_blanket} | Convert is meant for transforming a (now deprecated) polkadot-launch configuration to zombienet configuration |
| `version`    | - | Prints zombienet version |
| `help`       | - | Prints help information |

!!! warning
    For the `spawn` command to work on macOS, users need to be aware that the Polkadot binary is currently not compatible with macOS. As a result, macOS users will need to clone the [Polkadot repository](https://github.com/paritytech/polkadot-sdk){target=_blanket}, generate a release, and manually add it to their PATH.

Then, you can use the following flags to customize the behavior of the CLI:

| Flag         | Description                          |
| :---------:  | :----------------------------------: |
| `-p`, `--provider` | Provider to use for spawning the network |
| `-c`, `--config` | Path to the configuration file |
| `-n`, `--network` | Network to spawn |


## Configuration Files {#configuration-files}