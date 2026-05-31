# SauceDemo Automation – Python Makefile targets
# Requires: make, python3, pip, allure CLI

VENV        = .venv
PYTHON      = $(VENV)/bin/python
PIP         = $(VENV)/bin/pip
PYTEST      = $(VENV)/bin/pytest
RESULTS_DIR = allure-results
REPORT_DIR  = allure-report

.PHONY: install install-browsers test-q1 test-q2 test-q3 test-all report clean

## Install Python dependencies and Playwright browsers
install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PYTHON) -m playwright install chromium

## Run Q1 only (locked_out_user)
test-q1:
	$(PYTEST) tests/test_q1_locked_out_user.py -v
	allure generate $(RESULTS_DIR) --clean -o $(REPORT_DIR)

## Run Q2 only (standard_user)
test-q2:
	$(PYTEST) tests/test_q2_standard_user.py -v
	allure generate $(RESULTS_DIR) --clean -o $(REPORT_DIR)

## Run Q3 only (performance_glitch_user)
test-q3:
	$(PYTEST) tests/test_q3_performance_glitch_user.py -v
	allure generate $(RESULTS_DIR) --clean -o $(REPORT_DIR)

## Run ALL tests sequentially (Q1 → Q2 → Q3)
test-all:
	$(PYTEST) tests/test_q1_locked_out_user.py \
	          tests/test_q2_standard_user.py \
	          tests/test_q3_performance_glitch_user.py -v
	allure generate $(RESULTS_DIR) --clean -o $(REPORT_DIR)

## Generate and open the Allure HTML report (no test run)
report:
	allure generate $(RESULTS_DIR) --clean -o $(REPORT_DIR)
	allure open $(REPORT_DIR)

## Remove generated artifacts
clean:
	rm -rf $(RESULTS_DIR) $(REPORT_DIR) .pytest_cache __pycache__ tests/__pycache__ pages/__pycache__
