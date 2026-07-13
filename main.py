import os
import json
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from safety import sanitize_or_block

load_dotenv()
client = OpenAI()

def load_system_prompt(file_path="system_prompt3.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "אתה עוזר טכני שמחזיר JSON."

SYSTEM_PROMPT = load_system_prompt()

def generate_cli_advanced(user_instruction):
    if not user_instruction.strip():
        return "בבקשה הזן הוראה.", "", "", "", "", ""
        
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,  # טמפרטורה נמוכה לשמירה על מבנה JSON תקין
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_instruction}
            ]
        )
        
        raw_output = response.choices[0].message.content.strip()

        try:
            data = json.loads(raw_output)

            # עיבוד תהליך החשיבה מתוך תתי-השדות ב-JSON
            thought_data = data.get("thoughtProcess", {})
            thought_steps_list = [
                f"1. ניתוח: {thought_data.get('step1_analysis', '-')}",
                f"2. סביבה: {thought_data.get('step2_environment', '-')}",
                f"3. אבטחה: {thought_data.get('step3_safety_check', '-')}"
            ]
            thought_steps = "\n".join(thought_steps_list)

            shell = data.get("selectedShell", "unknown").upper()
            command = data.get("command", "")

            # בדיקות אבטחה בסיסיות
            blocked, cleaned_or_msg = sanitize_or_block(command)
            if blocked:
                return thought_steps, "BLOCKED", cleaned_or_msg, f"{data.get('confidenceScore', '-')}/10", data.get('riskLevel', 'RED'), "False"

            confidence = f"{data.get('confidenceScore', '-')}/10"
            risk = data.get("riskLevel", "unknown").upper()
            compliance = "מאושר (True)" if data.get("compliance") else "חסום (False)"

            return "\n".join(thought_steps), shell, cleaned_or_msg, confidence, risk, compliance

        except json.JSONDecodeError:
            # החזרת פלט ידידותי לשגיאה שניתן לתעד בגיליון
            return "שגיאה: הפלט אינו JSON תקין", "ERROR", raw_output, "0/10", "RED", "False"

    except Exception as e:
        return f"שגיאה בפנייה למודל: {str(e)}", "ERROR", "", "0/10", "RED", "False"

# --- ממשק גראדיו מתקדם (איטרציה 3) ---
with gr.Blocks(title="Hyper Advanced CLI Agent") as demo:
    gr.Markdown("# 🧠 Hyper Advanced CLI Agent - איטרציה 3 (Chain of Thought)")
    gr.Markdown("המערכת מציגה כעת את תהליך החשיבה הפנימי של המודל, בוחרת סביבת הרצה אופטימלית ומעריכה רמת ביטחון.")
    
    with gr.Row():
        with gr.Column(scale=2):
            input_text = gr.Textbox(label="הוראה בשפה טבעית (Input)", placeholder="הקלידי כאן את הבדיקה...")
            submit_btn = gr.Button("נתח ובצע שרשור חשיבה", variant="primary")
            output_thought = gr.TextArea(label="🧠 תהליך חשיבה מובנה (Chain of Thought)", lines=5)
            
        with gr.Column(scale=2):
            output_command = gr.Textbox(label="💻 פקודת ה-CLI הסופית (Command)")
            output_shell = gr.Textbox(label="🐚 סביבת הרצה נבחרת (Selected Shell)")
            output_confidence = gr.Textbox(label="🎯 מדד ביטחון עצמי (Confidence Score)")
            output_risk = gr.Textbox(label="⚠️ רמת סיכון (Risk Level)")
            output_compliance = gr.Textbox(label="🛡️ סטטוס אבטחה (Compliance)")

    submit_btn.click(
        fn=generate_cli_advanced, 
        inputs=input_text, 
        outputs=[output_thought, output_shell, output_command, output_confidence, output_risk, output_compliance]
    )

if __name__ == "__main__":
    demo.launch()