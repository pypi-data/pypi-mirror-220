# flake8-numba

Improve your Python development experience with flake8-numba. This plugin integrates with Flake8 to provide
comprehensive code analysis for projects that make use of numba. When working with numba, many errors are not
discovered until the code is run. However, many of these issues can be perfectly caught by performing some basic
syntactical analysis. This tool helps you catch potential errors and enhance code quality effortlessly.

## Installation

Make sure that you have `flake8` installed. Then:

```
pip install flake8-numba
```

After it calling `flake8` will include all rules defined by this plugin.

## Rules

Some examples are:

```python
@vectorize([float64(float64, float64)])
def f(x, y):
    return x + y, 2  # ERROR: only 1 value can be returned
```

or:

```python
# ERROR: Dimensions mismatch (second argument at left is an array but an scalar at right)
@guvectorize([(float32, float32[:], float32)], "(), () -> ()")
def func(...) -> None:
    ...
```


All available rules can be read in `RULES.md`
