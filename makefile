all: lint test clean

.PHONY: lint
lint:
	@echo -e "\033[0;36m## start lint ############\033[0m"
	flake8 \
		--exclude venv \
		# --extend-ignore W605\
		# --max-line-length=130 

	@echo -e "\033[1;32m## lint success ! #########\033[0m"

.PHONY: test
test:
	@echo -e "\033[0;36m## start test #############\033[0m"

	python -m unittest main.py

	@echo -e "\033[1;32m test end \033[0m"

.PHONY: clean
clean:
	@echo -e "\033[0;36m## start clean ############\033[0m"

	# rm -r ./__pycache__
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	rm tmp/*.*

	@echo -e "\033[1;32m## cleaned ################\033[0m"
