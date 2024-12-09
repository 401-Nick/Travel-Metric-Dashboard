ALLOWED_EXTENSIONS = {'csv'}

def is_csv_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
