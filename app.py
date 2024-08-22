from flask import Flask, render_template, send_from_directory, jsonify
import json
import os

app = Flask(__name__)

BOOK_DIR = 'processed_book'

def load_chapters():
    with open(os.path.join(BOOK_DIR, 'chapters.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    chapters = load_chapters()
    return render_template('reader.html', chapters=chapters)

@app.route('/api/chapters')
def get_chapters():
    chapters = load_chapters()
    return jsonify(chapters)

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_from_directory(BOOK_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)