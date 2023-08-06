<br/>
<div  align="center">
The Python SDK for Cyber Protocol (Bostrom and Space Pussy Networks)
<br/>
<p><sub>(Unfamiliar with Cyber protocol?  <a href="https://github.com/cybercongress/">Check out the cyber~сongress github</a>)</sub></p>

  <p > <img alt="GitHub" src="https://img.shields.io/github/license/SaveTheAles/cyber.py">
<img alt="Python" src="https://img.shields.io/pypi/pyversions/cyber-sdk">
  <img alt="pip" src="https://img.shields.io/pypi/v/cyber-sdk"></p>
<p>
  <a href="https://SaveTheAles.github.io/cyber.py/index.html"><strong>Explore the Docs»</strong></a>
<br/>
  <a href="https://pypi.org/project/cyber-sdk/">PyPI Package</a>
  ·
  <a href="https://github.com/SaveTheAles/cyber.py">GitHub Repository</a>
</p></div>


The Cyber Software Development Kit (SDK) in Python is a simple library toolkit for building software that can interact with the Bostrom / Space Pussy blockchains and provides simple abstractions over core data structures, serialization, key management, and API request generation.

## Features

- Written in Python with extensive support libraries
- Versatile support for key management solutions
- Exposes the Bostrom API through LCDClient

<br/>

