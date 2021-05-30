# Rename Scientific Papers

Why would you want to rename scientific papers?

Well, if you're like me and you spend a lot of time going through research papers, you will have found it quite annoying to figure out which pdf is for which paper once you've
downloaded them all to a single folder.

You'll have some named as "231514232" while others will have more sophisticated naming but in the end, this is all gibberish to you.

So, I decided to make a web app where you can upload all the pdfs you've downloaded, and get them back in a zipped file with each renamed with the title and year of publication.

Right now, this project is under construction, and my initial focus is just to rename the pdfs.

If I succeed in making this, I'll add more features. For example, I'll add a feature that will categorize the pdfs under keywords for ease of access or based on year of publication.

A few important notes regarding usage:

- This uses grobid through Docker containers
- It also uses the Grobid Python client

Both of these will not be included if you clone this repo. You will have to set them up separately. I'll add instructions for doing both of these later.
