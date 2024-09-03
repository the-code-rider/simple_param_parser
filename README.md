# Simple Param Parser
A dead simple, dependency free, param parser which reads command line args and return the value as a dict. Useful for quick
command line testing or integration. The package itself doesn't perform any validation. It simply reads and passes the value.

# How To Use

## Install

`pip install simple_param_parser`

```python
from simple_param_parser import accept_params

if __name__ == "__main__":
    params = accept_params(['--name', '--age', '--city'])
    print(params)

```