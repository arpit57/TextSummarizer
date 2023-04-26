
import requests
from bs4 import BeautifulSoup
# import streamlit as st
# from transformers import pipeline
import re
# from streamlit.components.v1 import html
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.ensemble import RandomForestClassifier
# import nltk
from transformers import T5ForConditionalGeneration, T5TokenizerFast
from flask import Flask, render_template




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
    article_text = article_soup.find_all("p", class_="duet--article--dangerously-set-cms-markup duet--article--standard-paragraph mb-20 font-fkroman text-18 leading-160 -tracking-1 selection:bg-franklin-20 dark:text-white dark:selection:bg-blurple [&_a]:shadow-underline-black dark:[&_a]:shadow-underline-white [&_a:hover]:shadow-highlight-franklin dark:[&_a:hover]:shadow-highlight-blurple")
    paras = []
    concatenated_text = ""
    for para in article_text:
        concatenated_text += para.text + " "
    l.append(concatenated_text.rstrip(" "))

# def get_first_thousand_words(text):
#     words = re.findall(r'\b\w+\b|[^\w\s]', text)
#     return ' '.join(words[:800])

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# summaries = []
# for i in l:
#     i = get_first_thousand_words(i)

#     summaries.append(summarizer(i, max_length=300, min_length=100))

# summariesText = [i[0]["summary_text"] for i in summaries]

# summaries = []
# percentages = []

# nltk.data.path.append('./nltk_data/') # set the path to the NLTK data directory
# # nltk.download('punkt', download_dir='./nltk_data/') # download the 'punkt' resource to the NLTK data directory

# for n, i in enumerate(l):
#     # Split the paragraph into sentences
#     sentences = nltk.sent_tokenize(i)
    
#     vectorizer = TfidfVectorizer(stop_words='english')
#     X = vectorizer.fit_transform(sentences)
    
#     y = [1 if i < len(sentences)//4 else 0 for i in range(len(sentences))]  # label the first half of sentences as important
#     clf = RandomForestClassifier()
#     clf.fit(X, y)
    
#     important_indices = clf.predict(X).nonzero()[0]  # get the indices of the important sentences
#     summary = ' '.join([sentences[i] for i in sorted(important_indices)])  # concatenate the important sentences into the summary
#     summary_percentage = round(len(summary) / len(l[n]) *100, 1)

#     # print(f"{summary} {len(summary)} / {len(l[n])} \n")
#     summaries.append(summary)
#     percentages.append(summary_percentage)


tokenizer = T5TokenizerFast.from_pretrained("t5-small", model_max_length=512)
model = T5ForConditionalGeneration.from_pretrained("t5-small")

summaries = []

for n, i in enumerate(l):
    inputs = tokenizer.encode("summarize: " + i, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(outputs[0])
    clean_summary = summary.replace('<pad> ', '').replace('</s>', '')
    summaries.append(clean_summary)

# st.title("Live tech news summarizer")
# text = " Read full article here"

# for n, i in enumerate(summaries):
#     st.write(f"<div style='font-weight:normal'>{i}<a href='{links[n]}'>{text}</a></div><br>", unsafe_allow_html=True)



app = Flask(__name__)

@app.route("/")
def helloo():
  return render_template("home.html", summariesAndLinks=zip(summaries, links))


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)