app: environment
	rm uv.lock

build:
	"tools/releasing/build.sh"

coverage:
	uv run tools/qa/coverage/update.sh

environment: uv.lock
	command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync

uv.lock: pyproject.toml
	uv lock

format:
	uv run tools/qa/format.sh

run_server:
	"src/bin/server.sh" -d

test: test_src test_qa

test_src:
	uv run pytest --cov=src --numprocesses=auto "tests/src"
	uv run python --version | cut -d. -f1,2 > "tools/qa/coverage/report.txt"
	uv run coverage report >> "tools/qa/coverage/report.txt"
	uv run coverage html --directory "tools/qa/coverage/html"

test_qa:
	uv run pytest --numprocesses=auto "tests/qa"

upload:
	"tools/releasing/upload.sh"

vscode: environment
	make test_src || true


.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
