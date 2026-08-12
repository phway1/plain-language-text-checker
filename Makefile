.PHONY: demo lint test
demo:
	PYTHONPATH=src python -m plaincheck.cli data/sample/synthetic_notice.txt --output reports
lint:
	PYTHONPATH=src python -m ruff check .
test:
	PYTHONPATH=src python -m pytest

