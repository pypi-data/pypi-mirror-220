# Pandas Sans Lambdas

![Tests](https://github.com/jakeantmann/pandas_sans_lambdas/actions/workflows/tests.yml/badge.svg)

Pandas method chaining using `assign` or `loc` usually means using lambdas. These get repetitive and reduce readability. Pandas Sans Lambdas is a solution to this. Here's an example:

``` python
import pandas as pd
from pandas_sans_lambdas import col

df = pd.DataFrame({"a": [1,2,3], "b": [4,5,6]})

# The old way
df = df.assign(with_lambdas = lambda DF: DF["a"] ** 2 / DF["b"])

# The new way
df = df.assign(sans_lambdas = col("a") ** 2 / col("b"))

print(df)
```

Hopefully you agree that this is more readable!

## Current project status

This package is under development. Specifically, unit test coverage is currently incomplete. Get in touch if you want to contribute to test coverage, or if you find any bugs!
