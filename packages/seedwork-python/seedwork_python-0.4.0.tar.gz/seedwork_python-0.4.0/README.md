# seedwork-python

Python seedwork library.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Requirements

python 3.9+


## Installation

### Using poetry
Make sure you have installed [poetry](https://python-poetry.org/)

```bash
poetry add seedwork-python
```

### Using pip
```bash
pip install seedwork-python
```

## Usage

```python
from dataclasses import dataclass

from seedwork.domain.aggregate_root import AggregateRoot

@dataclass
class User(AggregateRoot):
    name: str
    age: int

    def is_adult(self) -> bool:
        return self.age >= 18

user = User(name='foo', age=18)

assert user.is_adult()
```

For more examples, please refer to [tests](./tests).

Or you can refer to the sample project [eshop](
    https://github.com/Huangkai1008/eshop
)

## License
[MIT @ Huang Kai](./LICENSE)


