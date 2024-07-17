---
title: Minimal Example of the usage of Zombienet
description: This tutorial provides an example of how to use zombienet to spawn a network and run a simple test.
---

# Using Zombienet: A Minimal Example

This tutorial provides an example of how to use zombienet to spawn a basic network and run a simple test against it.

## Prerequisites

To follow this tutorial, first you need to have zombienet installed. If you haven't done so, please follow the instructions in the [Zombienet installation section](../index.md/#installation).

## Defining the network

As mentioned on the [Configuration Files section](../index.md/#configuration-files), Zombienet uses a configuration file to define the ephimeral network that will be spawned. This example will use the following configuration file:

```toml
[settings]
timeout = 120

[relaychain]
    [relaychain.nodes]
    name = "alice"
    
    [relaychain.nodes]
    name = "bob"

[parachains]
id = 100

    [parachains.collator]
    name = "collator01"
```

This configuration file defines a network with a relaychain with two nodes, `alice` and `bob`, and a parachain with a collator named `collator01`. Also, it sets a timeout of 120 seconds for the network to be ready.