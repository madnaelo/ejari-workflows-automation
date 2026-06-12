# Security And Data Handling

## Secrets

Secrets are loaded from `.env` locally or Colab userdata when running in Colab-like environments.

Required core values:

- `BASIC_AUTH`
- `CONSUMER_ID`
- `IDS_BASE_URL`
- `DLD_BASE_URL`
- `DLD_PROXY_URL`

DEWA values are required only for DEWA diagnostic/audit workflows:

- `DEWA_BASE_URL`
- `DEWA_CLIENT_ID`
- `DEWA_CLIENT_SECRET`
- `DEWA_VENDOR_ID`

Optional:

- `REQUEST_TIMEOUT_SECONDS`

## Git Ignore Policy

The repository ignores local secrets and runtime artifacts:

- `.env`
- `.venv/`
- `runs/`
- `progress*.json`
- `failure_report*.csv`
- `failure_report*.json`
- Jupyter logs/checkpoints

Do not override this unless there is an explicit, reviewed reason.

## Token Handling

Progress-style notebook logs redact token and secret fields.

Curl repro files intentionally keep full headers because the API team needs reproducible requests. Treat curl files as sensitive operational evidence.

Owner-assets audit notebook display generates property-detail curl candidates with placeholder token values:

- `<IPAAS_BEARER_TOKEN>`
- `<DLD_TOKEN_FOR_EID_...>`

These displayed curl candidates are still sensitive because they include Emirates IDs, property row values, property IDs, and endpoint paths. The user must replace placeholders with valid operational tokens before running them.

## Data Classification

Run outputs may include:

- Emirates IDs
- property IDs and row values
- tenant details
- contract row values and numbers
- contract document download metadata and response samples
- DLD/DDA/DEWA response payloads
- bearer/DLD tokens in curl files
- owner-assets property-detail curl candidates with token placeholders

Store and share these files according to Datacell/DDA handling rules.

## Progress And Success Inputs

Audit notebooks can load:

- run-level `progress.json` files
- individual `success_*.json` detail files
- merged progress/success reference files created under `runs/`

These files contain property identifiers, contract numbers, tenant contact fields, and API responses. They remain ignored by git and should be shared only as approved operational evidence.

## Audit Evidence

Contract download and pending auto-cancel audit notebooks write raw API evidence under `runs/`.

- Contract download failures may include curl files with live bearer/DLD headers.
- Pending auto-cancel evidence includes contract-history and contract-detail payloads.
- Auto-cancel reports use `OwnerContractSigningDate` only; stale exploratory files that used unrelated date fields should be deleted and not shared.

Keep `runs/` ignored by git and share only the minimum files needed for the support question.
