import zipfile
import os

INCLUDE = [
    "main.py",
    "safety.py",
    "data.py",
    "batch_runner.py",
    "export_results.py",
    "create_dry_results.py",
    "Dockerfile",
    "run_in_container.sh",
    "prompts_versions.md",
    "system_prompt.txt",
    "system_prompt2.txt",
    "system_prompt3.txt",
    "failures_report.md",
    "תיעוד_התהליך_dry_results.csv",
    "תיעוד התהליך_with_results.xlsx",
    "requirements.txt",
    "pyproject.toml",
]

def make_zip(out_name="submission.zip"):
    with zipfile.ZipFile(out_name, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in INCLUDE:
            if os.path.exists(f):
                z.write(f)
            else:
                print(f"Warning: {f} not found, skipping")
    print(f"Created {out_name}")

if __name__ == '__main__':
    make_zip()
