from DrissionPage import ChromiumPage, ChromiumOptions
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import re
from scholarly import scholarly


# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_author('Steven A Cholewiak')
author = scholarly.fill(next(search_query))
print(author)

# Print the titles of the author's publications
print([pub['bib']['title'] for pub in author['publications']])

# Take a closer look at the first publication
pub = scholarly.fill(author['publications'][0])
print(pub)

# Which papers cited that publication?
print([citation['bib']['title'] for citation in scholarly.citedby(pub)])
