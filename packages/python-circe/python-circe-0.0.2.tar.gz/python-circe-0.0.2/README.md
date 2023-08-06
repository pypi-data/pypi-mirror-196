# python-circe

This is a python wrapper for Circe. It is a port of the
[CirceR](https://github.com/OHDSI/CirceR) package.

## Features

* Convert a JSON cohort expression into a print-friendly presentation
* Convert a JSON cohort expression to a SQL query

## Installation

```bash
pip install python-circe
```

## Examples

```python
from importlib.resources import files

from circe.cohortExpression import CohortExpression

# load the example cohort expression
cohort_json = files('circe.data').joinpath('simpleCohort.json').read_text()

# create a cohort expression object
exp = CohortExpression.fromJson(cohort_json)

# Create print friendly output
print(MarkdownRender().renderCohort(exp))

```

## License
Apache License 2.0






