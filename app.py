
import requests
from bs4 import BeautifulSoup
import streamlit as st
import pickle
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier




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



summaries = []
percentages = []

nltk.data.path.append('./nltk_data/') # set the path to the NLTK data directory
# nltk.download('punkt', download_dir='./nltk_data/') # download the 'punkt' resource to the NLTK data directory


for n, i in enumerate(l):
    # Split the paragraph into sentences
    sentences = nltk.sent_tokenize(i)
    
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(sentences)
    
    y = [1 if i < len(sentences)//2 else 0 for i in range(len(sentences))]  # label the first half of sentences as important
    clf = RandomForestClassifier()
    clf.fit(X, y)
    
    important_indices = clf.predict(X).nonzero()[0]  # get the indices of the important sentences
    summary = ' '.join([sentences[i] for i in sorted(important_indices)])  # concatenate the important sentences into the summary
    summary_percentage = round(len(summary) / len(l[n]) *100, 1)

    # print(f"{summary} {len(summary)} / {len(l[n])} \n")
    summaries.append(summary)
    percentages.append(summary_percentage)



st.title("Daily Tech stories summarizer")
text = " Read full article here"

for n, i in enumerate(summaries):
	st.write(i + "<a href='" + links[n] + "'>" + text + "</a>", unsafe_allow_html=True)
	# st.write("<a href='" + links[n] + "'>" + text + "</a>", unsafe_allow_html=True)
	st.write("\n")