# Rename Scientific Papers

## Why would you want to rename scientific papers?

Well, if you're like me and you spend a lot of time going through research papers, you will have found it quite annoying to figure out which pdf is for which paper once you've
downloaded them all to a single folder.

You'll have some named as "231514232" while others will have more sophisticated naming but in the end, this is all gibberish to you.

So, I decided to make a web app where you can upload all the pdfs you've downloaded, and get them back in a zipped file with each renamed with the title and year of publication.

I will also make a simple script to use this application directly from the terminal (in the future).

## How to use

### Requirements

You will need the Docker Engine (with Docker Compose) to easily set up and run this application. If you run a Linux-based OS or MacOS, you will find using this application quite easy.

However, if you're using a version of Windows that does not support Docker, you won't be able to use it :(

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

You will notice log messages from two apps: the Flask app and the Grobid server (that this application uses for processing of pdf content).

### Open the Flask URL

Check the log messages by the Flask app and open the URL in your browser. This will normally be of the form x.x.x.x:5000

That's it! Now you can upload as many PDFs as you want and get a zipped file in return with the same PDFs renamed.

Note: The processing might take some time, so please be patient and carry on with your other work. The browser will prompt you automatically to download the zip file once the processing is completed.

For queries, suggestions, and issues, contact: ishaqibrahimbss@gmail.com
