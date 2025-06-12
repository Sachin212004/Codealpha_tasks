from flask import Flask, render_template, request, flash
from google.cloud import translate_v2 as translate
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Set full path to the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-key.json"

translate_client = translate.Client()

languages = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ar': 'Arabic',
    'ru': 'Russian',
    'it': 'Italian'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""
    selected_lang = "es"

    if request.method == 'POST':
        input_text = request.form['text']
        selected_lang = request.form['language']

        if not input_text.strip():
            flash("Please enter text to translate.")
        elif selected_lang not in languages:
            flash("Invalid language selected.")
        else:
            try:
                result = translate_client.translate(input_text, target_language=selected_lang)
                translated_text = result['translatedText']
            except Exception as e:
                flash(f"Translation error: {e}")

    return render_template('index.html', translated_text=translated_text, languages=languages, selected_lang=selected_lang)

if __name__ == '__main__':
    app.run(debug=True)
