## Simple web-scraper

I've written a script 
* that checks for new pages from the website abduzeedo.com
* uploads the images from each page to a separate imgur album
* uploads each album link to the subreddit /r/feedtesting

The config.txt has the time stamp for the last run (which let's the code know that a new page is up)
Client IDs have been masked from both imgur and reddit. Use your own codes.

Usage - 
```python
python main.py
```