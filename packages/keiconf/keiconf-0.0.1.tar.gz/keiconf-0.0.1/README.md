# keiconf

[![PyPI - Version](https://img.shields.io/pypi/v/keiconf.svg)](https://pypi.org/project/keiconf)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/keiconf.svg)](https://pypi.org/project/keiconf)
[![Hatch - Version](https://img.shields.io/badge/hatch-1.6.3-success)](https://github.com/pypa/hatch)

![Repo - PRs](https://img.shields.io/github/issues-pr-raw/asciifaceman/keiconf)
![Repo - Issues](https://img.shields.io/github/issues-raw/asciifaceman/keiconf)

A small, minimalist application json configuration tool for small projects.

Uses only stdlib if that matters to you.

-----

**Table of Contents**

- [Why tho?](#why-tho)
- [Installation](#installation)
- [Usage](#usage)
- [Parameters](#params)
- [Development](#development)
- [Limitations](#limitations)
- [Frequently Asked Questions](#faq)
- [License](#license)

## Why tho?
Fair question.

I originally started this project as an excuse to use Hatch and write a pyproject.toml no-distutils/setuptools python project and see how green the grass was.

I've typically been unhappy with the configuration options for python in a way I can't articulate very well, and I just wanted a simple json file read with some guiderails. Some quick user-side discovery to find my platform's config path and get going.

This project isn't meant to be a fully featured configuration system to slap into your next big webservice, it's just a small system to slap on your next prototype or small project. 

## Installation

```console
pip install keiconf
```

## Usage

```
from keiconf import KeiConf

k = KeiConf(filepath="path/to/file.json")
k.get("your_key")
k.get("path.to.your.nested_key")
k.start() # start watching config file for changes

```

## Params

```
KeiConf(filepath, indent=2, fail_on_missing_key=False, create_if_not_exist=False, watch_for_changes=False)
```

* `filepath:str`
    * The path to your target configuration file
    * ex. `/path/to/file.json`
* `indent:int`
    * The json indentation to use for the written file
    * ex. `2`
* `fail_on_missing_keys:bool`
    * If `True`, will raise a KeyError if a key is missing, which you can catch and exit on.
    * If `False`, will return nothing
* `create_if_not_exist:bool`
    * if `True`, will create the missing path directories and empty configuration file if it does not exist
    * if `False` will fail naturally on opening nonexistent configuration file
* `watch_for_changes:bool`
    * if `True` will launch the config file watcher on __init__ 
    * if `False` will not launch the config file watcher on __init__
    * See [Config File Watcher](#config-file-watcher) for more information

## Config File Watcher
If your KeiConf instance is started with `watch_for_changes=True` then a threaded file watcher will load changes to your configuration file as it sees them (within keiconf._CHANGE_WATCH_INTERVAL).

If your KeiConf instance is started with `watch_for_changes=False` then the threaded file watcher is not created automatically.

You can stop and start the file watcher manually via the start() and stop() functions. It can be start()'ed even if you launched with watch_for_changes=False

```
k = KeiConf(...)
k.start() # starts the file watcher if it isn't already
k.stop() # stops a running file watcher if it is running
```

The file watcher and loader is protected by a `threading.Lock()`

## Development
Development/Testing/Contribution requires hatch. Hatch provides the project management, environment abstraction, dependency resolution, and dev/test entrypoints. 

```
python3 -m pip install hatch
```

although it is recommended to install hatch via pipx

```
python3 -m pip install pipx
python3 -m pipx ensurepath
python3 -m pipx install hatch
```

## Limitations
* Need to investigate behavior with lists

## FAQ

* Why not dot notation / attribute reference?
    * A: I looked into this as I was interested in possibly doing it, but it looked rather lengthy to implement and involved modifying the base class quite a bit or using wrappers and I just wasn't sure that was in the spirit of minimalism. The get() function uses a string dot notation `get("path.to.key")` as a sort of middle ground. --- I may revisit in the future.

## License

`keiconf` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
