# promoted-python-delivery-client

Python client SDK for the Promoted.ai Delivery API

## Prereqs

- wheel
- setuptools
- twine
- [bump2version](https://github.com/c4urself/bump2version/)

## Development

- Start venv: `source venv/bin/activate`
- Build wheel: `python setup.py bdist_wheel`
- Install locally: `pip install dist/promoted_python_delivery_client-0.1.0-py3-none-any.whl --force-reinstall`
- Try it out:
  - See the `scripts/` directory.
  - Create a `.env` file with a few variables:
    ```sh
    DELIVERY_ENDPOINT=<GET ME FROM PROMOTED>
    DELIVERY_API_KEY=<GET ME FROM PROMOTED>
    METRICS_ENDPOINT=<GET ME FROM PROMOTED>
    METRICS_API_KEY=<GET ME FROM PROMOTED>
    ```
  - Invoke (for example) `python3 scripts/call_delivery.sh`.

## Testing

### Unit tests

- Use pytest:
  - `pytest tests/`

## Release

- Create a development branch
- `bump2version [major|minor|patch]`
- Send a pull request and merge.
- `python3 -m twine upload dist/*`
  - [PyPi](https://pypi.org/project/promoted-python-delivery-client/)
  - FUTURE: Do this with a Github Action.

## Dependencies

- [dataclasses-json](https://github.com/lidatong/dataclasses-json) -- flexible JSON serialization and deserialization of Python dataclasses. One key feature we use is the ability to omit None's (nulls) from request JSON to decrease payload size.
