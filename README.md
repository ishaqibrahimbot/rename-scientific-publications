# Rename Scientific Papers

## Why would you want to rename scientific papers?

Well, if you're like me and you've had to download a lot of research papers for literature reviews, you will have found it quite annoying to figure out which PDF is for which paper once you've downloaded them all to a single folder.

You'll have some named as "231514232" while others will have more sophisticated naming but in the end, this is all gibberish to you.

So, I decided to make a tool that you can use to rename each PDF with the title and year of publication so that it becomes a lot easier to organize and manage your research papers.

I originally set out to make a Flask web app using Python where a user can upload all the papers and get them back (renamed) inside a zip file. However, this proved to be too cumbersome and slowed down the processing by a great deal. In the end, I settled on a simple script that can be run from the command line and gives excellent processing speed.

## Requirements

This project only works on Linux-based operating systems or MacOS, for two reasons: (1) The service used for processing PDFs, Grobid, is not supported on Windows, and (2) Docker is not supported well on Windows either. So if you're a Windows user, I'm sorry :(

If you use Linux or MacOS, proceed with the instructions given below. You'll need the Docker Engine installed since this project uses a Docker image from the Docker Hub.

## Usage Instructions

### Grab the Grobid image from Docker

Make sure docker is installed in your system. If so, run the following command to pull the Grobid image:

```
sudo docker pull lfoppiano/grobid:0.6.2
```

### Clone this repo and go inside the directory

```
git clone https://github.com/ishaqibrahimbot/rename-scientific-publications.git
cd rename-scientific-publications
```

### Install the grobid client

```
git clone https://github.com/kermitt2/grobid_client_python.git
cd grobid_client_python
sudo python setup.py install
cd ..
```

All these commands are doing is cloning the repo for the grobid client, going inside its folder, installing the dependencies, and getting outside the folder.

### Start the Grobid server

```
./start_grobid_server.sh
```

### Run the script

Finally, make a directory named "pdfs" inside the project's root folder and paste all of your PDF files inside it.

Now go back to your terminal (open a new tab since the first one will now be running the Grobid server) and run the following command:

```
python rename_pdf.py
```  
The project will start processing your files. If you check the terminal window where the Grobid server is running, you will see the requests being sent and processed sequentially.

Run the above command with a -h argument to see all possible arguments. If you want your new PDF names to include the year of publication as well, run the following command:

```
python rename_pdf.py --include_year=True
```

Once the processing is finished (took me about 1-2 mins to process 10 PDFs with a total size of 9.8MB), you can go back to the "pdfs" folder and find your PDF files, renamed.

For queries, suggestions, and issues (especially if you find glaring problems in the code), contact: ishaqibrahimbss@gmail.com

## In case you want to check out the Flask app

Although I don't recommend that you use the Flask app (it works fine but is just too slow compared to the command line method), you can still do so by following these instructions.

### Clone the repo

Clone the repo to a local directory by running the following line of code:

```
git clone https://github.com/ishaqibrahimbot/rename-scientific-publications.git
```

### Use Docker Compose to start the services

Go into the cloned directory using your terminal and after that, run the following command (make sure you have docker-compose installed):

```
sudo docker-compose up
```

You will notice log messages from two apps: the Flask app and the Grobid server (that this application uses for processing of PDF content).

### Open the Flask URL

Check the log messages by the Flask app and open the URL in your browser. This will normally be of the form x.x.x.x:5000

That's it! Now you can upload as many PDFs as you want and get a zipped file in return with the same PDFs renamed.

Note: The processing might take some time, so please be patient and carry on with your other work. The browser will prompt you automatically to download the zip file once the processing is completed.

