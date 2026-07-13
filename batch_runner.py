import argparse
import pandas as pd
import time
import os

from safety import sanitize_or_block

# Note: import `generate_cli_advanced` lazily when not running dry to avoid
# importing OpenAI/OpenAI client during dry runs or when dependencies missing.


def detect_input_column(df: pd.DataFrame):
    for c in df.columns:
        if isinstance(c, str) and ("הוראה" in c or "Input" in c or "input" in c):
            return c
    # fallback: choose first column with object dtype
    for c in df.columns:
        if df[c].dtype == object:
            return c
    return df.columns[0]


def run_batch(input_path, sheet_name=None, output_path=None, delay=1.0, limit=None, dry=False):
    print(f"Loading '{input_path}'...")
    df = pd.read_excel(input_path, sheet_name=sheet_name)
    # pandas.read_excel can return a dict if sheet_name=None or multiple sheets.
    if isinstance(df, dict):
        if sheet_name and sheet_name in df:
            df = df[sheet_name]
        else:
            # pick the first sheet
            first_key = list(df.keys())[0]
            print(f"Multiple sheets found, using first sheet: {first_key}")
            df = df[first_key]

    input_col = detect_input_column(df)
    print(f"Detected input column: {input_col}")

    # Prepare output columns
    out_cols = ["ThoughtProcess", "SelectedShell", "Command", "Confidence", "Risk", "Compliance"]
    for c in out_cols:
        if c not in df.columns:
            df[c] = ""

    rows = df.shape[0]
    to_run = rows if limit is None else min(rows, limit)

    for i in range(to_run):
        instr = str(df.at[i, input_col]) if pd.notna(df.at[i, input_col]) else ""
        if not instr.strip():
            print(f"Row {i+1}: empty input, skipping")
            continue

        print(f"Row {i+1}/{to_run}: running instruction: {instr[:60]}")

        if dry:
            # Simulate a structured response without calling OpenAI
            thought = f"1. ניתוח: סימולציה עבור שורה {i+1}\n2. סביבה: cmd\n3. אבטחה: בדיקה בסיסית"
            shell = "CMD"
            command = f"echo 'SIMULATED: {instr[:40].replace("'", '')}'"
            confidence = "5/10"
            risk = "YELLOW"
            compliance = "חסום (False)"
            result = (thought, shell, command, confidence, risk, compliance)
        else:
            # Lazy import to avoid dependency issues during dry runs
            from main import generate_cli_advanced
            result = generate_cli_advanced(instr)
        # generate_cli_advanced returns 6 values in current implementation
        try:
            thought, shell, command, confidence, risk, compliance = result
        except Exception:
            # unexpected shape — store raw repr
            df.at[i, "ThoughtProcess"] = "ERROR"
            df.at[i, "SelectedShell"] = "ERROR"
            df.at[i, "Command"] = str(result)
            continue

        # ensure safety
        blocked, cleaned_or_msg = sanitize_or_block(command)
        if blocked:
            command_out = cleaned_or_msg
            shell_out = "BLOCKED"
        else:
            command_out = cleaned_or_msg
            shell_out = shell

        df.at[i, "ThoughtProcess"] = thought
        df.at[i, "SelectedShell"] = shell_out
        df.at[i, "Command"] = command_out
        df.at[i, "Confidence"] = confidence
        df.at[i, "Risk"] = risk
        df.at[i, "Compliance"] = compliance

        # polite delay to avoid rate limits
        time.sleep(delay)

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_with_results.xlsx"

    df.to_excel(output_path, index=False)
    print(f"Saved results to {output_path}")


def main():
    p = argparse.ArgumentParser(description="Batch run CLI agent over Excel scenarios")
    p.add_argument("input", help="Input Excel file path")
    p.add_argument("--sheet", help="Sheet name (optional)")
    p.add_argument("--out", help="Output Excel file path (optional)")
    p.add_argument("--delay", type=float, default=1.0, help="Delay between requests (s)")
    p.add_argument("--limit", type=int, help="Limit number of rows to run")
    p.add_argument("--dry", action="store_true", help="Dry run without calling OpenAI (simulate results)")
    args = p.parse_args()

    run_batch(args.input, sheet_name=args.sheet, output_path=args.out, delay=args.delay, limit=args.limit, dry=args.dry)


if __name__ == '__main__':
    main()
