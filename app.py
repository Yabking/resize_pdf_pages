import os
from flask import Flask, render_template, request, redirect, send_file, flash, send_from_directory, after_this_request, jsonify, session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import fitz
from io import BytesIO

# --- Flask setup ---
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cs50 final project")
app.config["MAX_CONTENT_LENGTH"] = 150 * 1024 * 1024  # 150 MB

def allowed_file(filename):
    return ("." in filename) and (filename.rsplit(".", 1)[1].lower() in ["pdf"])

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    flash("File too large. Maximum allowed size is 150 MB.", "danger")
    return redirect("/")

# --- Routes ---
@app.route("/", methods=["GET"])
def index():
    if "progress" not in session:
        session["progress"] = 0
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    session["progress"] = 0
    session.modified = True

    if "file" not in request.files:
        flash("No file part!!", "danger")
        return redirect("/")

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file!!", "danger")
        return redirect("/")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        try:
            file_bytes = file.read()
            input_doc = fitz.open(stream=file_bytes, filetype="pdf")
        except Exception:
            flash("Couldn't open the file", "danger")
            return redirect("/")

        try:
            new_width = 595
            output = fitz.open()

            total_pages = len(input_doc)
            if total_pages == 0:
                flash("PDF has no pages.", "danger")
                input_doc.close()
                return redirect("/")

            for page_number in range(total_pages):
                try:
                    page = input_doc.load_page(page_number)
                except Exception:
                    flash(f"Error on page {page_number}", "danger")
                    input_doc.close()
                    output.close()
                    return redirect("/")

                old_rect = page.rect
                scale_factor = new_width / old_rect.width
                new_height = old_rect.height * scale_factor

                new_page = output.new_page(width=new_width, height=new_height)
                new_page.show_pdf_page(new_page.rect, input_doc, page_number)

                session["progress"] = int(((page_number + 1) / total_pages) * 100)
                session.modified = True

            input_doc.close()

            output_bytes = BytesIO()
            output.save(output_bytes)
            output.close()
            output_bytes.seek(0)
            session["progress"] = 100
            session.modified = True

            @after_this_request
            def progress_0(response):
                flash("Successfully Completed!! Enjoy!!", "success")
                return response

            return send_file(
                output_bytes,
                as_attachment=True,
                download_name=f"resized_{filename}",
                mimetype="application/pdf",
            )
        except Exception as e:
            # Clean up well and give the user an error
            try:
                input_doc.close()
            except Exception:
                pass
            try:
                output.close()
            except Exception:
                pass
            flash(f"Unexpected error during processing: {str(e)}", "danger")
            return redirect("/")

    flash("Invalid file type!! only PDFs allowed.", "danger")
    return redirect("/")

@app.route("/progress")
def progress_status():
    return jsonify({"progress": session.get("progress", 0)})

# --- Favicon route ---
@app.route('/favicon.ico')
def favicon():
    images_dir = os.path.join(app.root_path, 'images')
    filename = 'ChatGPT_Image_Oct_9__2025__02_54_23_PM-removebg-preview.ico'
    return send_from_directory(images_dir, filename, mimetype='image/vnd.microsoft.icon')

# --- Run app ---
if __name__ == "__main__":
    app.run(debug=True)
