---
title: HRMP Channels
description: HRMP channels enable cross-chain communication in Polkadot, a temporary solution before the more efficient XCMP protocol is implemented.
---

# HRMP Channels

## Introduction

Polkadot is designed to enable seamless interoperability between its connected parachains. At the core of this interoperability is the Cross-Consensus Message Format (XCM), a standard language that allows parachains to communicate and interact with each other.

The actual network-layer protocol responsible for delivering XCM-formatted messages between parachains is called the Cross-Chain Message Passing (XCMP) protocol. XCMP maintains messaging queues on the Relay Chain, serving as a bridge to facilitate cross-chain interactions.

However, as XCMP is still under development, Polkadot has implemented a temporary substitute known as Horizontal Relay-routed Message Passing (HRMP). HRMP provides the same interface and functionality as the planned XCMP, but with a key difference - it stores all messages directly in the Relay Chain's storage, which is more resource-intensive.

Once XCMP is fully implemented, HRMP will be deprecated in favor of the native XCMP protocol. XCMP will offer a more efficient and scalable solution for cross-chain message passing, as it will not require the Relay Chain to store all the messages.

## Establishing HRMP Channels

To facilitate communication between parachains using the HRMP protocol, the parachains must explicitly establish communication channels by registering them on the Relay Chain.

Downward and upward channels from and to the Relay Chain are implicitly available, meaning they do not need to be explicitly opened.

Opening an HRMP channel requires the parachains involved to make a deposit on the Relay Chain. This deposit covers the expenses of using the Relay Chain's storage for the message queues associated with the channel.

### Relay Chain Parameters

Each Polkadot relay chain has a set of configurable parameters that control the behavior of the message channels between parachains. These parameters include `hrmpSenderDeposit`, `hrmpRecipientDeposit`, `hrmpChannelMaxMessageSize`, and `hrmpChannelMaxCapacity`.

When a parachain wants to open a new channel, it must take these parameter values into account to ensure the channel is configured properly.

To view the current values of these parameters in the Polkadot network:

1. Visit [Polkadot.js Apps](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fpolkadot.api.onfinality.io%2Fpublic-ws#/explorer), navigate to the **Developer** dropdown and select the **Chain state** option

    ![](/polkadot-ecosystem-docs-draft/images/build-on-polkadot/hrmp-channels/hrmp-channels-1.webp)

2. Under the **configuration** section, call the `activeConfig()` function by clicking the button with the **+** icon. This will display the current settings for all the Polkadot network parameters, including the HRMP channel settings

    ![](/polkadot-ecosystem-docs-draft/images/build-on-polkadot/hrmp-channels/hrmp-channels-2.webp)

### Dispatching Extrinsics

Establishing new HRMP channels between parachains requires dispatching specific extrinsic calls on the Polkadot relay chain from the parachain's origin.

The most straightforward approach is to implement the channel opening logic off-chain, then use the XCM pallet's `send` extrinsic to submit the necessary instructions to the relay chain. However, the ability to send arbitrary programs through the `Transact` instruction in XCM is typically restricted to privileged origins, such as the sudo pallet or governance mechanisms.

Parachain developers have a few options for triggering the required extrinsic calls from their parachain's origin, depending on the configuration and access controls defined:

- Sudo - if the parachain has a sudo pallet configured, the sudo key holder can use the sudo extrinsic to dispatch the necessary channel opening calls
- Governance - the parachain's governance system, such as a council or OpenGov, can be used to authorize the channel opening calls
- Privileged Accounts - the parachain may have other designated privileged accounts that are allowed to dispatch the HRMP channel opening extrinsics

## Opening HRMP Channels Between Parachains

For establishing bidirectional communication channels between parachains on the Polkadot network, using the HRMP protocol, the following steps are required:

1. Channel Request - the parachain that wants to open an HRMP channel must make a request to the parachain it wishes to have an open channel with
2. Channel Acceptance - the other parachain must then accept this request in order to complete the channel establishment

This process results in a unidirectional HRMP channel, where messages can flow in only one direction between the two parachains.

To enable bidirectional communication, an additional HRMP channel must be established in the opposite direction. This requires repeating the request and acceptance process, but with the parachains reversing their roles.

Once both unidirectional channels are established, the parachains can then send messages back and forth freely through the bidirectional HRMP communication channel.

### Detailed Procedure for HRMP Channel Setup

This example will demonstrate how to open a channel between parachain 2500 and parachain 2600, using Rococo Local as the relay chain.

#### Step 1 - Fund Sovereign Account

The sovereign account for parachain 2500 on the relay chain must be funded so it can take care of any XCM transact fees.

Use Polkadot.js Apps UI to connect to the relay chain and transfer funds from your account to the parachain 2500 sovereign account.
![](/polkadot-ecosystem-docs-draft/images/build-on-polkadot/hrmp-channels/hrmp-channels-3.webp)

??? note "Calculating Parachain Sovereign Account"
    To generate the sovereign account address for a parachain, you'll need to follow these steps:

    1. Determine if the parachain is an "up/down" chain (parent or child) or a "sibling" chain:

        - Up/down chains use the prefix `0x70617261` (which decodes to `b"para"`)

        - Sibling chains use the prefix `0x7369626c` (which decodes to `b"sibl"`)

    2. Calculate the u32 scale encoded value of the parachain ID:

        For example, parachain 2500 would be encoded as `c4090000`

    3. Combine the prefix and parachain ID encoding to form the full sovereign account address:

        The sovereign account of parachain 2500 in relay chain will be `0x70617261c4090000000000000000000000000000000000000000000000000000`
        and the SS58 format of this address is `5Ec4AhPSY2GEE4VoHUVheqv5wwq2C1HMKa7c9fVJ1WKivX1Y`
    
    To perform this conversion, you can also use the **"Para ID" to Address** section in [Substrate Utilities](https://www.shawntabrizi.com/substrate-js-utilities/).

#### Step 2 - Create Channel Opening Extrinsic

1. In Polkadot.js Apps, connect to the relay chain, navigate to the **Developer** dropdown and select the **Extrinsics** option

    ![](/polkadot-ecosystem-docs-draft/images/build-on-polkadot/hrmp-channels/hrmp-channels-4.webp)

2. Construct an `hrmpInitOpenChannel` extrinsic call

    1. Select the **hrmp** pallet
    2. Choose the **hrmpInitOpenChannel** extrinsic
    3. Fill in the parameters
        - **recipient** - parachain ID 
        - **proposedMaxCapacity** - max number of messages that can be pending in the channel at once
        - **proposedMaxMessageSize** - max message size that could be put into the channel
    4. Copy the encoded call data
    ![](/polkadot-ecosystem-docs-draft/images/build-on-polkadot/hrmp-channels/hrmp-channels-5.webp)

#### Step 3 - Submit XCM to Initiate Channel


## Opening HRMP Channels with System Parachains

