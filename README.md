# dotenv-manager

A decorator for defining a set of environment variables.
Uses the python-dotenv package to load additional variables from .env

The dotenv manager ensures the environment variables used in the project are set and have the correct types.

## Getting Started

```shell
pip install dotenv-manger
```

```python
from dotenv_manger import EnvManager

@EnvManager()
class CONFIG:
    KEY1: str
    KEY2: str
    INT_KEY: int
```
Using the ```prefix``` parameter, it is possible to use a common prefix and separate the variables in groups.
```python
@EnvManager(prefix="AWS_")
class AWS_CONFIG:
    SECRET: str
    ENDPOINT: str

@EnvManager(prefix="AZURE_")
class AZURE_CONFIG:
    SECRET: str
    ENDPOINT: str
```
Using strict=False, an error message is printed to the terminal, instead of throwing an error.
```python
@EnvManager(strict=False)
class CONFIG:
    NOT_FOUND_KEY: str
    ENDPOINT: str
```
