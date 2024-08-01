from flask import Flask, request, render_template_string
from pdf_digestion_tools import get_text_from_file, clean_text

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if not allowed_file(file.filename):
            return "File must be a pdf"
        if file:
            text = get_text_from_file(file)
            cleaned_text = clean_text(text)
            word_count = len(cleaned_text)
            return f"The PDF contains {word_count} words."
        print("No return")
    return '''
    <!doctype html>
    <title>Upload a PDF</title>
    <h1>Upload a PDF to count words</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)