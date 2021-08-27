coverage:
	poetry run tools/qa/coverage/update.sh

format:
	poetry run tools/qa/format.sh

install: poetry.lock
	command -v poetry || pip install poetry
	poetry install
	make test_src || true

test: test_src test_qa

test_src:
	poetry run pytest --cov=src --numprocesses=auto "tests/src"
	poetry run python --version | cut -d. -f1,2 > "tools/qa/coverage/report.txt"
	poetry run coverage report >> "tools/qa/coverage/report.txt"
	poetry run coverage html --directory "tools/qa/coverage/html"

test_qa:
	poetry run pytest --numprocesses=auto "tests/qa"

package:
	"tools/releasing/package.sh"

upload:
	"tools/releasing/upload.sh"
