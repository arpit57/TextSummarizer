
import requests
from bs4 import BeautifulSoup
import streamlit as st
from transformers import pipeline
import re
from streamlit.components.v1 import html


# specify the URL of the news website to scrape
url = "https://www.theverge.com/"

# send a GET request to the website URL and store the response
response = requests.get(url)

# parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# find all the news article links on the website
article_links = soup.find_all("a", class_="group-hover:shadow-underline-franklin")

l = []
links = []

# loop through each article link and scrape the article text
for link in article_links:
    # extract the URL of the article
    article_url = link["href"]
    
    # send a GET request to the article URL and store the response
    article_response = requests.get(url + article_url)
    links.append(url + article_url)

#     # parse the HTML content of the article using BeautifulSoup
    article_soup = BeautifulSoup(article_response.content, "html.parser")
    
#     # find the main text content of the article and print it
    article_text = article_soup.find("div", class_="clearfix").get_text()
    l.append(article_text)

def get_first_thousand_words(text):
    words = re.findall(r'\b\w+\b|[^\w\s]', text)
    return ' '.join(words[:800])

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summaries = []
for i in l:
    i = get_first_thousand_words(i)

    summaries.append(summarizer(i, max_length=300, min_length=100))

summariesText = [i[0]["summary_text"] for i in summaries]



st.title("Live tech news summarizer")
text = " Read full article here"

for n, i in enumerate(summariesText):
    st.write(f"<div style='font-weight:normal'>{i}<a href='{links[n]}'>{text}</a></div><br>", unsafe_allow_html=True)

