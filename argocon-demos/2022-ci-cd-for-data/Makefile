# Help
.PHONY: default
default:
	@echo "Please specify a build target. The choices are:"
	@echo "    spin-up:                    Create the ci example on a kubernetes cluster"
	@echo "    tear-down:                  Remove the ci example from kubernetes cluster"

.PHONY: spin-up
spin-up:
	@echo "============= Spinning-up CI example ============="
	kubectl apply -f bootstrap/argo-events/installation.yaml
	kubectl apply -f bootstrap/argo-workflows/installation.yaml
	kubectl apply -f bootstrap/argo-events/event-bus.yaml
	kubectl apply -f bootstrap/argo-events/github-access-secret.yaml
	kubectl apply -f bootstrap/argo-events/event-source.yaml
	kubectl apply -f bootstrap/argo-workflows/doubler-template.yaml
	kubectl apply -f bootstrap/argo-events/sensor.yaml

.PHONY: tear-down
tear-down:
	@echo "============= Tearing-down CI example ============="
	kubectl delete -f bootstrap/argo-events/sensor.yaml
	kubectl delete -f bootstrap/argo-workflows/doubler-template.yaml
	kubectl delete -f bootstrap/argo-events/event-source.yaml
	kubectl delete -f bootstrap/argo-events/github-access-secret.yaml
	kubectl delete -f bootstrap/argo-events/event-bus.yaml
	kubectl delete namespace argo-events
	kubectl delete namespace argo
