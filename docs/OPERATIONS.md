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
7. In `create` mode, choose whether to control individual property contract statuses.
8. If individual control is enabled, choose a target for each property:
   - `pending_owner_sign` stops after API5 creation and read-only detail checks.
   - `pending_tenant_sign` signs owner only.
   - `pending_payment` signs owner and tenant, then stops before payment.
9. To advance a previously stopped contract, enable `Continue signing previously created pending contracts from API` and choose the later target status when prompted.
10. For each owner Emirates ID, select the tenant profile when prompted.
11. Review `runs/ejari_creation_<timestamp>/successes` and `runs/ejari_creation_<timestamp>/failures`.

## Owner-Assets Audit Checklist

1. Open `Owner_Assets_Current_Contract_Audit.ipynb`.
2. Run configuration, authentication, normalization, API, comparison, and run cells from the top.
3. Choose the audit source:
   - `Current contract-history audit` for fresh active, pending, and termination-request contract-history properties.
   - `Most recent progress.json successes` for the newest successful Ejari creation run under `runs/`.
   - `Select progress/success JSON file(s)` for one or more `progress.json` or `success_*.json` files.
4. If running current contract-history audit, decide whether to also compare against progress/success references.
5. If running progress/success references, decide whether to cross-verify against current contract history. Choose `Yes` when tenant-side rented checks should be driven by current pending/active/termination-request tenant contracts.
6. Select all configured Emirates IDs or approve them one by one.
7. Review summary counts:
   - `problematic_properties`
   - `problematic_properties_present_in_contract_history`
   - `problematic_properties_present_in_progress_success`
8. Expand problematic rows in notebook output to inspect JSON and owner-assets property-detail curl candidates.

Owner-assets audit outputs are written under either:

- `runs/current_contract_owner_assets_audit_<timestamp>/`
- `runs/success_reference_owner_assets_audit_<timestamp>/`

Key files:

- `problematic_current_contract_properties.csv`
- `problematic_success_reference_properties.csv`
- `summary.csv`
- `errors.csv`

## DEWA Audit Checklist

1. Open `DEWA_Premise_Id_Audit.ipynb`.
2. Choose one of the source modes:
   - newest progress successes
   - uploaded progress/success files
   - live API audit
3. For live API audit, select one or more checkbox sources:
   - contract history only active
   - contract history all other than pending
   - owner-assets leased plus rented
4. For uploaded inputs, use the file picker. Multiple selected files are merged before audit.
5. Select all configured Emirates IDs or approve them one by one.
6. Review generated CSV/JSON output under `runs/dewa_premise_audit_<timestamp>/` or `runs/dewa_premise_audit_successes_<timestamp>/`.
7. Check `dewa_premise_id_mismatch` and `dewa_premise_id_mismatch_detail` for premise IDs that differ across property detail, contract details, contract history, property lists, success progress, or the DEWA status response. Use `contract_version_type` to distinguish `New` from `Renewal` contracts.

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
- Popup UI does not appear: the shared helpers fall back to typed input. For file inputs, paste one or more paths separated by commas or semicolons.
- Current contract-history audit shows zero current rows for an Emirates ID: if a progress/success reference was selected, check `progress_success_properties` and `Output comparison properties`; unmatched progress/success rows are still emitted.
- A problematic owner-assets row is hard to inspect: expand the row in notebook output, then expand `Row JSON` and `Problematic property-detail curl(s)`.

## Evidence To Share With API Teams

Use the generated `.sh` curl files and matching `_response_*.json` files under the run folder. These files may contain live tokens, so share them only with authorized API/support teams.
