# Olympix Test Generator

Olympix Test Generator is a Python package designed to assist with the generation of unit tests for Solidity smart contracts. These unit tests are specifically designed to be ran through [Foundry](https://book.getfoundry.sh/), a tool for writing unit tests in Solidity. 

## Installation

You can install Olympix Test Generator using pip:

```bash
pip install opix-test-generator
```

## Usage

The package includes a command-line interface for generating tests.

Before running the script, make sure to set the `OPLYMPIX_API_KEY` environment variable in a `.env` file located in the same directory.

To generate a test, run:

```bash
olympix generate
```

The tool will guide you through the process of generating the test.

## Project Structure

The project includes the following Python files:

- `client.py`: The main script for interacting with the Olympix DevSecTools API. It includes an interactive command-line interface.

## Dependencies

This project's dependencies are specified in the `requirements.txt` file.