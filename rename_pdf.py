from bs4 import BeautifulSoup
import os
import glob
import re
from getYear import get_year
from grobid_client.grobid_client import GrobidClient

def process_pdfs(UPLOAD_FOLDER, include_year):
    client = GrobidClient(config_path="./grobid_client_python/config.json")

    if include_year:
        client.process("processFulltextDocument", UPLOAD_FOLDER, output="processed_pdfs", consolidate_header=False, verbose=True, n=1)
    else:
        client.process("processHeaderDocument", UPLOAD_FOLDER, output="processed_pdfs", consolidate_header=False, verbose=True, n=1)

def get_title(soup, pdfs_folder, include_year):

    title = soup.title.getText()
    title = re.sub("[^a-zA-Z ]+", " ", title)

    if len(title) > 40:
        title = title[:40]

    if include_year:
        date = get_year(soup.date.getText())
        if date is not None:
            new_title = os.path.join(pdfs_folder, "(" + date + ")" + " " + title +  ".pdf")
        else:
            new_title = os.path.join(pdfs_folder, title + ".pdf")
    else:
        new_title = os.path.join(pdfs_folder, title + ".pdf")
    
    return new_title


def rename_pdfs(UPLOAD_FOLDER, include_year):

    processed_pdfs_folder = "processed_pdfs"
    pdfs_folder = UPLOAD_FOLDER
    xml_files = glob.glob(os.path.join(processed_pdfs_folder, "*.xml"))
    pdf_files = glob.glob(os.path.join(pdfs_folder, "*.pdf"))


    allSoups = []

    for xml_file in xml_files:
        with open(xml_file, 'r') as f:
            allSoups.append(BeautifulSoup(f, 'lxml'))

    new_titles = []

    for soup in allSoups:
        new_title = get_title(soup, pdfs_folder, include_year)
        print(new_title)
        new_titles.append(new_title)

    for i in range(len(pdf_files)):
        os.rename(pdf_files[i], new_titles[i]) 


# Leave these two lines, do not remove them. Add these two to the grobid service definition
# in the docker-compose.yaml file if you want to replace the config file in the container
# # with a local (modified) config file
# volumes:
#         - ./config.yaml:/opt/grobid/grobid-service/config/config.yaml





















