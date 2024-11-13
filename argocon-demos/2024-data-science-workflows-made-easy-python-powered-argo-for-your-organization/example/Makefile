.PHONY: run-offline
run-offline:
	poetry run -m ds_blog

.PHONY: run
run:
	@poetry export --without-hashes --without-urls > requirements.txt
	@docker build . -t ds-blog:v1
	poetry run python -m ds_blog

.PHONY: install
install:
	@./install.sh
	poetry install

.PHONY: add-data
add-data:  ## Minio must be port-forwarded before running
	@mc alias set localminio http://localhost:9000 argoproj sup3rs3cr3tp4ssw0rd1
	@mc put assets/diabetes.csv localminio/workflows/diabetes.csv

.PHONY: format
format: ## Format and sort imports for source, tests, examples, etc.
	@poetry run ruff format .
	@poetry run ruff check . --fix
