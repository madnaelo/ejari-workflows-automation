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

## Data Classification

Run outputs may include:

- Emirates IDs
- property IDs and row values
- tenant details
- contract row values and numbers
- DLD/DDA/DEWA response payloads
- bearer/DLD tokens in curl files

Store and share these files according to Datacell/DDA handling rules.
