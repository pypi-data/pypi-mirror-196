# plink
[![PyPI version](https://badge.fury.io/py/plink-url.svg)](https://badge.fury.io/py/plink-url)
[![Buymeacoffee](https://badgen.net/badge/icon/buymeacoffee?icon=buymeacoffee&label)](https://www.buymeacoffee.com/sg6j7z465pf)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![GitHub issues](https://img.shields.io/github/issues/jessicaward/plink)](https://GitHub.com/jessicaward/plink/issues/)

Recursive link analyser, written in Python

## Installation
To install plink, run the following command in your terminal:
```bash
python -m pip install --upgrade pip wheel
python -m pip install plink-url
```

To upgrade plink, run the following command in your terminal:
```bash
python -m pip install --upgrade pip wheel
python -m pip install --upgrade plink-url
```

If this does not work, you may have to use the `python3` or `pip3` commands instead.

## Examples
Basic example:
```bash
plink-url https://github.com/Jessicaward/plink
```

Limit analysis to a single domain:
```bash
plink-url https://jessica.im/Blog/ --whitelist https://jessica.im
```

Block multiple domains:
```bash
plink-url https://jessica.im/ --blacklist https://last.fm https://stackoverflow.com
```

Include extra information:
```bash
plink-url https://jessica.im/ --verbose
```

Specify a depth limit:
```bash
plink-url https://jessica.im/ --depth=3
```

Print extra details about the tool and it's usage:
```bash
plink-url https://jessica.im/ --help
```
