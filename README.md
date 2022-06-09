# promoted-python-delivery-client

Python client SDK for the Promoted.ai Delivery API

## Prereqs

- wheel
- setuptools
- twine

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
