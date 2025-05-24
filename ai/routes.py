from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import openai  # убедитесь, что установлен openai
from config import Config
import re

ai_bp = Blueprint('ai', __name__)

client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

@ai_bp.route('/ai_character', methods=['GET', 'POST'])
def ai_character():
    if request.method == 'POST':
        prompt = request.form['prompt']
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an assistant that creates fictional characters for writers. "
                                                  "The user may describe the character in Russian, Kazakh, or English. "
                                                  "Always reply in English. Use this format: name, age, appearance, personality, backstory. "
                                                  "Do not use bold text."},
                    {"role": "user", "content": f"Create a character: {prompt}. Format: name, age, appearance, personality, backstory"}
                ]
            )
            raw = response.choices[0].message.content

            def safe_search(pattern, text, group=1, default=''):
                match = re.search(pattern, text)
                return match.group(group).strip() if match else default

            character_data = {}
            character_data['name'] = safe_search(r"[Nn]ame[:\-]\s*(.+)", raw)
            age_str = safe_search(r"[Aa]ge[:\-]\s*(\d+)", raw)
            character_data['age'] = int(age_str) if age_str.isdigit() else None
            character_data['appearance'] = safe_search(r"[Aa]ppearance[:\-]\s*(.+)", raw)
            character_data['personality'] = safe_search(r"[Pp]ersonality[:\-]\s*(.+)", raw)
            character_data['backstory'] = safe_search(r"[Bb]ackstory[:\-]\s*(.+)", raw)

            session['ai_character'] = character_data
            return redirect(url_for('characters.create_character'))

        except Exception as e:
            flash(f"Ошибка: {e}", 'danger')

    return render_template('ai_character.html')
