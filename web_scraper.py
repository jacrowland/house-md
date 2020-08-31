"""
web_scraper.py

Scrape a file full of links to House M.D. (2004) scripts.
For each url output a file of character dialogue for use in chatterbot training.

"""

from urllib.request import urlopen
import html as HTML
import re

def scrape(urls):
    scraped = 0
    for url in urls:
        url = url.replace("\n", "")
        scraped += 1
        print('[' + str(scraped) + ' of ' + str(len(urls)) + '] ' + url)
        page = urlopen(url)
        # Extract html bytes and parse as a string
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        # Where the script begins in the html 
        start = html.find('<a name="cutid1"></a>')
        end = html.find("<a name='cutid1-end'></a>")
        html = html[start+21:end]
        html = html.split("<br />")

        script = []
        for line in html:
            line = HTML.unescape(line)
            # if line is dialogue in the form "character name: line...")
            if not (re.search(r"\w+\s?\w:\s[\w,’'.\s\[\]\-–]+",line) == None):
                script.append(line)

        filename = 'script' + str(scraped) + '.txt'
        outputToFile(script, filename) 

def outputToFile(script, filename):
    f = open('scripts/' + filename, "w", encoding='utf-8')
    for line in script:
        f.write(line + '\n')
    f.close()
    print('Found and saved ' + str(len(script)) + ' lines to ' + filename)

def main():
    urls = open('urls.txt', 'r') # files containg the urls for the various scripts
    urls = urls.readlines()
    scrape(urls)
main()
