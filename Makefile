build:
	python setup.py bdist_wheel

test:
	pytest tests/

install_local:
	pip install dist/promoted_python_delivery_client-2.1.1-py3-none-any.whl --force-reinstall

uninstall_local:
	pip uninstall dist/promoted_python_delivery_client-2.1.1-py3-none-any.whl
