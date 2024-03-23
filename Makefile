SHELL:=/bin/bash

.PHONY: install copy run

install:
	python3 -m venv nimenv_localminers && \
	source ./nimenv_localminers/bin/activate && \
	pip3 install -r requirements.txt

run:
ifndef addressList
	$(error address list (format : addressList="nimble1xxxx nimble1yyyy") is not set.)
endif
	@echo "----------------------------------"
	@echo "Starting Process for addresses $(addressList)"
	
	source ./nimenv_localminers/bin/activate && \
	python execute.py $(addressList)
	
	@echo "Process Completed for addresses $(addressList)"
	@echo "----------------------------------"






