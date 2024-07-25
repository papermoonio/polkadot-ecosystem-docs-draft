---
title: Minimal Example of the usage of Zombienet
description: This tutorial provides an example of how to use Zombienet to spawn a basic network and run a simple test over it.
---

# Using Zombienet: A Minimal Example

This tutorial provides an example of how to use zombienet to spawn a basic network and run a simple test against it.

## Prerequisites

To follow this tutorial, first you need to have zombienet installed. If you haven't done so, please follow the instructions in the [Zombienet installation section](../index.md/#installation).

## Defining the network

As mentioned in the [Configuration Files section](../index.md/#configuration-files), Zombienet uses a configuration file to define the ephemeral network that will be spawned. This example will use the following configuration file:

```toml
[settings]
timeout = 120

[relaychain]

[[relaychain.nodes]]
name = "alice"
validator = true

[[relaychain.nodes]]
name = "bob"
validator = true

[[parachains]]
id = 100

  [parachains.collator]
  name = "collator01
```

This configuration file defines a network with a relaychain with two nodes, `alice` and `bob`, and a parachain with a collator named `collator01`. Also, it sets a timeout of 120 seconds for the network to be ready.


## Running the network

To spawn the network, run the following command:

```bash
zombienet -p native spawn minimal-example.toml
```

This command will spawn the network defined in the `minimal-example.toml` configuration file. The `-p native` flag specifies that the network will be spawned using the native runtime.

If successful, you will see the following output:

<div id="termynal" data-termynal>
    <span data-ty="input"><span class="file-path">zombienet -p native spawn minimal-example.toml</span>
    <table>
        <thead>
            <tr>
                <th colspan="3" align="center">
                    Network launched 🚀🚀
                </th>
            </tr>
        </thead>
        <tr>
            <th>Namespace</th>
            <td>zombie-75a01b93c92d571f6198a67bcb380fcd</td>
        </tr>
        <tr>
            <th>Provider</th>
            <td>native</td>
        </tr>
            <tr>
                <th colspan="3" align="center">
                Node Information
                </th>
            </tr>
        <tr>
            <th>Name</th>
            <td>alice</td>
        </tr>
        <tr>
            <th>Direct Link</th>
            <td><a href="https://polkadot.js.org/apps/?rpc=ws://127.0.0.1:55308#explorer">https://polkadot.js.org/apps/?rpc=ws://127.0.0.1:55308#explorer</a></td>
        </tr>
        <tr>
            <th>Prometheus Link</th>
            <td><a href="http://127.0.0.1:55310/metrics">http://127.0.0.1:55310/metrics</a></td>
        </tr>
        <tr>
            <th>Log Cmd</th>
            <td>tail -f /var/folders/f4/7rdt2m9d7j361dm453cpggbm0000gn/T/zombie-75a01b93c92d571f6198a67bcb380fcd_21724-2</td>
        </tr>
            <tr>
                <th colspan="3" align="center">
                Node Information
                </th>
            </tr>
        <tr>
            <th>Name</th>
            <td>bob</td>
        </tr>
        <tr>
            <th>Direct Link</th>
            <td><a href="https://polkadot.js.org/apps/?rpc=ws://127.0.0.1:55312#explorer">https://polkadot.js.org/apps/?rpc=ws://127.0.0.1:55312#explorer</a></td>
        </tr>
        <tr>
            <th>Prometheus Link</th>
            <td><a href="http://127.0.0.1:55314/metrics">http://127.0.0.1:55314/metrics</a></td>
        </tr>
        <tr>
            <th>Log Cmd</th>
            <td>tail -f /var/folders/f4/7rdt2m9d7j361dm453cpggbm0000gn/T/zombie-75a01b93c92d571f6198a67bcb380fcd_21724-2</td>
        </tr>
            <tr>
                <th colspan="3" align="center">
                Node Information
                </th>
            </tr>
        <tr>
            <th>Name</th>
            <td>collator01</td>
        </tr>
        <tr>
            <th>Direct Link</th>
            <td><a href="https://polkadot.js.org/apps/?rpc=ws://127.0.0.1:55316#explorer">https://polkadot.js.org/apps/?rpc=ws://127.0.0.1:55316#explorer</a></td>
        </tr>
        <tr>
            <th>Prometheus Link</th>
            <td><a href="http://127.0.0.1:55318/metrics">http://127.0.0.1:55318/metrics</a></td>
        </tr>
        <tr>
            <th>Log Cmd</th>
            <td>tail -f /var/folders/f4/7rdt2m9d7j361dm453cpggbm0000gn/T/zombie-75a01b93c92d571f6198a67bcb380fcd_21724-2</td>
        </tr>
        <tr>
            <th>Parachain ID</th>
            <td>100</td>
        </tr>
        <tr>
            <th>ChainSpec Path</th>
            <td>/var/folders/f4/7rdt2m9d7j361dm453cpggbm0000gn/T/zombie-75a01b93c92d571f6198a67bcb380fcd_21724-2</td>
        </tr>
    </table>
</div>


!!! note 
    Consider that the IPs and ports may vary dynamically each time the network is spawned if those parameters are not explicity defined in the configuration file, so the links provided in the output may not be the same as the ones in the example.
