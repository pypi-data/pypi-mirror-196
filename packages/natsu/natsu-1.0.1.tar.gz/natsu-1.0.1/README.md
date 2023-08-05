# natsu

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/natsu?logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/natsu)
[![PyPI](https://img.shields.io/pypi/v/natsu?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/natsu)
[![PyPI - License](https://img.shields.io/pypi/l/natsu?color=03cb98&style=for-the-badge)](https://github.com/celsiusnarhwal/natsu/blob/main/LICENSE.md)
[![Code style: Black](https://aegis.celsiusnarhwal.dev/badge/black?style=for-the-badge)](https://github.com/psf/black)

natsu allows you to `sum()` with Python objects of any class that implements `__add__()`.

## Installation

```bash
pip install natsu
```

## Usage

```python
from natsu import sum

sum(some_iterable)
```

`natsu.sum()` is fully backwards-compatible with the built-in `sum()` function.

## License

natsu is licensed under the [MIT License](LICENSE.md).
