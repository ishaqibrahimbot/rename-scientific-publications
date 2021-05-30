from bs4 import BeautifulSoup
import os
import glob

pdf_folder = "processed_pdfs"
xml_files = glob.glob(os.path.join(pdf_folder, "*.xml"))

print(xml_files)
allSoups = []

for xml_file in xml_files:
    with open(xml_file, 'r') as f:
        allSoups.append(BeautifulSoup(f, 'lxml'))

print(allSoups)
