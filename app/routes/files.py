from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    abort,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.utils.verify_extension_type import is_csv_file
from app.models import UploadedFile
from app import db
import os

files = Blueprint("files", __name__)

# Constants
UPLOAD_FOLDER = "uploads"

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@files.route("/")
@login_required
def home():
    # Retrieve all uploaded files for the current user
    uploaded_files = UploadedFile.query.filter_by(user_id=current_user.id).all()
    return render_template("files.html", uploaded_files=uploaded_files)


@files.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")

    if not file or file.filename == "":
        flash("No file selected.", "danger")
        return redirect(url_for("files.home"))

    if not is_csv_file(file.filename):
        flash("Invalid file type. Please upload a CSV file.", "danger")
        return redirect(url_for("files.home"))

    # Save the file locally
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Ensure unique filenames
    if os.path.exists(file_path):
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(file_path):
            filename = f"{base}_{counter}{extension}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            counter += 1

    file.save(file_path)

    # Store file metadata in the database
    uploaded_file = UploadedFile(
        filename=filename, file_path=file_path, user_id=current_user.id
    )
    db.session.add(uploaded_file)
    db.session.commit()

    flash("File uploaded successfully!", "success")
    return redirect(url_for("files.home"))


@files.route("/download/<int:file_id>/<filename>", methods=["GET"])
@login_required
def download_file(filename, file_id):
    # Legacy, replace with Session.get()
    uploaded_file = UploadedFile.query.get(file_id)

    if not uploaded_file or uploaded_file.filename != filename:
        abort(404, description="File not found")

    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found")


@files.route("/delete/<int:file_id>", methods=["POST"])
@login_required
def delete_file(file_id):
    # Get the file from the database
    # Legacy, replace with Session.get()
    uploaded_file = UploadedFile.query.get(file_id)

    # Ensure the file exists and belongs to the current user
    if not uploaded_file or uploaded_file.user_id != current_user.id:
        flash("File not found or access denied.", "danger")
        return redirect(url_for("files.home"))

    # Attempt to delete the file from the file system
    try:
        if os.path.exists(uploaded_file.file_path):
            os.remove(uploaded_file.file_path)
    except Exception as e:
        flash(f"Error deleting file from disk: {e}", "danger")
        return redirect(url_for("files.home"))

    # Delete the file record from the database
    db.session.delete(uploaded_file)
    db.session.commit()

    flash("File deleted successfully!", "success")
    return redirect(url_for("files.home"))


# This renames the file and updates the database record
@files.route("/rename_file/<int:file_id>", methods=["POST"])
@login_required
def rename_file(file_id):
    # Get the file from the database
    uploaded_file = UploadedFile.query.get(file_id)

    # Ensure the file exists and belongs to the current user
    if not uploaded_file or uploaded_file.user_id != current_user.id:
        flash("File not found or access denied.", "danger")
        return redirect(url_for("files.home"))

    new_filename = request.form.get("new_filename")

    if not new_filename or new_filename == "":
        flash("Invalid filename.", "danger")
        return redirect(url_for("files.home"))

    # Ensure unique filenames and that the filename ends with .csv
    new_filename = secure_filename(new_filename)

    if new_filename.endswith(".csv"):
        new_filename = new_filename[:-4]

    new_filename = f"{new_filename}.csv"

    new_file_path = os.path.join(UPLOAD_FOLDER, new_filename)

    if os.path.exists(new_file_path):
        base, extension = os.path.splitext(new_filename)
        counter = 1
        while os.path.exists(new_file_path):
            new_filename = f"{base}_{counter}{extension}"
            new_file_path = os.path.join(UPLOAD_FOLDER, new_filename)
            counter += 1

    os.rename(uploaded_file.file_path, new_file_path)

    # Update the database record
    uploaded_file.filename = new_filename
    uploaded_file.file_path = new_file_path
    db.session.commit()

    flash("File renamed successfully!", "success")
    return redirect(url_for("files.home"))
