import re

# רשימת דפוסים מסוכנים המחייבים חסימה מידית
_DANGEROUS_PATTERNS = [
    r"rm\s+-rf",
    r"format\s+C:",
    r"format\s+C:\\",
    r"delete\s+C:\\",
    r"remove-psdrive",
    r"shutdown",
    r"poweroff",
    r"stop-computer",
    r"del\s+.*C:\\",
    r"remove-item\s+-recurse\s+-force\s+C:\\",
    r"change-password",
]


def is_dangerous(command: str) -> bool:
    if not command:
        return False
    cmd = command.lower()
    for p in _DANGEROUS_PATTERNS:
        if re.search(p, cmd):
            return True
    # חיפוש ישיר של הוראות למחיקה של כל הכונן
    if "delete c:" in cmd or "format c:" in cmd or ("מחוק" in cmd and "c:" in cmd):
        return True
    return False


def sanitize_or_block(command: str):
    """מנסה לנקות את הפקודה ולהחזיר (blocked: bool, cleaned_command: str).
    אם זוהתה פקודה מסוכנת מוחזרת הודעת חסימה.
    """
    if not command:
        return False, ""

    # הסרת תווי שליטה ו-newlines - בודקים שורת פקודה אחת בלבד
    cleaned = command.replace("\r", "").strip()
    # אם יש שורות מרובות - שומרים רק את הראשונה
    if "\n" in cleaned:
        cleaned = cleaned.splitlines()[0].strip()

    # בדיקת סיכונים בסיסית
    if is_dangerous(cleaned):
        return True, "נחסם מטעמי אבטחה"

    # ממשק פשוט לבדיקת תוים לא רצויים
    if not re.match(r"^[\x20-\x7E\u0590-\u05FF\\/:._\-\s]+$", cleaned):
        # תווים לא צפויים - נחסום כנקיטת זהירות
        return True, "נחסם מטעמי אבטחה"

    return False, cleaned


def basic_syntax_ok(command: str) -> bool:
    if not command:
        return False
    # אסור newlines מרובות
    if "\n" in command:
        return False
    # אסור פייפינג מורכב כאן (פירוש: לבדיקה פשוטה בלבד)
    return True
