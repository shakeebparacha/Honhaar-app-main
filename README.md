# Student Account Manager

A Streamlit app for collecting student or guardian account information based on age, with an admin dashboard and CSV export.

## Features
- Student submissions with a reference number
- Guardian submissions for age 18 and under
- Admin login with dashboard, filtering, and CSV export
- Local JSON storage

## Installation

1. Use Python 3.11
2. Install requirements:
```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Data Storage

Data is stored in `student_data.json` in the app directory.
On Streamlit Community Cloud, the filesystem is ephemeral, so data can be lost on redeploys or restarts.

## Deployment (Streamlit Cloud)

The app pins Python 3.11 via `runtime.txt` and installs dependencies from `requirements.txt`.

## Requirements

- Python 3.11
- Streamlit 1.35.0
- Pandas 2.2.2
