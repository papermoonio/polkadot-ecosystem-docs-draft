---
title: Using chopsticks  for forking Substrate based chains.
description: Discover the fundamentals of using Chopsticks to replay blockchain transactions, analyze changes in system state, simulate XCM interactions, and locally duplicate substrate based networks.
---

# Chopsticks

## Introduction

[Chopsticks]({{ repositories.chopsticks }}){target=_blank} introduces a user-friendly method for developers to locally fork existing Substrate-based chains. This capability enables the replaying of blocks to analyze transaction impacts and facilitates the forking of multiple chains for comprehensive testing. This capability empowers developers to experiment with custom blockchain configurations in a local development environment, avoiding the complexities of deploying on a live network. By simplifying the process of building blockchain applications on Substrate, Chopsticks aims to broaden developers’ accessibility and rapid iteration in blockchain development. 

This article covers the fundamentals of using Chopsticks to fork Substrate-based chains, including replaying blockchain transactions, analyzing changes in system state, simulating cross-chain message (XCM) interactions, and locally duplicating Substrate-based networks. 

!!!Note
    Chopsticks does not support calls made through the Ethereum JSON-RPC at this time. Consequently, you cannot fork your chain using Chopsticks and connect Metamask to it.

## Getting Started

To begin using Chopsticks, you can install it as a package using either [Node package manager]({{ tools.npm }}){target=_blank} or [Yarn]({{ tools.yarn }}){target=_blank}:

```bash
npm i @acala-network/chopsticks@latest
```

After installation, you can execute commands using the Node package executor. For instance, the following command allows you to execute Chopstick's main command.

```bash
npx i @acala-network/chopsticks@latest
```

