---
title: Asset Transfer API
description: Asset Transfer API is a library that simplifies the transfer of assets for Substrate based chains. It provides methods for cross-chain and local transfers.
---

# Asset Transfer API

## Introduction

[Asset Transfer API](https://github.com/paritytech/asset-transfer-api){target=_blank}, a tool developed and maintained by [Parity](https://www.parity.io/){target=_blank}, is a specialized library designed to streamline asset transfers for Substrate-based blockchains. This API provides a simplified set of methods for users to:

- Execute asset transfers to other parachains or locally within the same chain
- Facilitate transactions involving system parachains like Asset Hub (Polkadot and Kusama)

The Asset Transfer API supports Parachain to Parachain transfers, currently limited to XCM V2, except for primary asset transactions. 

By using this API, developers can manage asset transfers more efficiently, reducing the complexity associated with cross-chain transactions and enabling smoother operations within the ecosystem.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/en/){target=_blank} (recommended version 21 or greater)
- Package manager - [npm](https://www.npmjs.com/){target=_blank} should be installed with Node.js by default. Alternatively, you can use other package managers like [Yarn](https://yarnpkg.com/){target=_blank}

## Install Asset Transfer API

To use `asset-transfer-api`, you need a JavaScript project. If you don't have one, you can create a new one:

1. Create a new directory for your project:
    ```bash
    mkdir my-asset-transfer-project \
    && cd my-asset-transfer-project
    ```

2. Initialize a new project:
    ```bash
    npm init -y
    ```

Once you have a project set up, you can install the asset-transfer-api package:

```bash
npm install @substrate/asset-transfer-api@{{build_on_polkadot.xcm.asset_transfer_api.version}}
```

!!!note
    This documentation covers version {{build_on_polkadot.xcm.asset_transfer_api.version}} of Asset Transfer API.








