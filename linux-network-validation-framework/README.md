# Linux Network Validation & Test Automation Framework

A Python-based QA automation project for validating TCP/UDP communication on Linux.

The project was designed to demonstrate practical software QA, networking, automation, debugging, logging, and failure-diagnostics skills.

## What it validates

### TCP functional tests
- TCP connectivity
- PING/PONG validation
- ECHO message validation
- Command processing
- Large payload handling
- Response latency measurement

### UDP functional tests
- UDP connectivity
- PING/PONG validation
- ECHO validation
- Invalid command handling

### Negative tests
- Closed port connection
- Timeout detection
- Unknown command handling
- Graceful connection close

### Reliability tests
- Multiple simultaneous clients
- Repeated connections
- Server restart and recovery

### Diagnostics
The framework can collect Linux networking information using commands such as:

```bash
ip addr
ip route
ss -lnt
ping
```

It also performs a TCP port reachability check and records latency/error information.

## Architecture

```text
                    +------------------+
                    |   Test Runner    |
                    +---------+--------+
                              |
          +-------------------+-------------------+
          |                   |                   |
 +--------v-------+   +-------v--------+  +-------v---------+
 | Functional QA |   | Negative Tests |  | Reliability QA  |
 +--------+-------+   +-------+--------+  +-------+---------+
          |                   |                   |
          +-------------------+-------------------+
                              |
                    +---------v---------+
                    | TCP / UDP Servers |
                    +---------+---------+
                              |
                    +---------v---------+
                    | Diagnostics/Logs  |
                    +-------------------+
```

## Project structure

```text
linux-network-validation-framework/
├── app/
│   ├── tcp_server.py
│   ├── tcp_client.py
│   ├── udp_server.py
│   └── udp_client.py
├── diagnostics/
│   └── network_diagnostics.py
├── tests/
│   ├── test_tcp_functional.py
│   ├── test_udp_functional.py
│   ├── test_negative.py
│   ├── test_concurrency_recovery.py
│   └── test_diagnostics.py
├── logs/
├── reports/
├── run_tests.py
├── README.md
└── .gitignore
```

## Run

No external Python packages are required.

```bash
python3 run_tests.py
```

The framework generates:

```text
reports/test_report.txt
reports/test_report.json
logs/tcp_server.log
logs/udp_server.log
```

## CV description

**Linux Network Validation & Test Automation Framework | 2026**

Developed a Python-based automated network validation framework on Linux for testing TCP/UDP communication. Designed functional, negative, timeout, recovery and concurrent-connection test scenarios, with automated failure diagnostics, logging and test reporting.

**Technologies:** Python, Linux, TCP/IP, UDP, Socket Programming, Test Automation.
