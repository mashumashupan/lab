VENV_NAME?=streamlit_csv
SOURCE=. $(VENV_NAME)/bin/activate &&
CSV_FILES=result/csv_files
HTML_FILES=result/html_files

.PHONY: local
local: ## run local env
	${SOURCE} streamlit run main.py

.PHONY: lint
lint: ## format all code
	${SOURCE} isort ./*.py
	${SOURCE} black ./*.py

.PHONY: install
install: # install developer requirements
	${SOURCE} pip3 install --upgrade pip
	${SOURCE} pip3 install -r requirements.txt

.PHONY: venv
venv: ## Create a virtualenv
	python3 -m venv $(VENV_NAME)

.PHONY: off
off: ## Deactivate a virtualenv
	deactivate

.PHONY: html
html: ## Generate html file from csv
	python3 graphParser.py


upload: ## Generate html file from csv
	git add .
	git commit -m "update files"
	git push

clean:
	 find ${CSV_FILES} ${HTML_FILES} -type f -delete

set:
	mv ../ga-graph/Koala-manygen/result/* ./result/csv_files