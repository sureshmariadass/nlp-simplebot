import random
import string
import nltk
import requests

import numpy as np

from googlesearch import search
from lxml import html
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer


user_input = "how old is samuel l jackson"

google_search_results = list(search(user_input, stop=3, pause=1))
webpage = requests.get(google_search_results[0])
webpage_tree = html.fromstring(webpage.content)
webpage_soup = BeautifulSoup(webpage.content, "lxml")
webpage_text = ''
all_p_list = webpage_soup.findAll('p')
for element in all_p_list:
  webpage_text += '\n' + ''.join(element.findAll(text = True))

print("Type: ", type(webpage_text))
print(webpage_text)
