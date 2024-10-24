# Help
.PHONY: default
default:
	@echo "Please specify a build target. The choices are:"
	@echo "    image:                Build docker image"
	@echo "    image-m1:             Build docker image on an m1 mac"

.PHONY: install
install: image image-m1
	kubectl config set-context docker-desktop
	kubectl apply -f installation.yaml
	kubectl apply -f dask_standard_cluster_workflow_template.yaml
	kubectl apply -f dask_workflow_template.yaml

.PHONY: image
image:
	@echo "============= Building docker image ============="
	docker build -t local-docker/argocon21_dask ./workload

.PHONY: image-m1
image-m1:
	@echo "============= Building docker m1 image ============="
	docker buildx build --output=type=docker --platform=linux/amd64 -t local-docker/argocon21_dask ./workload
