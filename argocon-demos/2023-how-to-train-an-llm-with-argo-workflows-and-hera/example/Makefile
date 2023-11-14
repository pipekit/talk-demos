IMAGE_NAME="flaviuvadan/kubecon-na-23-finetune-llama2"

.PHONY: help
help: ## Showcase the help instructions for all the available `make` commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: format
format: ## Format and sort imports for source, tests, examples, etc.
	@poetry run black .
	@poetry run ruff . --fix

.PHONY: image
image: ## Build the Docker image
	@docker buildx build --platform linux/amd64 --push -t $(IMAGE_NAME):latest .