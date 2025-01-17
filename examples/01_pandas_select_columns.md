---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"tags": ["learning objective"]}

:::{hint} About this demo
:class: dropdown

This exercice illustrates:
- the use of MyST for rich text, including admonitions and embedded values
- the use of arbitrary features of the underlying language and
  libraries to generate random values (here a Pandas DataFrame) and
  test them.
- specifying learning objectives as a narrative
- the rich display of values
- one approach to structure the solution and answer cells enabling
  testing and displaying the solution

:::

:::{admonition} Learning objective

Extract multiple columns from a Pandas DataFrame.

:::


```{code-cell} ipython3
:tags: [hide-cell]

from random import randint
import numpy as np
import pandas as pd

NROWS = randint(2, 5)
NCOLUMNS = randint(10, 12)
columnnames = [f"C{randint(0, NCOLUMNS-1)}"
            for i in range(randint(2, min(3, NCOLUMNS)))]

T = pd.DataFrame(
    data=np.array(range(NROWS*NCOLUMNS)).reshape(NROWS, NCOLUMNS),
    columns=[f"C{str(col)}" for col in range(NCOLUMNS)],
    index=[f"L{str(line)}" for line in range(NROWS)])
```

+++

:::{admonition} Instructions

Consider `T` be the following Pandas DataFrame:

{eval}`T`

Extract the columns {eval}`columnnames` from `T`, in the given order.

:::

```{code-cell} ipython3
:tags: [hide-cell, solution]

T[columnnames]
```

```{code-cell} ipython3
:tags: [answer]

_
```

```{code-cell} ipython3
:tags: [hide-cell, test]

answer = _
solution = __
assert type(answer) == type(solution)
pd.testing.assert_frame_equal(answer, solution)
```
