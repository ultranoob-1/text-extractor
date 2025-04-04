from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No file selected", 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    extracted_text = pytesseract.image_to_string(Image.open(file_path))
    return render_template("result.html", text=extracted_text)

if __name__ == "__main__":
    app.run(debug=True)
