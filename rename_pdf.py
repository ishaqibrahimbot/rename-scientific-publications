from bs4 import BeautifulSoup
import os
import glob
import re
from getYear import get_year
from grobid_client.grobid_client import GrobidClient
import argparse

def process_pdfs(UPLOAD_FOLDER, include_year, concurrency):
    """
    Use grobid_client_python to send pdf files to the Grobid Server and save the *.tei.xml files 
    returned inside the "processed_pdfs" folder.

    Two modes:

    - include_year=True -> adds the year of publication to the start of the name of each pdf
    - include_year=False -> Does not do the above
    """

    client = GrobidClient(config_path="./grobid_client_python/config.json")

    if include_year:
        client.process("processFulltextDocument", UPLOAD_FOLDER, output="processed_pdfs", consolidate_header=False, verbose=True, n=concurrency)
    else:
        client.process("processHeaderDocument", UPLOAD_FOLDER, output="processed_pdfs", consolidate_header=False, verbose=True, n=concurrency)


def get_xml_files(pdf_files):
    """
    Get the list of corresponding .tei.xml files for each pdf file, once Grobid has completed its
    processing.
    """
    xml_files = []

    for file in pdf_files:
        _, file_only = os.path.split(file)
        new_file_path = os.path.join("processed_pdfs", file_only)
        new_file_path = new_file_path[:-4] + ".tei.xml"
        xml_files.append(new_file_path)

    return xml_files


def get_title(soup, pdfs_folder, include_year):
    """
    Get a standardized title from the object returned by BeautifulSoup
    """

    title = soup.title.getText()
    title = re.sub("[^a-zA-Z ]+", " ", title) #Remove any characters other than letters

    if len(title) > 40:
        title = title[:40] #Just take the first 40 characters of the title for the new name of the pdf


    # Depending on the value of include_year, either add the YoP to the name or not
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
    """
    Grab all the .tei.xml files, run them through BeautifulSoup to get the new file name, and rename
    each pdf file.
    """

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

    # Make the "processed_pdfs" folder if it doesn't already exist
    if not os.path.exists("processed_pdfs"):
        os.mkdir("processed_pdfs")

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











