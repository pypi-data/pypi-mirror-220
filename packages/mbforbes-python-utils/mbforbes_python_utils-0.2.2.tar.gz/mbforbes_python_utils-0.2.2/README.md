# python-utils

So maybe I stop writing the same things over and over.

## Installation

```sh
# Python 3 only (I'm using Python 3.7).
pip install mbforbes-python-utils
```

## Usage

```python
from mbforbes_python_utils import read, write, flatten

# read() removes leading/trailing whitespace.
contents = read("foo.txt")

# write() creates intermediate directories if needed.
# Pass `info_print = False` to disable printing.
write("bar/baz.txt", contents)

# flatten() flattens lists.
flatten([[1, [2, [3]]]])  # -> [1, 2, 3]
```

## Tests

```sh
python test_mbforbes_python_utils.py
```

## Releasing

I don't do this enough to remember how to do it

```sh
# Increment version in setup.py. Then,
pip install twine wheel
python setup.py sdist bdist_wheel
twine check dist/*
# If the above failed, `rm -rf build/ dist/` before retrying
twine upload dist/*
```
