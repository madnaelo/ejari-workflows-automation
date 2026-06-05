# Ejari Automation Local Run

This notebook was adapted to run outside Google Colab so the DDA/DLD/DEWA APIs are called from your local network.

## Setup

1. Create a project-local virtual environment:

Run: `python -m venv .venv; .\.venv\Scripts\Activate.ps1`

2. Install dependencies:

Run: `pip install -r requirements.txt`

3. Copy `.env.example` to `.env` and fill in the same values that were previously stored in Colab secrets/userdata.

Run: `Copy-Item .env.example .env`

4. Start Jupyter locally:

Run: `.\start_jupyter.ps1`

The launcher uses `.venv` inside this project folder. If `.venv` is missing, it recreates it and installs `requirements.txt`.

Then open `Ejari_Creation_Automation.ipynb` and run the cells from your local machine.
