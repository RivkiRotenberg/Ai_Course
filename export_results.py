import csv
from data import data as sheet_text

def parse_tsv(tsv_text):
    rows = [r.split('\t') for r in tsv_text.splitlines() if r.strip()]
    return rows

def export_csv(path="test_scenarios_export.csv"):
    rows = parse_tsv(sheet_text)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for r in rows:
            writer.writerow(r)
    print(f"Exported {len(rows)} rows to {path}")

if __name__ == '__main__':
    export_csv()
