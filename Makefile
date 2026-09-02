.PHONY: quickstart generate test
generate:
	python src/generate_data.py

quickstart:
	python -m pip install -r requirements.txt
	python scripts/run.py
	@echo "Done. See reports/tables/, reports/figures/, and reports/anomaly_summary.md."

test:
	python -m pytest tests/ -v
