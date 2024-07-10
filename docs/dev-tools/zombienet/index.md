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
    nix run github:paritytech/zombienet/<INSERT_ZOMBIENET_VERSION> -- \\
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
    docker run -it --rm \\
    -v $(pwd):/workspace \\
    paritytech/zombienet:<INSERT_ZOMBIENET_VERSION> \\
    spawn /workspace/<INSERT_ZOMBIENET_CONFIG_FILE_NAME>.toml
    ```

    !!! note
        Ensure to replace the `<INSERT_ZOMBIENET_VERSION>` with the desired version of Zombienet. Also, replace the `<INSERT_ZOMBIENET_CONFIG_FILE_NAME>` with the name of the configuration file you want to use.

    !!! warning
        The command above mounts the current directory to the `/workspace` directory inside the Docker container. This allows Zombienet to access the configuration file and other files in the current directory. If you want to mount a different directory, replace `$(pwd)` with the desired directory path.


## Providers

Internally, Zombienet is a Javascript library, designed to run on Node.js and support different backend providers to run the nodes; at this moment [Kubernetes]( https://kubernetes.io/ ){target=_blanket}, [Podman]( https://podman.io/ ){target=_blanket} and, native are supported.

It's important to note that each provider has its own specific requirements and installation steps. The following sections guide the installation process for each provider and the necessary requirements.

### Kubernetes
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod

### Podman
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod

### Native
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod

## CLI Usage