# Installation

```bash
pip install myqcd
```

Requirements:

- Python 3.10 or newer;
- SymPy 1.12 or newer.

The complete test suite is currently exercised on Python 3.12 with SymPy 1.14.
Python 3.10, 3.11 and 3.13 are declared and expected to work but are not
automatically verified on this machine.

## Source checkout

```bash
pip install .
```

## Documentation build

```bash
python -m sphinx -b html -W docs/en docs/en/_build
```

## Evidence boundary

Installing the package gives access to the algebra, operator and diagram
layers. The `python -m myqcd` entry point additionally needs
`refer/papers/INDEX.md` from the source repository; in a pure installation use
`python -m myqcd.operator_audit` instead.
