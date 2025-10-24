# app.py
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
from transformers import pipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


simplifier = pipeline("text2text-generation", model="facebook/bart-large-cnn")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def simplify_text(text):
    simplified = simplifier(text, max_length=130, min_length=30, do_sample=False)
    return simplified[0]['generated_text']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                text = pytesseract.image_to_string(Image.open(filepath))
            else:
                with open(filepath, 'r') as f:
                    text = f.read()
            
            simplified_text = simplify_text(text)
            return jsonify({'original': text, 'simplified': simplified_text})
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)