# Spotify Insights

Spotify Insights is a DIS project by **kcf105** and **mwn201**.

The project consists of a Streamlit app that connects to a local PostgreSQL database and loads Spotify data from an Excel file into database tables. The data file is included in the repository.

## Requirements

To run the project locally, you need:

- Python 3.12 or newer
- PostgreSQL installed and running
- The project dependencies from `reqs.txt`

## Setup

Clone or download the project, then run the following inside the project folder.

### 1. Create and activate venv

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r reqs.txt
```

### 3. Set up the database connection

Create a `.env` file in the main project folder and add your PostgreSQL connection URL:

```env
DATABASE_URL=postgresql+psycopg2://localhost
```

If it doesnt load add your password like this:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost
```

## Run the app

Start the Streamlit app with:

```bash
python -m streamlit run app.py
```