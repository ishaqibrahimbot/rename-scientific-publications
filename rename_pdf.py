from bs4 import BeautifulSoup
import os
import glob
import re
from getYear import get_year

processed_pdfs_folder = "processed_pdfs"
pdfs_folder = "pdfs"
xml_files = glob.glob(os.path.join(processed_pdfs_folder, "*.xml"))
pdf_files = glob.glob(os.path.join(pdfs_folder, "*.pdf"))

def get_title(soup):

    title = soup.title.getText()
    title = re.sub("[^a-zA-Z ]+", " ", title)

    if len(title) > 40:
        title = title[:40]
    
    date = get_year(soup.date.getText())
    if date is not None:
        new_title = os.path.join(pdfs_folder, "(" + date + ")" + " " + title +  ".pdf")
    else:
        new_title = os.path.join(pdfs_folder, title + ".pdf")
    
    return new_title


allSoups = []

for xml_file in xml_files:
    with open(xml_file, 'r') as f:
        allSoups.append(BeautifulSoup(f, 'lxml'))

new_titles = []

for soup in allSoups:
    new_title = get_title(soup)
    print(new_title)
    new_titles.append(new_title)

for i in range(len(pdf_files)):
    os.rename(pdf_files[i], new_titles[i]) 

























