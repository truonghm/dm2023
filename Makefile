pipc = ${HOME}/miniconda3/envs/pip-base/bin/python -m piptools compile
.PHONY: install clean lint format 

## Install for production
install:
	@echo ">> Installing dependencies"
	pip install -r requirements-project.txt

## Install for development 
install-dev: install
	pip install -r requirements-project-dev.txt

req-dev:
	$(pipc) --generate-hashes --output-file=requirements-project-dev.txt --extra=project --extra=dev pyproject.toml --resolver=backtracking

req:
	$(pipc) --generate-hashes --output-file=requirements-project.txt --extra=project pyproject.toml --resolver=backtracking

## Delete all temporary files
clean:
	py3clean .
	rm -rf .ruff_cache
	rm -rf .ipynb_checkpoints
	rm -rf **/.ipynb_checkpoints
	rm -rf .pytest_cache
	rm -rf **/.pytest_cache
	rm -rf __pycache__
	rm -rf **/__pycache__
	rm -rf build
	rm -rf dist

## Lint using ruff
ruff:
	ruff .

## Format files using black
format:
	black .
	ruff . --fix

## Run tests
test:
	pytest  --cov=project --cov-report=html --log-level=WARNING --disable-pytest-warnings

## Run checks (ruff + test)
check:
	ruff check .
	black --check .

## Get docker-compose log
log:
	docker-compose logs -f


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available commands:$$(tput sgr0)"
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')