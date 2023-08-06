<table>
  <tr>
    <td colspan=2><strong>
    shil
      </strong>&nbsp;&nbsp;&nbsp;&nbsp;
      <small><small>
      </small></small>
    </td>
  </tr>
  <tr>
    <td width=15%><img src=img/icon.png style="width:150px"></td>
    <td>
      Shell-util library for python.  Includes helpers for subprocess invocation, shell-formatters / pretty-printers, and more.
      <br/><br/>
      <a href=https://pypi.python.org/pypi/shil/><img src=""https://img.shields.io/pypi/l/shil.svg"></a>
      <a href="https://github.com/elo-enterprises/shil/actions/workflows/python-test.yml"><img src="https://github.com/elo-enterprises/shil/actions/workflows/python-test.yml/badge.svg"></a>
    </td>
  </tr>
</table>

---------------------------------------------------------------------------------

  * [Overview](#overview)
    * [Features](#features)
  * [Installation](#installation)
  * [Usage](#usage)
    * [OOP-style Dispatch](#oop-style-dispatch)
    * [Functional approach to dispatch](#functional-approach-to-dispatch)
    * [Loading data when command-output is JSON](#loading-data-when-command-output-is-json)
    * [Serialization with Pydantic](#serialization-with-pydantic)
    * [Caller determines logging](#caller-determines-logging)
    * [Rich-console Support](#rich-console-support)
    * [Stay DRY with Runners](#stay-dry-with-runners)


---------------------------------------------------------------------------------

## Overview

The `shil` library provides various shell-utilities for python.

### Features

* Helpers for subprocess invocation
* Shell-formatters / pretty-printers
* A somewhat usable parser / grammer for bash
* Console support for [rich](https://rich.readthedocs.io/en/stable/index.html) & [rich protocols](https://rich.readthedocs.io/en/stable/protocol.html)


---------------------------------------------------------------------------------

## Installation

See [pypi](https://pypi.org/project/shil/) for available releases.

```
pip install shil
```

---------------------------------------------------------------------------------

## Usage

See also:

* [the unit-tests](tests/units) for some examples of library usage
* [the smoke-tests](tests/smoke/test.sh) for example usage of stand-alone scripts


### OOP-style Dispatch 

This uses `shil.Invocation` and returns `shil.InvocationResponse`.

```
import shil 
req = cmd = shil.Invocation(command='ls /tmp')
resp = cmd()
print(resp.stdout)
```

### Functional approach to dispatch

Use `shil.invoke`, get back `shil.InvocationResponse` 

```
import shil 
resp = shil.invoke('ls /tmp')
```

### Loading data when command-output is JSON

```
import shil 
req = cmd = shil.Invocation(command='echo {"foo":"bar"}')
resp = cmd()
print(resp.data)
assert type(resp.data) == type({})
assert resp.data['foo']=='bar'
```

### Serialization with Pydantic

```
import shil 
import json
req = cmd = shil.Invocation(command='echo {"foo":"bar"}')
resp = cmd()
json.loads(resp.json())
json.loads(req.json())
for k,v in req.dict().items():
  assert getattr(resp,k)==v
```

### Caller determines logging 

Works like this with basic logger:

```
import shil 
import logging
logger = logging.getLogger()
shil.invoke('ls /tmp', command_logger=logger.critical, output_logger=logger.warning)
```

Supports using [rich-logger](https://rich.readthedocs.io/en/stable/logging.html) too:

```
import shil 
from rich.console import Console 
console = Console(stderr=True)
shil.invoke('ls /tmp', command_logger=console.log)
```

### Rich-console Support

Besides using rich-logger as above, you can use the [rich-protocol](https://rich.readthedocs.io/en/stable/protocol.html) more directly.  Printing works the way you'd expect for `Invocation` and `InvocationResponse`.

```
import shil 
req = cmd = shil.Invocation(command='echo {"foo":"bar"}')
resp = cmd()
import rich
rich.print(req)
rich.print(resp)
```


### Stay DRY with Runners

Runner's are basically just [partials](https://en.wikipedia.org/wiki/Partial_application) on `shil.invoke`.  It's simple but this can help reduce copying around repetitive configuration.

```
from rich.console import Console 
console=Console(stderr=True)
runner = shil.Runner(
  output_logger=console.log,
  command_logger=console.log)
runner('ls /tmp')
```
