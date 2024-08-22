---
title: Convert assets on Asset Hub
description: A guide detailing the step-by-step process of converting assets on Asset Hub, helping users navigate the asset management on the platform efficiently.
---

# Asset Conversion on Asset Hub

## Introduction

Asset Conversion is an Automated Market Maker (AMM) that utilizes [Uniswap V2](https://github.com/Uniswap/v2-core){target=\_blank} logic and is implemented as a pallet on Polkadot's AssetHub. For more details about this feature, please visit the Asset Conversion on the [Asset Conversion on Asset Hub](https://wiki.polkadot.network/docs/learn-asset-conversion-assethub){target=\_blank} page. 

This guide will provide detailed information about the key functionalities offered by the
[Asset Conversion](https://github.com/paritytech/polkadot-sdk/tree/master/substrate/frame/asset-conversion){target=\_blank} pallet on Asset Hub, including: 

- Creating a liquidity pool
- Adding liquidity to a pool
- Swapping assets
- Withdrawing liquidity from a pool

#TODO: talk about test env

## Prerequisites

Before converting assets on Asset Hub, you must ensure to have:

- Access the [Polkadot.Js App](https://polkadot.js.org/apps){target=\_blank} interface and connect it to the intended blockchain
- A funded wallet containing the assets you wish to convert, and that the wallet has enough balance to cover the transaction fees

## Creating a Liquidity Pool

