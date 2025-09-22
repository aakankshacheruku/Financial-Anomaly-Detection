.PHONY: quickstart
quickstart:
	python -m pip install -r requirements.txt
	python scripts/run.py
	@echo "Done. See reports/tables/ and reports/figures/."
