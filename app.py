import os
import glob
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import rename_pdf
from rename_pdf import process_pdfs, get_title, rename_pdfs

UPLOAD_FOLDER = "pdfs"
ALLOWED_EXTENSIONS = {'pdf'}
ZIP_FILE_NAME = "tmp.zip"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)

		files = request.files.getlist("file")

		for file in files:
			if file.filename == '':
				flash("No selected file")
				return redirect(request.url)

			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		process_pdfs(UPLOAD_FOLDER)
		rename_pdfs(UPLOAD_FOLDER)
		
		processed_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.pdf"))

		with ZipFile(ZIP_FILE_NAME, "w") as zip_file:
			for file in processed_files:
				zip_file.write(file)

		return send_file(ZIP_FILE_NAME, as_attachment=True)		
		

	return render_template('upload_page.html')


@app.route("/uploads/<filename>")
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == '__main__':
	app.run(debug=True)