---
title: Testing OpenGov Proposals with Chopsticks.
description: # Add description
---

# Testing OpenGov Proposals with Chopsticks

## Introduction

Polkadot's OpenGov is a sophisticated governance mechanism designed to allow the network to evolve gracefully over time, guided by its stakeholders. This system features multiple tracks for different types of proposals, each with its own parameters for approval, support, and timing. While this flexibility is powerful, it also introduces complexity that can lead to failed proposals or unexpected outcomes.

Testing governance proposals before submission is crucial for the ecosystem. This process enhances efficiency by reducing the need for repeated submissions, improves security by identifying potential risks, and allows for proposal optimization based on simulated outcomes. It also serves as an educational tool, providing stakeholders with a safe environment to understand the impacts of different voting scenarios. By leveraging simulation tools like Chopsticks, proposers can refine their ideas, anticipate potential issues, and increase the likelihood of successful implementation, ultimately leading to more effective and informed governance decisions.

By using Chopsticks, developers and governance participants can:

- Simulate the entire lifecycle of a proposal
- Test various voting outcomes and participation levels
- Analyze the effects of successful proposals on the network state
- Identify potential issues or unexpected consequences before real-world implementation

This tutorial will guide you through the process of using Chopsticks to thoroughly test OpenGov proposals, ensuring that when you submit a proposal to the live network, you can do so with confidence in its effects and viability.

## Prerequisites

- Basic understanding of [PolkadotJS](https://polkadot.js.org/docs/){target=_blank} and [OpenGov](https://wiki.polkadot.network/docs/learn-polkadot-opengov){target=_blank}

## Setting Up the Project

Before diving into testing OpenGov proposals, you need to set up your development environment. You'll create a TypeScript project and install the necessary dependencies. You'll use Chopsticks to fork the Polkadot network and simulate the proposal lifecycle, while PolkadotJS will be your interface for interacting with the forked network and submitting proposals.

Follow these steps to set up your project:

1. Create a new project directory and navigate into it:
  ```bash
  mkdir opengov-chopsticks && cd opengov-chopsticks
  ```

2. Initialize a new TypeScript project:
  ```bash
  npm init -y \
  && npm install typescript ts-node @types/node --save-dev \
  && npx tsc --init
  ```

3. Install the required dependencies:
  ```bash
  npm install @polkadot/api @acala-network/chopsticks
  ```

4. Create a new TypeScript file for your testing script:
  ```bash
  touch test-proposal.ts
  ```

5. Open the `tsconfig.json` file and ensure it includes these compiler options:
   ```json
   {
      "compilerOptions": {
        "module": "CommonJS",
        "esModuleInterop": true,
        "target": "esnext",
        "moduleResolution": "node",
        "declaration": true,
        "sourceMap": true,
        "skipLibCheck": true,
        "outDir": "dist",
        "composite": true
      }
    }
   ```

The `test-proposal.ts` file is where you'll write your code to simulate and test OpenGov proposals.
Now that your environment is set up, let's proceed to the introduction and steps for submitting a proposal.


## Submitting and Executing a Proposal Using Chopsticks

It's important to note that you should identify the right track and origin for your proposal. For example, if you're requesting funds from the treasury, select the appropriate treasury track based on the spend limits. For more detailed information, refer to [Polkadot OpenGov Origins](https://wiki.polkadot.network/docs/learn-polkadot-opengov-origins){target=_blank}.

### Submitting a Preimage

The preimage is the actual call that you want to execute trough governance. Submitting a preimage is separate from creating a proposal because storing a large preimage can be expensive. This separation allows another account to submit the preimage and pay the fee if needed.