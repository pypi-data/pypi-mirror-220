# A lightweight library for Connecting to Google Cloud Run Endpoints
This is a lightweight library for making authenticated calls to Cloud Run endpoints with Python clients.

## Usage
Before you can use this project, you need to install [Poetry](https://python-poetry.org/docs/), a tool for dependency management and packaging in Python.
On Unix-based systems (like Linux and MacOS), you can install Poetry using this command:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

- To run tests, from `alis-build-client/alis/build`: ```python -m unittest discover test``` \
- To install the package locally: ```poetry install``` \
- To build the package: ```poetry build``` \
- To publish the package: \
    - Populate dist/ by building the package from source \
    - Set up ~/.pypirc \
    ```
    [pypi]
        username = __token__
        password = <API_KEY>
    ```
    - Publish dist/ with twine \
    ```pip install twine```
    ```twine upload -r pypi dist/*```
