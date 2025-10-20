import json, argparse, datetime as dt
from pathlib import Path

REQ = ["title","domain","subdomain","audience","format","status","author","last_updated"]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--min-freshness-days", type=int, default=90)
    args = p.parse_args()

    data = json.loads(Path(args.input).read_text())
    today = dt.date.today()
    bad = []
    for i, rec in enumerate(data):
        missing = [k for k in REQ if k not in rec]
        try:
            d = dt.date.fromisoformat(rec.get("last_updated","1970-01-01"))
        except Exception:
            d = dt.date(1970,1,1)
        stale = (today - d).days > args.min_freshness_days
        if missing or stale:
            bad.append({"index": i, "missing": missing, "stale": stale})
    if bad:
        print("quality_issues=", bad)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
