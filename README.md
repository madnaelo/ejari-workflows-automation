# Ejari Automation Local Run

This notebook was adapted to run outside Google Colab so the DDA/DLD/DEWA APIs are called from your local network.

## Setup

1. Create a virtual environment:

```powershell
python -m venv E:\codex_work\venvs\DLD-Ejari-CheckDDAData
E:\codex_work\venvs\DLD-Ejari-CheckDDAData\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in the same values that were previously stored in Colab secrets/userdata.

```powershell
Copy-Item .env.example .env
```

4. Start Jupyter locally:

```powershell
.\start_jupyter.ps1
```

Then open `Ejari_Creation_Automation.ipynb` and run the cells from your local machine.
