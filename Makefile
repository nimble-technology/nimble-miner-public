SHELL:=/bin/bash

.PHONY: install copy run

install:
	python3 -m venv nimenv_localminers && \
	source ./nimenv_localminers/bin/activate && \
	pip3 install -r requirements.txt

run:
ifndef addr
	$(error addr is not set.)
endif
	@echo "----------------------------------"
	@echo "Starting Process for Address $(addr)"
	
	source ./nimenv_localminers/bin/activate && \
	python execute.py $(addr)
	
	@echo "Process Completed for Address $(addr)"
	@echo "----------------------------------"

check:
	@echo "----------------------------------"
	@curl -X POST https://mainnet.nimble.technology:443/check_balance -H "Content-Type: application/json" -d '{"address": "$(addr)"}'
	@echo ""
	@echo "----------------------------------"
	
logs:
	@echo "----------------------------------"
	
	python showlogs.py
	
	@echo "----------------------------------"



