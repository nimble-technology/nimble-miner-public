SHELL:=/bin/bash

.PHONY: install copy run

install:
	python3 -m venv nimenv_localminers && \
	source ./nimenv_localminers/bin/activate && \
	pip3 install -r requirements.txt

run:
ifndef addressList
	$(error addressList (format : "nimble1xxxx nimble1yyyy" is not set.)
endif
	@echo "----------------------------------"
	@echo "Starting Process for Address List $(addressList)"
	
	source ./nimenv_localminers/bin/activate && \
	python execute.py $(addressList)
	
	@echo "Process Completed for Address List $(addressList)"
	@echo "----------------------------------"






