# Operations Runbook

## Before Running

1. Confirm you are on the local network that can reach the staging APIs.
2. Confirm `.env` exists and has current values.
3. Start Jupyter with `.\start_jupyter.ps1`.
4. Open the required notebook.
5. Keep Excel closed for output CSV files that may be overwritten.

## Creation Checklist

1. Open `Ejari_Creation_Automation.ipynb`.
2. Run the shared setup/API cells.
3. Skip cancellation and termination unless needed.
4. Choose creation mode:
   - `curl` for API-team repro files only.
   - `create` for actual contract submission/signing.
5. Choose `fresh` when intentionally starting over.
6. Choose `resume` when continuing from `progress.json`.
7. For each owner Emirates ID, select the tenant profile when prompted.
8. Review `runs/ejari_creation_<timestamp>/successes` and `runs/ejari_creation_<timestamp>/failures`.

## Cancellation Checklist

1. Ensure `progress.json` contains the contracts you intend to cancel.
2. Run cancellation.
3. The notebook cancels progress-file contracts first.
4. If prompted, decide whether to fetch pending contracts from API and cancel them too.

## Termination Checklist

1. Run in `curl` mode first when validating payloads.
2. Use `terminate` mode only when ready to call write APIs.
3. Type `TERMINATE` when the notebook asks for explicit confirmation.
4. Review `progress-termination.json`, failure reports, and per-run detail files.

## Troubleshooting

- `Repository not found` while pushing: the current Git credentials do not have access to that GitHub repository, or the URL is wrong.
- `UnicodeDecodeError` reading JSON: ensure files are opened with UTF-8. The main notebook now does this for progress files.
- `401 Token Expired`: the request helper refreshes the iPaaS bearer token once and retries.
- Excel locks a CSV: close the CSV in Excel and rerun the report save step.
- API returns HTTP 200 with validation errors: the notebooks inspect response payload errors, not only HTTP status.

## Evidence To Share With API Teams

Use the generated `.sh` curl files and matching `_response_*.json` files under the run folder. These files may contain live tokens, so share them only with authorized API/support teams.
