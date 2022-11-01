import logging
import os
import urllib.request

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

# resemes_url = 'https://www.beamjobs.com/resumes/data-science-resume-example-guide'
resemes_url = 'https://www.beamjobs.com/resumes/data-engineer-resume-examples'

r = requests.get(resemes_url)
soup = BeautifulSoup(r.content, "html.parser")

urls = soup.findAll('a', attrs={'class': 'd-block mx-auto'}, href=True)
logging.info(f"Found {len(urls)} sample resume")

print(f"Start Downloading sample resumes")
for url in urls:
    logging.info("")
    logging.info(url['href'])
    urllib.request.urlretrieve(
        url['href'],
        f"scrappers/samples/{os.path.basename(url['href'])}"
    )
    logging.info(f"scrappers/samples/{os.path.basename(url['href'])}")
logging.info("Done downloading sample resumes!")
