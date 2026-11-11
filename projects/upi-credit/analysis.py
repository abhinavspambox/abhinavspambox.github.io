"""UPI x Credit: how big is everyday UPI spending next to credit cards?
Reads data.csv (NPCI monthly UPI statistics, Jan-Oct 2026) and ../card-pulse/data.csv (RBI card spend).
Run: python analysis.py   (Python 3, no extra packages)"""
import csv, pathlib

here = pathlib.Path(__file__).parent
upi = list(csv.DictReader(open(here / "data.csv")))
cards = {r["month"]: float(r["spend_inr_lakh_cr"]) for r in csv.DictReader(open(here.parent / "card-pulse" / "data.csv"))}

print(f"{'Month':<9}{'Volume (bn)':>12}{'Value (L cr)':>14}{'Avg ticket (Rs)':>17}{'UPI / cards':>13}")
for r in upi:
    vol, val = float(r["upi_volume_bn"]), float(r["upi_value_inr_lakh_cr"])
    ticket = val * 1e12 / (vol * 1e9)
    ratio = f"{val / cards[r['month']]:.1f}x" if r["month"] in cards else "-"
    print(f"{r['month']:<9}{vol:>12.2f}{val:>14.2f}{ticket:>17,.0f}{ratio:>13}")

a, b = upi[0], upi[-1]
print(f"\nVolume growth {a['month']} -> {b['month']}: {float(b['upi_volume_bn'])/float(a['upi_volume_bn'])-1:+.1%}")
print(f"Value growth  {a['month']} -> {b['month']}: {float(b['upi_value_inr_lakh_cr'])/float(a['upi_value_inr_lakh_cr'])-1:+.1%}")
