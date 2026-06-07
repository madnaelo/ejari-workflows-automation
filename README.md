# Dubai Now Ejari Automation

Local Jupyter notebooks for DLD/DDA/Dubai Now Ejari workflows. The notebooks were adapted from Colab so the API calls run from a local network that can reach the staging DLD/DDA/DEWA endpoints.

## What Is Included

- `Ejari_Creation_Automation.ipynb` - main workflow notebook for contract creation, signing continuation, cancellation, termination, and DEWA diagnostics.
- `DEWA_Premise_Id_Audit.ipynb` - audit notebook for comparing DEWA premise IDs across property list, property detail, contract detail, and contract history responses.
- `Owner_Assets_Contract_History_Comparison.ipynb` - audit notebook for finding active/pending/termination-request contract-history properties missing from the expected owner-assets lists.
- `start_jupyter.ps1` - local Jupyter launcher.
- `requirements.txt` - Python/Jupyter dependencies.
- `.env.example` - required environment variable template.

## Setup

Run these commands from the project folder.

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Fill `.env` with the values previously stored in Colab secrets/userdata.

Start Jupyter:

```powershell
.\start_jupyter.ps1
```

Then open the notebook you need.

## Normal Workflow

Use `Ejari_Creation_Automation.ipynb` for day-to-day Ejari processing.

1. Run the shared setup/API cells from the top.
2. Choose whether to run cancellation, termination, creation/signing, or DEWA diagnostic sections when prompted.
3. Use `curl` mode when you only want reproducible API request files without creating or terminating contracts.
4. Use `create` or `terminate` modes only when you intend to call the write APIs.
5. Review run artifacts under `runs/<workflow>_<timestamp>/`.

## Outputs And Resume Files

Runtime files are intentionally ignored by git:

- `runs/`
- `progress*.json`
- `failure_report*.csv`
- `failure_report*.json`
- Jupyter logs and checkpoints

`progress.json` is the current creation progress/resume file. Timestamped copies under `runs/` preserve per-run evidence.

`progress-termination.json` is the termination progress/resume file.

## Security Notes

- Do not commit `.env`, progress files, failure reports, or run output folders.
- Notebook progress-style logs redact tokens/secrets.
- Curl repro files intentionally keep full request headers because they are used for API-team troubleshooting. Treat them as sensitive and share only with authorized recipients.
- The main notebook uses `REQUEST_TIMEOUT_SECONDS` from `.env` when present; default is `90`.

## More Documentation

- [Notebook Guide](docs/NOTEBOOKS.md)
- [Operations Runbook](docs/OPERATIONS.md)
- [Security And Data Handling](docs/SECURITY.md)
- [GitHub Sync Notes](docs/GITHUB_SYNC.md)
