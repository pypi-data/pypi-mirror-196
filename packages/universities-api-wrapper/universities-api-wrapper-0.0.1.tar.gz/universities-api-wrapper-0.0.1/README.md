# Universities API Wrapper

This is a small API wrapper designed to consume [Universities API](https://github.com/Hipo/university-domains-list-api) from Python command line. API consumer was built as a project to build first Python library. 

## Requirements

This package requires [requests](https://pypi.org/project/requests/) package to function properly.

## Installation

### Local installation

Install the package via:

```bash
python setup.py install
```

### PyPI installation

Alternatively, you can install package via PyPI `pip` package manager.

## Usage

Once installed, you can use wrapper the following way. First, instantiate the library.

```python
from universities_api_wrapper import HipolabsUniversitiesAPI
```

Then initialize the client. If you are using local connection only:

```python
client = HipolabsUniversitiesAPI("local")
```

Alternatively, if you wish to use remote connection:

```python
client = HipolabsUniversitiesAPI("remote")
```

If you pass anything else, library will raise `UniversitiesAPIError`.

Client has now been initialized. Let's start searching.

### Search by Country

```python
client.search("Turkey")
```

### Search by University

```python
client.search(None, "East")
```

### Combination Search

This function is searching by country and university name.

```python
client.search("Turkey", "East")
```

## Unit Tests

This module has built-in unit test kit in `tests` folder. You can run the unit tests by:

```
python -m pytest tests
```

## License

This API consumer is licensed under [MIT license](https://opensource.org/license/mit/).
