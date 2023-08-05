# 🦄 Magic RegEx
**Readable Regular Expressions for Python**

![Stable Version](https://img.shields.io/pypi/v/magicregex?label=stable)
![Python Versions](https://img.shields.io/pypi/pyversions/magicregex)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Downloads](https://img.shields.io/pypi/dm/magicregex)

1. Runtime is ultra-minimal
2. Compiles to pure RegEx
3. Automatically typed capture groups
4. Natural language syntax

This library is a port of the [magic-regexp](https://regexp.dev) JavaScript module by [Daniel Roe](https://roe.dev/).

## Quickstart

First, install `magicregex` by
```shell
pip install magicregex
```

Second, find e-mails in text by
```python
import magicregex as mre

reg = mre.createRegEx(
    mre.exactly(
        mre.letter.TimesAtLeast(1)
        .And(mre.exactly('@'))
        .And(mre.letter.TimesAtLeast(1))
        .And(mre.exactly('.'))
        .And(mre.letter.TimesAtLeast(2))
    )
)
reg.findall('daniel@roe.uk lore ipsum thomas@wollmann.de') 
# Result: ['daniel@roe.uk', 'thomas@wollmann.de']
```

## Documentation

Up to now, this module is compatible with [magic-regexp](https://regexp.dev/getting-started/usage)'s documentation.

## Contribute

Made with ❤️. If you want to support:

- Clone this repository
- Install dependencies using `poetry install --with dev`
- Run tests using `pytest`
- Run code checks using `pre-commit run`