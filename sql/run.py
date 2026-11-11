"""Builds portfolio.db from the project CSVs and runs every query in queries.sql.
Run from this folder:  python run.py     (Python 3 standard library only)
Open portfolio.db afterwards in DB Browser for SQLite to explore further."""
import csv, pathlib, sqlite3

here = pathlib.Path(__file__).parent
proj = here.parent / "projects"
db = here / "portfolio.db"
db.unlink(missing_ok=True)
con = sqlite3.connect(db)
con.executescript((here / "schema.sql").read_text())

def load(table, path, cols):
    rows = [[r[c] for c in cols] for r in csv.DictReader(open(path, encoding="utf-8"))]
    con.executemany(f"INSERT INTO {table} VALUES ({','.join('?' * len(cols))})", rows)

load("card_monthly", proj / "card-pulse/data.csv", ["month", "cards_outstanding_mn", "spend_inr_lakh_cr"])
load("issuer_apr2026", proj / "card-pulse/issuers_apr2026.csv", ["issuer", "spend_inr_cr", "cards_outstanding_mn", "spend_yoy_pct"])
load("upi_monthly", proj / "upi-credit/data.csv", ["month", "upi_volume_bn", "upi_value_inr_lakh_cr"])
load("ombudsman_fy25", proj / "complaint-radar/data.csv", ["category", "share_pct_fy25"])
con.commit()

def queries():
    title, buf = None, []
    for line in (here / "queries.sql").read_text().splitlines():
        if line.startswith("-- Q"):
            if title: yield title, "\n".join(buf).strip()
            title, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if title: yield title, "\n".join(buf).strip()

def run_all():
    out = []
    for title, sql in queries():
        cur = con.execute(sql)
        out.append((title, sql, [d[0] for d in cur.description], cur.fetchall()))
    return out

if __name__ == "__main__":
    for title, sql, cols, rows in run_all():
        print(f"\n== {title}")
        print(" | ".join(cols))
        for r in rows: print(" | ".join("" if v is None else str(v) for v in r))
