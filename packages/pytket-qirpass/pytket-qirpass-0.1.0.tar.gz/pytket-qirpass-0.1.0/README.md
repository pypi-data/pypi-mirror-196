# pytket-qirpass

This module provides a method to optimize QIR using pytket.

## Installation

Python 3.9, 3.10 or 3.11 is required.

### From pypi

```shell
pip install pytket-qirpass
```

### Locally

The package is built with the `flit` backend, so it is first necessary to
install this:

```shell
pip install flit
```

Then to install lfrom the top-level directory (containing `pyproject.toml`):

```shell
flit install
```

To run unit tests:

```shell
python -m unittest test.test_qirpass
```

(These take a few minutes to run.)

## Usage

This module provides a single function, `apply_qirpass`, which takes as input

- some QIR bitcode
- a pytket compilation pass
- a target gateset

and outputs some new QIR bitcode, where the pass has been applied to the basic
blocks in the input program, followed by a rebase to the target gateset.

For example:

```python
from pytket_qirpass import apply_qirpass
from pytket.circuit import OpType
from pytket.passes import FullPeepholeOptimise

qir_out = apply_qirpass(
    qir_bitcode=qir_in,
    comp_pass=FullPeepholeOptimise(allow_swaps=False),
    target_1q_gates={OpType.Rx, OpType.Rz},
    target_2q_gates={OpType.ZZPhase},
)
```

Both the input and the output are Python `bytes` objects.

Provided the pass preserves the circuit semantics, `apply_qirpass` preserves
the QIR semantics.
