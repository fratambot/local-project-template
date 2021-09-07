notebook:
	cd notebooks/ ; \
	poetry run jupyter notebook
.PHONY: notebook

lint:
	poetry run black .
	poetry run pylint models tests
.PHONY: lint

test:
	poetry run pytest -vv
.PHONY: test