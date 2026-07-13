# CLI Agent - Prompt Engineering Project

מיני-פרויקט להמרת הוראות בשפה טבעית לשורת פקודה (Windows)

מה יש במאגר:
- `main.py` - אפליקציית Gradio שמשתמשת ב-OpenAI chat completions ומצפה לפלט JSON (ראה `system_prompt3.txt`).
- `safety.py` - בדיקות וסינון פקודות מסוכנות.
- `data.py` - תרחישי בדיקה מוכנים בגוף טקסט שניתן להעתיק לגיליון.
- `תיעוד התהליך.xlsx` - גיליון המקור עם תרחישי בדיקה (הוסיפי/י תוצאות לאחר ריצה).
- `batch_runner.py` - סקריפט שמריץ את הסוכן על כל שורה ב-Excel ומכניס את התוצאות חזרה.
- `export_results.py` - יצוא התרחישים ל-CSV/Excel עבור Google Sheets.
- `Dockerfile` + `run_in_container.sh` - sandbox מבוסס PowerShell להרצת פקודות מבודדות.
- `prompts_versions.md` - תיעוד כל פרומפטי האיטרציות.

מצב נוכחי ולמה זה עדיין לא "מושלם":
- ישנם כלים להשקה ולבדיקה, אך ה־batch שלא קורא ל‑API באופן אמיתי דורש התקנת pip והגדרת `OPENAI_API_KEY` לריצה אמיתית.
- חשוב שתעברי על תוצאות ה־dry-run ותאשרי אילו שורות יש להריץ בפועל.

שלבים להרצה ובדיקות (מומלץ לבצע בסדר זה):

1) יצירת סביבה והתקנת תלויות
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m ensurepip --upgrade
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) יצירת CSV מתוך התרחישים (לגוגל שיטס)
```powershell
python export_results.py
```

3) ריצה Dry (ללא קריאות ל‑OpenAI) — ממלא תוצאות מדומות שניתן לבדוק במהירות
```powershell
python batch_runner.py "תיעוד התהליך.xlsx" --dry
```

4) ריצה אמיתית (דורשת `OPENAI_API_KEY` מוגדרת בסביבה או בקובץ `.env`)
```powershell
$env:OPENAI_API_KEY="sk-..."
python batch_runner.py "תיעוד התהליך.xlsx"
```

5) בדקי את הקובץ שנשמר (`תיעוד_התהליך_with_results.xlsx`) וטעי את התוצאות בגיליון גוגל.

Docker sandbox - בניה והרצה (אופציונלי):
```powershell
docker build -t cli-agent-sandbox .
docker run --rm cli-agent-sandbox pwsh -NoProfile -Command "dir"
```

רשימת קבצים שיש לצרף להגשה:
- קוד מקור (`.py`), `requirements.txt`, `pyproject.toml`.
- כל גרסאות הפרומפט (`system_prompt*.txt`) או `prompts_versions.md`.
- גיליון הבדיקות עם תוצאות (CSV/Excel) ו־link ל‑Google Sheet.
- `failures_report.md` עם תובנות מהמבחנים.

רוצה שאפעל כך:
A) אבנה ואהריץ כאן את ה‑Docker sandbox בלבד (ללא עלות OpenAI).
B) אנסה להתקין pip ולהריץ את ה‑batch כאן עם ה‑OPENAI_API_KEY שלך (את צריכה לספק אותו או להוסיף `.env`).
C) אייצר עבורך את ה‑Excel המלא ב‑dry-run בלבד ואז תחליטי אילו שורות להריץ אמיתית.

ענה/י A, B או C ואפעל בהתאם.