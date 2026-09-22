.DEFAULT_GOAL := build

app: environment
	rm Makefile uv.lock

build: uv.lock
	"tools/releasing/build.sh"

coverage: uv
	uv run tools/qa/coverage/update.sh

# Namespace to deploy into (override with: make deploy NAMESPACE=myns)
NAMESPACE ?= photostream
K8S_DIR := tools/deployment/kubernetes

deploy:
	kubectl kustomize "$(K8S_DIR)" \
	    | sed "s/namespace: photostream/namespace: $(NAMESPACE)/g" \
	    | kubectl apply -f -
	kubectl rollout restart deployment/photostream -n "$(NAMESPACE)"


environment: uv uv.lock
	uv sync

uv:
	command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh

uv.lock: pyproject.toml uv
	uv lock

format: uv
	uv run tools/qa/format.sh

run_server:
	"src/bin/server.sh" -d

test: test_src test_qa

test_src: uv
	uv run pytest --cov=src --numprocesses=auto "tests/src"
	uv run python --version | cut -d. -f1,2 > "tools/qa/coverage/report.txt"
	uv run coverage report >> "tools/qa/coverage/report.txt"
	uv run coverage html --directory "tools/qa/coverage/html"

test_qa: uv
	uv run pytest --numprocesses=auto "tests/qa"

upload:
	"tools/releasing/upload.sh"

vscode: environment
	make test_src || true


.PHONY: app build coverage deploy environment uv format run_server test test_src test_qa upload vscode help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
