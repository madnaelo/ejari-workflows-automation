# Notebook Guide

## `Ejari_Creation_Automation.ipynb`

Main operational notebook.

Sections:

- Shared helpers, prompts, and run artifact logging
- API definitions, config, storage, and shared workflow helpers
- Contract cancellation
- Contract termination
- Contract creation and signing
- DEWA premise diagnostic

Important modes:

- `no` - skip that section.
- `curl` - build request curl files without calling the write API.
- `create` - submit contract creation and continue signing.
- `terminate` - call termination APIs after explicit confirmation.

Most Yes/No and menu prompts use shared popup selectors from `notebook_operator_utils.py`. Free-text prompts such as email, DOB, max count, and explicit `TERMINATE` confirmation remain typed inputs.

Creation flow summary:

1. Load vacant properties from owner-assets `vacant/2` and `vacant/3`.
2. Validate property.
3. Fetch tenant details from the tenant API.
4. Submit or log API5 create request.
5. Load contract details and property details after submission.
6. Download pending contract document.
7. Sign as owner.
8. Sign as tenant using tenant token when needed.
9. Save success/failure detail files and reports.

Termination flow summary:

1. Load leased/rented contract candidates.
2. Load contract details.
3. Derive a valid termination date from contract start/end date.
4. Submit owner termination or write curl only.
5. Attempt tenant approval depending on the configured token mode.
6. Save progress, success/failure JSON, and failure CSV.

## `DEWA_Premise_Id_Audit.ipynb`

Audit notebook for DEWA premise consistency.

Supported input modes:

- Most recent Ejari creation `progress.json` successes.
- Uploaded one or more `progress.json` or success-reference files.
- Live API audit sources selected with checkboxes:
  - contract history, only active
  - contract history, all other than pending
  - owner-assets leased plus rented

The uploaded-file path uses the shared native file picker and defaults to the project folder. Multiple valid files are merged before audit.

It compares:

- DEWA premise from property list
- DEWA premise from property detail
- DEWA premise from contract details
- DEWA premise from contract history
- useful fields from DEWA premise status check

Outputs are written to `runs/dewa_premise_audit_<timestamp>/`.

## `Owner_Assets_Current_Contract_Audit.ipynb`

Audit notebook for contract-history vs owner-assets consistency.

Supported input modes:

- Current contract history.
- Most recent Ejari creation `progress.json` successes.
- Uploaded one or more `progress.json` or individual `success_*.json` files.

Current contract-history mode filters contract history to active, pending, and termination-request contracts.

Expected matching:

- `OwnerContracts` should exist in owner-assets `owned` or `leased`.
- `TenantContracts` should exist in owner-assets `rented`.
- If the same property is both owner and tenant in current contract history, both sides are checked.

Cross-reference behavior:

- In current contract-history mode, the user can also select a progress/success reference file. The output then includes both contract-history rows and unmatched progress/success rows.
- In progress/success modes, the user can cross-check against current contract history. If a matching tenant contract is active, pending, or termination-request, rented owner-assets is checked too.
- Summary output includes counts for problematic properties present in current contract history and present in progress/success references.

Problematic row display:

- Notebook output renders problematic rows as collapsed expandable sections.
- The section title shows Emirates ID, property ID, property title, and property row value.
- Expanding the row shows collapsible JSON and collapsible owner-assets property-detail curl candidates for the missing endpoint side.
- The same curl candidates are saved in `Problematic property detail curl(s)` in CSV/JSON outputs.

Outputs are written to `runs/current_contract_owner_assets_audit_<timestamp>/` or `runs/success_reference_owner_assets_audit_<timestamp>/`.

## Shared Python Helpers

- `notebook_config.py` centralizes configured Emirates IDs.
- `notebook_operator_utils.py` provides popup option dialogs, checkbox multi-select, Yes/No prompts, Emirates ID selection, and file pickers. If popups are unavailable, it falls back to typed input.
- `notebook_progress_utils.py` validates and merges progress/success files. It accepts `progress.json` files and individual `success_*.json` files, wrapping success detail files into the same success-reference structure.
