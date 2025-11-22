import os
from flask import Flask, render_template, request, redirect, send_file, flash, send_from_directory, after_this_request, jsonify, session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import fitz
import tempfile
from io import BytesIO


# --- Flask setup ---
app = Flask(__name__)
app.secret_key = "cs50 final project"
app.config["MAX_CONTENT_LENGTH"] = 150 * 1024 * 1024
progress = 0


def allowed_file(filename):
    return ("." in filename) and (filename.rsplit(".", 1)[1].lower() in ["pdf"])


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    flash("File too large. Maximum allowed size is 150 MB.", "danger")
    return redirect("/")


# --- Routes ---
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    global progress

    if "file" not in request.files:
        flash("No file part!!", "danger")
        return redirect("/")

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file!!", "danger")
        return redirect("/")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        output = fitz.open()

        with tempfile.TemporaryDirectory() as temp:
            filedir = os.path.join(temp, filename)
            file.save(filedir)
            try:
                input_doc = fitz.open(filedir)
            except Exception:
                flash("Couldn't open the file", "danger")
                return redirect("/")

            new_width = 595
            BATCH_SIZE = 10

            batches = []

            for i in range(0, len(input_doc), BATCH_SIZE):
                output_doc = fitz.open()
                for page_number in range(i, min(i + BATCH_SIZE, len(input_doc))):
                    try:
                        page = input_doc.load_page(page_number)
                    except Exception:
                        flash(f"Error on page {page_number}", "danger")
                        return redirect("/")
                    old_rect = page.rect
                    scale_factor = new_width / old_rect.width
                    new_height = old_rect.height * scale_factor

                    new_page = output_doc.new_page(width=new_width, height=new_height)
                    new_page.show_pdf_page(new_page.rect, input_doc, page_number)
                    progress = (page_number / len(input_doc)) * 100
                out = os.path.join(temp, f"batch_{i // BATCH_SIZE}.pdf")
                output_doc.save(out)
                output_doc.close()
                batches.append(out)
            input_doc.close()

            for f in batches:
                with fitz.open(f) as batch:
                    output.insert_pdf(batch)


        output_bytes = BytesIO()
        output.save(output_bytes)
        output.close()
        output_bytes.seek(0)
        progress = 100
        
        
        @after_this_request
        def progress_0(response):
            flash("Successfully Completed!! Enjoy!!", "success")
            return response

        return send_file(output_bytes, as_attachment=True, download_name=f"resized_{filename}", mimetype="application/pdf")

    flash("Invalid file type!! only PDFs allowed.", "danger")
    return redirect("/")

@app.route("/progress")
def progress_status():
    return jsonify({"progress": progress})

# --- Favicon route ---
@app.route('/favicon.ico')
def favicon():
    images_dir = os.path.join(app.root_path, 'images')
    filename = 'ChatGPT_Image_Oct_9__2025__02_54_23_PM-removebg-preview.ico'
    return send_from_directory(images_dir, filename, mimetype='image/vnd.microsoft.icon')

# --- Run app ---
if __name__ == "__main__":
    app.run(debug=True)
