import streamlit as st
from utils.components import init_page

init_page('Database')

st.markdown("""
<div style="display:flex; gap:8px; align-items:center; margin-bottom:12px; flex-wrap:wrap;">
    <span style="background:#336791; color:white; padding:4px 14px; border-radius:20px; font-size:13px; font-weight:600;">PostgreSQL</span>
    <span style="background:#2a9d4e; color:white; padding:4px 14px; border-radius:20px; font-size:13px; font-weight:600;">Synthetic Data</span>
</div>
""", unsafe_allow_html=True)
st.caption("    All data is synthetically generated to simulate realistic Spotify listening behaviour.")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Tables", "5")
c2.metric("Users", "50")
c3.metric("Listens", "3,000")
c4.metric("Tracks", "499")
c5.metric("Artists", "73")

st.divider()

st.subheader("Table Definitions")
st.info('Each card below represents a table in the PostgreSQL database, showing its columns, data types, and key constraints (PK = Primary Key, FK = Foreign Key).')

TABLES = [
    {
        "name": "user",
        "rows": 50,
        "description": "Registered listeners on the platform.",
        "columns": [
            ("user_id", "UUID", "PK"),
            ("user_name", "TEXT", ""),
            ("birth_year", "INT", ""),
            ("nationality", "CHAR(2)", ""),
            ("gender", "CHAR(1)", ""),
            ("created_at", "DATE", ""),
        ],
    },
    {
        "name": "listens",
        "rows": 3000,
        "description": "One row per listen.",
        "columns": [
            ("user_id", "UUID", "FK → user"),
            ("track_id", "UUID", "FK → track"),
            ("timestamp", "TIMESTAMP", ""),
        ],
    },
    {
        "name": "track",
        "rows": 499,
        "description": "Tracks followed in this dataset.",
        "columns": [
            ("track_id", "UUID", "PK"),
            ("title", "TEXT", ""),
            ("duration_seconds", "INT", ""),
            ("artist_id", "UUID", "FK → artist"),
            ("feature_id", "UUID", "FK → artist (NULL)"),
            ("release_year", "INT", ""),
        ],
    },
    {
        "name": "artist",
        "rows": 73,
        "description": "Music artists who have tracks in the database.",
        "columns": [
            ("artist_id", "UUID", "PK"),
            ("artist_name", "TEXT", ""),
            ("artist_img", "TEXT", "URL"),
        ],
    },
    {
        "name": "favourites",
        "rows": 0,
        "description": "Locally stored favourites — artists or tracks saved in this app session.",
        "columns": [
            ("favourite_id", "UUID", "PK"),
            ("type",         "TEXT", "'artist' or 'track'"),
        ],
    },
]

PK_COLOR  = "#b45309"
FK_COLOR  = "#1d6fa4"
PKFK_COLOR = "#6d3fc0"

def badge(text: str, color: str) -> str:
    return (
        f'<span style="background:{color}; color:white; padding:1px 8px; '
        f'border-radius:10px; font-size:11px; margin-left:6px; '
        f'white-space:nowrap;">{text}</span>'
    )

def render_card(table: dict) -> None:
    rows_html = ""
    for col_name, col_type, note in table["columns"]:
        if "PK" in note and "FK" in note:
            b = badge(note, PKFK_COLOR)
        elif "PK" in note:
            b = badge("PK", PK_COLOR)
        elif "FK" in note:
            target = note.split("→")[-1].strip().split()[0] if "→" in note else ""
            nullable = "nullable" in note
            label = f"FK → {target}" + (" (nullable)" if nullable else "")
            b = badge(label, FK_COLOR)
        elif note:
            b = badge(note, "#4b5563")
        else:
            b = ""

        rows_html += (
            f'<div style="display:flex; justify-content:space-between; align-items:center; '
            f'padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.05);">'
            f'<span style="font-family:monospace; font-size:13px; color:#f1f5f9;">{col_name}{b}</span>'
            f'<span style="color:#94a3b8; font-size:12px; font-family:monospace;">{col_type}</span>'
            f'</div>'
        )

    st.markdown(
        f"""
        <div style="background:#1e293b; border:1px solid #334155; border-radius:12px;
                    padding:18px 20px; margin-bottom:15px; height:100%;">
            <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
                <span style="font-size:15px; font-weight:700; font-family:monospace; color:#f1f5f9;">{table['name']}</span>
                <span style="font-size:12px; color:#64748b;">{table['rows']:,} rows</span>
            </div>
            <div style="font-size:12px; color:#94a3b8; margin-bottom:10px;">{table['description']}</div>
            {rows_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

left, right = st.columns(2)

with left:
    render_card(TABLES[0])
    render_card(TABLES[2])

with right:
    render_card(TABLES[1])
    render_card(TABLES[3])
    render_card(TABLES[4])