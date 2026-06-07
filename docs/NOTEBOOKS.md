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

It compares:

- DEWA premise from property list
- DEWA premise from property detail
- DEWA premise from contract details
- DEWA premise from contract history
- useful fields from DEWA premise status check

Outputs are written to `runs/dewa_premise_audit_<timestamp>/`.

## `Owner_Assets_Contract_History_Comparison.ipynb`

Audit notebook for contract-history vs owner-assets consistency.

It filters contract history to active, pending, and termination-request contracts.

Expected matching:

- `OwnerContracts` should exist in owner-assets `owned` or `leased`.
- `TenantContracts` should exist in owner-assets `rented`.

Outputs are written to `runs/owner_assets_contract_history_comparison_<timestamp>/`.
