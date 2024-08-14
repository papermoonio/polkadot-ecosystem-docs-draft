---
title: Register a foreign asset
description: An in-depth guide to registering a foreign asset on the Asset Hub parachain, providing clear, step-by-step instructions.
---

# Register a foreign asset on Asset Hub

## Introduction

As outlined in the [Asset Hub Overview](./overview.md#foreign-assets){target=_blank}, Asset Hub supports two categories of assets: local and foreign. Foreign assets are originated outside of Asset Hub and are recognized by [`Multilocations`](https://wiki.polkadot.network/docs/learn/xcm/fundamentals/multilocation-summary){target=_blank}. This guide will walk you through the process of registering a foreign asset on the Asset Hub parachain.

In order to register a foreign asset on Asset Hub, it's important to notice that the process involves a communication between two parachains. Asset Hub parachain will be the destination of the foreign asset, while the source parachain will be the origin of the asset. The communication between the two parachains is facilitated by the [Cross-Chain Message Passing (XCMP)](https://wiki.polkadot.network/docs/learn-xcm){target=_blank} protocol.

## Prerequisites

