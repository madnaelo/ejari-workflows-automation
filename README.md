# Dubai Now Ejari Automation

Local Jupyter notebooks for DLD/DDA/Dubai Now Ejari workflows. The notebooks were adapted from Colab so the API calls run from a local network that can reach the staging DLD/DDA/DEWA endpoints.

## What Is Included

- `Ejari_Creation_Automation.ipynb` - main workflow notebook for contract creation, signing continuation, cancellation, termination, and DEWA diagnostics.
- `DEWA_Premise_Id_Audit.ipynb` - audit notebook for comparing DEWA premise IDs across property list, property detail, contract detail, contract history, success progress, and DEWA status responses; outputs property title, premise mismatch, and New/Renewal contract version columns.
- `Contract_Download_Audit.ipynb` - audit notebook for validating `downloadTenancyContract` and `download` endpoints for active, pending, and termination-request contracts.
- `Pending_Contract_Auto_Cancel_Audit.ipynb` - audit notebook for pending contracts that calculates 1-day and 5-day candidate auto-cancel dates from `OwnerContractSigningDate`.
- `Owner_Assets_Current_Contract_Audit.ipynb` - audit notebook for finding owner-assets coverage gaps from current contract history, recent progress successes, uploaded `progress.json`, or individual `success_*.json` files.
- `notebook_config.py` - shared Emirates ID configuration used by the notebooks.
- `notebook_operator_utils.py` - shared notebook UI helpers for popup option dialogs, Yes/No prompts, Emirates ID selection, and file pickers.
- `notebook_progress_utils.py` - shared progress/success JSON loading, validation, and merge helpers.
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
5. In `create` mode, optional per-property status control can stop contracts at pending owner sign, pending tenant sign, or pending payment.
6. Review run artifacts under `runs/<workflow>_<timestamp>/`.

## Audit Workflows

Use `Owner_Assets_Current_Contract_Audit.ipynb` to verify that properties appear in the expected owner-assets endpoints.

- Current contract-history mode checks active, pending, and termination-request contracts.
- Owner role expects the property in `owner-assets/owned/{2,3}` or `owner-assets/leased/{2,3}`.
- Tenant role expects the property in `owner-assets/rented/{2,3}`.
- Progress/success reference modes can use the newest run, uploaded `progress.json`, multiple uploaded progress files, or individual `success_*.json` files.
- When progress/success references are cross-checked with current contract history, the output includes both matching contract-history properties and unmatched progress/success reference properties.
- Problematic output rows are displayed in collapsed sections in the notebook. Expanding a section shows row JSON and owner-assets property-detail curl candidates for the missing endpoint side.

Use `DEWA_Premise_Id_Audit.ipynb` to verify DEWA premise IDs.

- It can audit the newest creation successes, uploaded progress/success files, or live API sources.
- Live API audit sources are selected with checkboxes: active contract history, non-pending contract history, and owner-assets leased/rented.
- Uploaded progress/success files can be selected with the native file picker; multiple valid files are merged before audit.

Use `Contract_Download_Audit.ipynb` to verify contract document download endpoints.

- It starts with Emirates ID `784195279540512`, then processes the other configured Emirates IDs.
- Pending contracts are checked with `downloadTenancyContract`.
- Active and termination-request contracts are checked with both `downloadTenancyContract` and `download`.
- Failed downloads produce matching curl and response files for API-team troubleshooting.

Use `Pending_Contract_Auto_Cancel_Audit.ipynb` to inspect pending contract auto-cancel timing.

- It filters contract history to pending contracts only.
- It loads contract details for each pending contract.
- It calculates `auto_cancel_1_day_date` and `auto_cancel_5_day_date` from `OwnerContractSigningDate` only.
- If `OwnerContractSigningDate` is missing, both auto-cancel date columns are blank and `autocancel_base_source` is marked `missing OwnerContractSigningDate`.

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
- Owner-assets audit property-detail curls use placeholder token values in notebook display, but generated runtime evidence may still contain sensitive identifiers.
- The main notebook uses `REQUEST_TIMEOUT_SECONDS` from `.env` when present; default is `90`.

## More Documentation

- [Notebook Guide](docs/NOTEBOOKS.md)
- [Operations Runbook](docs/OPERATIONS.md)
- [Security And Data Handling](docs/SECURITY.md)
- [GitHub Sync Notes](docs/GITHUB_SYNC.md)
