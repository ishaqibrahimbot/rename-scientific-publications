from bs4 import BeautifulSoup
import os
import glob
import re
from getYear import get_year
from grobid_client.grobid_client import GrobidClient
import argparse

def process_pdfs(UPLOAD_FOLDER, include_year, concurrency):
    client = GrobidClient(config_path="./grobid_client_python/config.json")

    if include_year:
        client.process("processFulltextDocument", UPLOAD_FOLDER, output="processed_pdfs", consolidate_header=False, verbose=True, n=concurrency)
    else:
        client.process("processHeaderDocument", UPLOAD_FOLDER, output="processed_pdfs", consolidate_header=False, verbose=True, n=concurrency)


def get_xml_files(pdf_files):
    xml_files = []

    for file in pdf_files:
        _, file_only = os.path.split(file)
        new_file_path = os.path.join("processed_pdfs", file_only)
        new_file_path = new_file_path[:-4] + ".tei.xml"
        xml_files.append(new_file_path)

    return xml_files


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
    pdf_files = glob.glob(os.path.join(pdfs_folder, "*.pdf"))
    xml_files = get_xml_files(pdf_files)

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


def main(pdf_folder, include_year, n):
    process_pdfs(pdf_folder, include_year, n) #Process the pdfs using Grobid
    rename_pdfs(pdf_folder, include_year) #Rename by extracting the title and date from xml files

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pdf_folder",
        default="pdfs",
        type=str,
        help="Specify the name of the folder containing the PDFs")

    parser.add_argument(
        "--include_year",
        type=bool,
        default=False,
        help="Specify True or False depending on whether you want to include the year of publication in the filename as well. This will take a bit longer to process.")

    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="Specify the number of concurrent requests you want to make in the range 1-10. Note that higher values will overload your CPU so make sure you have a blazing fast CPU with multiple cores to use high concurrency.")

    args = parser.parse_args()

    main(args.pdf_folder, args.include_year, args.n)











