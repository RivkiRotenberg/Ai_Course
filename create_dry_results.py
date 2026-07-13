import csv
from data import data as tsv_text

def parse_tsv(tsv_text):
    rows = [r.split('\t') for r in tsv_text.splitlines() if r.strip()]
    headers = rows[0]
    return headers, rows[1:]

def simulate_row(row, idx):
    # row layout: number, category, input, output, is_valid, notes
    number = row[0]
    category = row[1]
    instr = row[2]

    thought = f"1. ניתוח: זיהוי ישויות ובקשה; 2. סביבה: cmd; 3. אבטחה: בדיקה סטנדרטית" 
    shell = "CMD"
    command = f"echo " + '"SIM:{0}"'.format(idx)
    confidence = "6/10"
    risk = "green"
    compliance = "חסום (False)"

    return [number, category, instr, command, "לא נבדק", "", thought, shell, command, confidence, risk, compliance]

def main():
    headers, rows = parse_tsv(tsv_text)
    out_headers = [
        "מספר בדיקה", "קטגוריה", "הוראה (Input)", "Output (original)", "האם תקין (כן/לא)", "הערות",
        "ThoughtProcess", "SelectedShell", "Command", "Confidence", "Risk", "Compliance"
    ]

    out_rows = []
    for i, r in enumerate(rows, start=1):
        out_rows.append(simulate_row(r, i))

    out_path = "תיעוד_התהליך_dry_results.csv"
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(out_headers)
        writer.writerows(out_rows)

    print(f"Dry results written to {out_path}")

if __name__ == '__main__':
    main()
