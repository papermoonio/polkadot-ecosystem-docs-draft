# Testing DSL

Zombienet provides a Domain Specific Language (DSL) for writing tests. The DSL is designed to be human-readable and allows you to write tests using natural language expressions. Using this DSL, you can define assertions and tests against the spawned network. This way, users can evaluate different metrics, such as:

- On chain storage
- Metrics
- Histograms
- Logs
- System events
- Tracing
- Custom api calls (through polkadot.js)
- Commands 

These abstractions are expressed by sentences defined in a natural language style. Therefore, each test line will be mapped to a test to run. Also, the test file (`*.zndsl`) includes pre-defined header fields used to define information about the suite, such as network configuration and credentials location.

## Test file 

### Name

The test name in Zombienet is derived from the filename by removing any leading numeric characters before the first hyphen. For example, a file named “0001-zombienet-test.zndsl” will result in a test name of "zombienet-test" which will be displayed in the test runner’s report output.

### Structure

The test file is a text file with the extension `.zndsl`. It is divided into two parts: the header and the body. The header contains the network configuration and the credentials to use, while the body contains the tests to run.

The header is defined by the following fields:

| Key            | Type     | Description                                                                                     |
| -------------- | -------- | ----------------------------------------------------------------------------------------------- |
| `description`  | String (optional) | Long description of the test suite                                                  |
| `network`      | String   | Path to the network definition file, supported in both `json` and `toml` formats                   |
| `creds`        | String   | Credentials file name or path to use (available only with Kubernetes provider). Looks in current directory or `$HOME/.kube/` if a filename is passed |

The body contains the tests to run. Each test is defined by a sentence in the DSL, which is mapped to a test to run. Each test line defines an assertion or a command to be executed against the spawned network.

#### Assertions

Assertions are defined by sentences in the DSL that evaluate different metrics, such as on-chain storage, metrics, histograms, logs, system events, tracing, and custom API calls. Each assertion is defined by a sentence in the DSL, which is mapped to a test to run.

- `Well know functions` - already mapped test function
    - node-name: `well-know_defined_test` [within x seconds]. For example:
        - alice: is up
        - alice: parachain 100 is registered within 225 seconds
        - alice: parachain 100 block height is at least 10 within 250 seconds

- `Histogram assertion` - get metrics from prometheus, calculate the histogram and assert on the target value/s.
    - node-name: `reports histogram memtric_name has comparator target_value samples in buckets ["bucket","bucket",...] [within x seconds]`
        - `alice`: reports histogram polkadot_pvf_execution_time has at least 2 samples in buckets ["0.1", "0.25", "0.5", "+Inf"] within 100 seconds

- `Metric assertion` - get metric from prometheus and assert on the target value.
    - node-name: `reports metric_name comparator target_value (e.g "is at least x", "is greater than x") [within x seconds]`. For example:
        - alice: reports node_roles is 4

- `Logs assertions` - get logs from nodes and assert on the matching pattern (support regex and glob).
    - node-name: `log line (contains|matches) (regex|glob) "pattern" [within x seconds]`. For example:
        - alice: log line matches glob "rted #1" within 10 seconds

- `Logs assertions` - get logs from nodes and assert on the number of lines matching pattern (support regex and glob).
    - node-name: `count of log lines (containing|matcheing) (regex|glob) "pattern" [within x seconds]`. For example:
        - alice: count of log lines matching glob "rted #1" within 10 seconds

- System events assertion - find a system event from subscription by matching a pattern. The subscription is made when we start this particular test, so we can not match on event in the past.
    - node-name: `system event (contains|matches)(regex| glob) "pattern" [within x seconds]`. For example:
        - alice: system event matches ""paraId":[0-9]+" within 10 seconds

- `Tracing assertion` - match an array of span names from the supplied traceID. This is NOT supported by the native provider
    - node-name: `trace with traceID contains ["name", "name2",...]`. For example:
        - alice: trace with traceID 94c1501a78a0d83c498cc92deec264d9 contains ["answer-chunk-request", "answer-chunk-request"]

- `Custom js scripts` - allow to run a defined JS script and assert on the completeness or return value.
    - node-name: `js-script script_relative_path [return is comparator target_value] [within x seconds]`. For example:
        - alice: js-script ./0008-custom.js return is greater than 1 within 200 seconds

- `Custom ts scripts` - allow to run a defined TS script and assert on the completeness or return value.
    - node-name: `ts-script script_relative_path [return is comparator target_value] [within x seconds]`. For example:
        - alice: ts-script ./0008-custom-ts.ts return is greater than 1 within 200 seconds

- `Backchannel wait for value and register to use`
    - node-name: `wait for var name and use as X [within 30 seconds]`. For example:
        - alice: wait for name and use as X within 30 seconds

#### Commands

Commands allow interaction with the nodes, with the ability to run pre-defined commands or an arbitrary command in the node.

- `restart`
    -  node-name `restart [after x seconds]` - will stop the process and start again after the x amount of seconds or innmediatly.
    - node-name `pause` - will pause (SIGSTOP) the process
    - node-name `resume` - will pause (SIGCONT) the process
    - `sleep x` - will sleep the test-runner for x amount of seconds.


## Example

For example, the following test file defines two tests: a small network test and a big network test. Each test defines a network configuration file and credentials to use.

The tests define assertions to evaluate the network’s metrics and logs. The assertions are defined by sentences in the DSL, which are mapped to tests to run.

``` toml
Description: Small Network test
Network: ./0000-test-config-small-network.toml
Creds: config

# metrics
alice: reports node_roles is 4
alice: reports sub_libp2p_is_major_syncing is 0

# logs
bob: log line matches glob "*rted #1*" within 10 seconds
bob: log line matches "Imported #[0-9]+" within 10 seconds
```

And the second test file:

``` toml
Description: Big Network test
Network: ./0001-test-config-big-network.toml
Creds: config

# metrics
alice: reports node_roles is 4
alice: reports sub_libp2p_is_major_syncing is 0

# logs
bob: log line matches glob "*rted #1*" within 10 seconds
bob: log line matches "Imported #[0-9]+" within 10 seconds

# custom js script
alice: js-script ./0008-custom.js return is greater than 1 within 200 seconds

# custom ts script
alice: ts-script ./0008-custom-ts.ts return is greater than 1 within 200 seconds

# backchannel
alice: wait for name and use as X within 30 seconds

# well know functions
alice: is up
alice: parachain 100 is registered within 225 seconds
alice: parachain 100 block height is at least 10 within 250 seconds

# histogram
alice: reports histogram polkadot_pvf_execution_time has at least 2 samples in buckets ["0.1", "0.25", "0.5", "+Inf"] within 100 seconds

# system events
alice: system event matches ""paraId":[0-9]+" within 10 seconds

# tracing
alice: trace with traceID 94c1501a78a0d83c498cc92deec264d9 contains ["answer-chunk-request", "answer-chunk-request"]
```

## Running tests

To run the tests by using native provider, you can use the `zombienet` binary. The binary will read the test files and execute the tests defined in the DSL. The binary will output the results of the tests in the console.

```bash
zombienet -p native test <INSERT_TEST_FILE_NAME>
```

!!! note
    Replace `<INSERT_TEST_FILE_NAME>` with the path to the test file you want to run.

