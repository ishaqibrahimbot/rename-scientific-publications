import os, shutil
import glob
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import rename_pdf
from rename_pdf import process_pdfs, get_title, rename_pdfs

def setup_folder(FOLDER_PATH):
    if os.path.exists(FOLDER_PATH):
        shutil.rmtree(FOLDER_PATH)
        os.mkdir(FOLDER_PATH)
    else:
        os.mkdir(FOLDER_PATH)


#Define paths
UPLOAD_FOLDER = "pdfs"
XML_FOLDER = "processed_pdfs"
ALLOWED_EXTENSIONS = {'pdf'}
ZIP_FILE_NAME = "tmp.zip"

#Initialize folders
setup_folder(UPLOAD_FOLDER)
setup_folder(XML_FOLDER)

#Initialize Flask app and set upload folder path
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Function to check if uploaded file is a PDF
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Root route methods for uploading, renaming, and downloading files
@app.route("/", methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':

		#Make sure files are uploaded
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)

		#Obtain list of uploaded files
		files = request.files.getlist("file")

		for file in files:
			#If there is an empty name file or a bunch of weird stuff in the uploads, tell the user
			if file.filename == '':
				flash("No selected file")
				return redirect(request.url)

			#Make the filename secure using the secure_filename function
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #Save the file

		print("Made it till here!")
		process_pdfs(UPLOAD_FOLDER) #Process the pdfs using Grobid
		rename_pdfs(UPLOAD_FOLDER) #Rename by extracting the title and date from xml files
		
		processed_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.pdf"))

		#Package all pdfs into a single zip file
		with ZipFile(ZIP_FILE_NAME, "w") as zip_file:
			for file in processed_files:
				zip_file.write(file)

		#Send zip file to user for downloading
		return send_file(ZIP_FILE_NAME, as_attachment=True)

	print("Loading the default page!")		
		
	#If method isn't POST, just render the default homepage
	return render_template('upload_page.html')


#Run the app
if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")
