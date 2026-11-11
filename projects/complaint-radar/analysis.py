"""Complaint Radar: where do banking complaints come from?
Reads data.csv (RBI Ombudsman Annual Report 2024-25 category shares) and prints a ranked view.
Run: python analysis.py   (Python 3, no extra packages)"""
import csv, pathlib

here = pathlib.Path(__file__).parent
rows = sorted(csv.DictReader(open(here / "data.csv")), key=lambda r: -float(r["share_pct_fy25"]))

for r in rows:
    s = float(r["share_pct_fy25"])
    print(f"{r['category']:<30}{s:>7.2f}%  " + "#" * round(s))

cc_fy25, growth = 50811, 0.2004
print(f"\nCredit card complaints FY25: {cc_fy25:,}")
print(f"Credit card complaints FY24 (derived): {cc_fy25/(1+growth):,.0f}")
