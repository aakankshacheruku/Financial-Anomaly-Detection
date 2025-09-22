# Financial Anomaly Detection

Flag unusual transactions with a simple z-score baseline. I focused on clarity: a small sample, one CSV output of anomalies, and a quick histogram.

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
make quickstart
```

Outputs will appear in `reports/tables/` and `reports/figures/`.

## What I learned
- Keep calculations simple and NA-safe first, then iterate.
- Make small, testable steps and produce artifacts (CSV/PNG) every run.
- Write down decisions so future changes are easier to review.

## Decisions & next steps
- Start with a small sample so the pipeline is easy to run.
- This baseline is simple; next I want to compare IQR and robust z-scores, and experiment with rolling windows.
- Roadmap: expand data, add better metrics, and tighten tests as I go.

## Preview
After `make quickstart`, you should see a CSV table and one PNG in `reports/`.
![Amounts histogram (sample)](reports/figures/amount_hist.png)

