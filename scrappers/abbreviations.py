import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

EDUCATION_DEGREES_1 = pd.read_html("https://www.mc.edu/offices/marketing/branding/editorial-style-guide/abbreviations")[
    0]
EDUCATION_DEGREES_1 = EDUCATION_DEGREES_1.iloc[1:, :]  # remove first row
EDUCATION_DEGREES_1.rename(columns={0: 'Degree', 1: 'Abbreviation'}, inplace=True)
EDUCATION_DEGREES_1 = EDUCATION_DEGREES_1.Abbreviation.apply(lambda abbv: re.sub(r'[?|$|.|!|,]', r'', abbv)).tolist()
# get from another url
URL = "https://abbreviations.yourdictionary.com/articles/degree-abbreviations.html"
r = requests.get(URL)
soup = BeautifulSoup(r.content, "html.parser")

sections = soup.findAll('section', attrs={'class': 'article-body'})
len(sections)

EDUCATION_DEGREES_2 = {}


def removesuffix(string, suffix):
    if string.endswith(suffix):
        return string[:-len(suffix)]
    return string


def li_tag_stripe(li_tag, split_at):
    li_tag = li_tag.text.strip().split(split_at)
    abbv, degree = li_tag
    # abbv = abbv.removesuffix(' - ') # removesuffix is a 3.9+ method in str
    abbv = removesuffix(abbv, ' - ')
    abbv = re.sub(r'[?|$|.|!|,]', r'', abbv)
    two_abbv = abbv.split(' or ')
    if len(two_abbv) > 1:
        for ab in two_abbv:
            EDUCATION_DEGREES_2[ab] = split_at + degree

    if len(two_abbv) == 1:
        EDUCATION_DEGREES_2[abbv] = split_at + degree


for li_tag in sections[4].findAll('li'):
    li_tag_stripe(li_tag=li_tag, split_at='Associate')

for li_tag in sections[5].findAll('li'):
    li_tag_stripe(li_tag=li_tag, split_at='Bach')

# pd.DataFrame(EDUCATION_DEGREES.items()).head()
EDUCATION_DEGREES_2 = list(EDUCATION_DEGREES_2.keys())
EDUCATION_DEGREES = list(set(EDUCATION_DEGREES_1 + EDUCATION_DEGREES_2))

df = pd.DataFrame({'degrees': EDUCATION_DEGREES})
df.to_csv("scrappers/degrees.csv", index=False)
print("Education Degrees Saved")
