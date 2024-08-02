import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, render_template, redirect, url_for,flash, send_file
from article_digestion.pdf_digestion_tools import *
from statistics_generation.stat_generation_tools import *
from datetime import datetime

ALLOWED_EXTENSIONS = {'pdf'}
SAVE_FILE_NAME = "app/memory/article_memory.txt"

app = Flask(__name__)
app.secret_key = "super secret key" 


def allowed_file(filename): # check if file has an allowed extension
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html', page_count=None, word_count=None)

@app.route('/', methods=['POST'])
def upload_file():
    
    # Ingest data from upload.html
    date_submitted = convert_to_datetime(request.form['date_submitted'])
    author = request.form['author']
    title = request.form['title']
    
    # Checking file integrity 
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash("File must be a pdf")
        return redirect(request.url)

    if file:
        # Process the information in the PDF
        text,page_count = get_text_and_pg_count_from_file(file)
        cleaned_text = clean_text(text)
        word_count = len(cleaned_text)
        
        # Create a new article object
        article = ArticleData(title, author, date_submitted, int(page_count), int(word_count))
        save_article_data_to_memory_file(article,SAVE_FILE_NAME)

        flash("File successfully uploaded and article data saved.")
        return render_template('upload.html', page_count=page_count, word_count=word_count)
    else:
        flash("No file uploaded.")
        return redirect(request.url)

@app.route('/generate_statistics')
def generate_statistics():
    stats = generate_stats()
    img = create_stats_graph(stats)
    return send_file(img, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)