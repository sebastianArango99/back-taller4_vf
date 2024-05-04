#
# Makefile
#

deps:
	@poetry --version &> /dev/null || (echo -e "ERROR: please install poetry" && false)
	poetry config virtualenvs.in-project true
	poetry env list
	poetry env info
	poetry install
	touch $@

run: ## run project in localhost web server
	poetry run uvicorn api.main:app --reload