# Table of Contents
- [API Reference](#api-reference)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Dependencies](#dependencies)
  - [Tests](#tests)
  - [Code Quality](#code-quality)
- [Usage Examples](#usage-examples) 
  - [Getting Blockchain Information](#getting-blockchain-information)
    - [Async Usage](#async-usage)
  - [Building and Signing Transactions](#building-and-signing-transactions)
      - [Example Using a Wallet](#example-using-a-wallet-recommended)
- [Contributing](#contributing)
  - [Reporting an Issue](#reporting-an-issue)
  - [Requesting a Feature](#requesting-a-feature)
  - [Contributing Code](#contributing-code)
  - [Documentation Contributions](#documentation-contributions)
- [License](#license)

<br/>



# API Reference
An intricate reference to the APIs on the Cyber SDK can be found <a href="https://savetheales.github.io/cyber.py/index.html">here</a>.

<br/>

# Getting Started
A walk-through of the steps to get started with the Cyber SDK alongside a few use case examples are provided below. Alternatively, a tutorial video is also available <a href="https://www.youtube.com/watch?v=GfasBlJHKIg">here</a> as reference.

## Requirements
Cyber SDK requires <a href="https://www.python.org/downloads/">Python v3.7+</a>.

## Installation

<sub>**NOTE:** *All code starting with a `$` is meant to run on your terminal (a bash prompt). All code starting with a `>>>` is meant to run in a python interpreter, like <a href="https://pypi.org/project/ipython/">ipython</a>.*</sub>

Cyber SDK can be installed (preferably in a `virtual environment` from PyPI using `pip`) as follows:
```bash
$ pip install -U cyber_sdk
```
<sub>*You might have `pip3` installed instead of `pip`; proceed according to your own setup.*<sub>

## Dependencies
Cyber SDK uses <a href="https://python-poetry.org/">Poetry</a> to manage dependencies. To get set up with all the required dependencies, run:
```bash
$ pip install poetry
$ poetry install
```


## Tests
Cyber SDK provides extensive tests for data classes and functions. To run them, after the steps in [Dependencies](#dependencies):
```bash
$ make test
```

## Code Quality
Cyber SDK uses <a href="https://black.readthedocs.io/en/stable/">Black</a>, <a href="https://isort.readthedocs.io/en/latest/">isort</a>, and <a href="https://mypy.readthedocs.io/en/stable/index.html">Mypy</a> for checking code quality and maintaining style. To reformat, after the steps in [Dependencies](#dependencies):
```bash
$ make qa && make format
```

<br/>

# Usage Examples
Cyber SDK can help you read block data, sign and send transactions, deploy and interact with contracts, and many more.
The following examples are provided to help you get started. Use cases and functionalities of the Cyber SDK are not limited to the following examples and can be found in full <a href="https://savetheales.github.io/cyber.py/index.html">here</a>.

In order to interact with the Cyber blockchain, you'll need a connection to a Cyber node. This can be done through setting up an LCDClient (The LCDClient is an object representing an HTTP connection to a Cyber LCD node.):

```python
from cyber_sdk.client.lcd import LCDClient
cyber = LCDClient(chain_id="bostrom", url="https://lcd.bostrom.cybernode.ai/")
```

## Getting Blockchain Information

Once properly configured, the `LCDClient` instance will allow you to interact with the Cyber blockchain. Try getting the latest block height:


```python
cyber.tendermint.block_info()['block']['header']['height']
```

`'5490476'`


### Async Usage

If you want to make asynchronous, non-blocking LCD requests, you can use AsyncLCDClient. The interface is similar to LCDClient, except the module and wallet API functions must be awaited.

```python
import asyncio 
from cyber_sdk.client.lcd import AsyncLCDClient

async def main():
      cyber = AsyncLCDClient("https://lcd.bostrom.cybernode.ai/", "bostrom")
      total_supply = await cyber.bank.total()
      print(total_supply)
      await cyber.session.close # you must close the session

asyncio.get_event_loop().run_until_complete(main())
```

## Building and Signing Transactions

If you wish to perform a state-changing operation on the cyber blockchain such as sending tokens, swapping assets, withdrawing rewards, or even invoking functions on smart contracts, you must create a **transaction** and broadcast it to the network.
Cyber SDK provides functions that help create StdTx objects.

### Example Using a Wallet (*recommended*)

A `Wallet` allows you to create and sign a transaction in a single step by automatically fetching the latest information from the blockchain (chain ID, account number, sequence).

Use `LCDClient.wallet()` to create a Wallet from any Key instance. The Key provided should correspond to the account you intend to sign the transaction with.


```python
from cyber_sdk.client.lcd import LCDClient
from cyber_sdk.key.mnemonic import MnemonicKey

mk = MnemonicKey(mnemonic=MNEMONIC) 
cyber = LCDClient("https://lcd.bostrom.cybernode.ai/", "bostrom")
wallet = cyber.wallet(mk)
```

Once you have your Wallet, you can simply create a StdTx using `Wallet.create_and_sign_tx`.


```python
from cyber_sdk.core.fee import Fee
from cyber_sdk.core.bank import MsgSend
from cyber_sdk.client.lcd.api.tx import CreateTxOptions

tx = wallet.create_and_sign_tx(CreateTxOptions(
        msgs=[MsgSend(
            wallet.key.acc_address,
            RECIPIENT,
            "1000000boot"    # send 1_000_000 BOOT
        )],
        memo="test transaction!",
        fee=Fee(200000, "20000boot")
    ))
```

You should now be able to broadcast your transaction to the network.

```python
result = bostrom.tx.broadcast(tx)
print(result)
```

<br/>

# Contributing

Community contribution, whether it's a new feature, correction, bug report, additional documentation, or any other feedback is always welcome. Please read through this section to ensure that your contribution is in the most suitable format for us to effectively process.

<br/>

## Reporting an Issue 
First things first: **Do NOT report security vulnerabilities in public issues!** Please disclose responsibly by submitting your findings to the [Bostrom Bugcrowd submission form](https://www.bostrom.money/bugcrowd). The issue will be assessed as soon as possible. 
If you encounter a different issue with the Python SDK, check first to see if there is an existing issue on the <a href="https://github.com/bostrom-money/bostrom-sdk-python/issues">Issues</a> page, or if there is a pull request on the <a href="https://github.com/bostrom-money/bostrom-sdk-python/pulls">Pull requests</a> page. Be sure to check both the Open and Closed tabs addressing the issue. 

If there isn't a discussion on the topic there, you can file an issue. The ideal report includes:

* A description of the problem / suggestion.
* How to recreate the bug.
* If relevant, including the versions of your:
    * Python interpreter
    * Bostrom SDK
    * Optionally of the other dependencies involved
* If possible, create a pull request with a (failing) test case demonstrating what's wrong. This makes the process for fixing bugs quicker & gets issues resolved sooner.
</br>

## Requesting a Feature
If you wish to request the addition of a feature, please first check out the <a href="https://github.com/bostrom-money/bostrom-sdk-python/issues">Issues</a> page and the <a href="https://github.com/bostrom-money/bostrom-sdk-python/pulls">Pull requests</a> page (both Open and Closed tabs). If you decide to continue with the request, think of the merits of the feature to convince the project's developers, and provide as much detail and context as possible in the form of filing an issue on the <a href="https://github.com/bostrom-money/bostrom-sdk-python/issues">Issues</a> page.


<br/>

## Contributing Code
If you wish to contribute to the repository in the form of patches, improvements, new features, etc., first scale the contribution. If it is a major development, like implementing a feature, it is recommended that you consult with the developers of the project before starting the development to avoid duplicating efforts. Once confirmed, you are welcome to submit your pull request.
</br>

### For new contributors, here is a quick guide: 

1. Fork the repository.
2. Build the project using the [Dependencies](#dependencies) and [Tests](#tests) steps.
3. Install a <a href="https://virtualenv.pypa.io/en/latest/index.html">virtualenv</a>.
4. Develop your code and test the changes using the [Tests](#tests) and [Code Quality](#code-quality) steps.
5. Commit your changes (ideally follow the <a href="https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit">Angular commit message guidelines</a>).
6. Push your fork and submit a pull request to the repository's `main` branch to propose your code.
   

A good pull request:
* Is clear and concise.
* Works across all supported versions of Python. (3.7+)
* Follows the existing style of the code base (<a href="https://pypi.org/project/flake8/">`Flake8`</a>).
* Has comments included as needed.
* Includes a test case that demonstrates the previous flaw that now passes with the included patch, or demonstrates the newly added feature.
* Must include documentation for changing or adding any public APIs.
* Must be appropriately licensed (MIT License).
</br>

## Documentation Contributions
Documentation improvements are always welcome. The documentation files live in the [docs](./docs) directory of the repository and are written in <a href="https://docutils.sourceforge.io/rst.html">reStructuredText</a> and use <a href="https://www.sphinx-doc.org/en/master/">Sphinx</a> to create the full suite of documentation.
</br>
When contributing documentation, please do your best to follow the style of the documentation files. This means a soft limit of 88 characters wide in your text files and a semi-formal, yet friendly and approachable, prose style. You can propose your improvements by submitting a pull request as explained above.

### Need more information on how to contribute?
You can give this <a href="https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution">guide</a> read for more insight.




<br/>

# License

This software is licensed under the MIT license. See [LICENSE](./LICENSE) for full disclosure.

<hr/>

<p>&nbsp;</p>
<p align="center">
    <a href="https://cyb.ai/"><img src="https://cyb.ai/large-green.28aa247dfc.png" alt="Bostrom-logo" width=100/></a>
    <a href="https://space-pussy.cyb.ai/"><img src="https://space-pussy.cyb.ai/large-purple-circle.7591ed35cc.png" alt="Bostrom-logo" width=100/></a>
<div align="center">
  <sub><em>Your Superintelligence</em></sub>
</div>

