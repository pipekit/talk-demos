# Help
.PHONY: default
default:
	@echo "Please specify a build target. The choices are:"
	@echo "    image:                Build docker image"
	@echo "    image-m1:             Build docker image on an m1 mac"

.PHONY: image
image:
	@echo "============= Building docker image ============="
	docker build -t pipekit13/argocon21_dask ./workload

.PHONY: image-m1
image-m1:
	@echo "============= Building docker m1 image ============="
	docker buildx build --output=type=docker --platform=linux/amd64 -t pipekit13/argocon21_dask ./workload
