
# import requests
# from bs4 import BeautifulSoup
# import re
# from transformers import T5ForConditionalGeneration, T5TokenizerFast
from flask import Flask, render_template
import os



# # specify the URL of the news website to scrape
# url = "https://www.theverge.com/"

# # send a GET request to the website URL and store the response
# response = requests.get(url)

# # parse the HTML content of the response using BeautifulSoup
# soup = BeautifulSoup(response.content, "html.parser")

# # find all the news article links on the website
# article_links = soup.find_all("a", class_="group-hover:shadow-underline-franklin")

# l = []
# links = []

# # loop through each article link and scrape the article text
# for link in article_links:
#     # extract the URL of the article
#     article_url = link["href"]
    
#     # send a GET request to the article URL and store the response
#     article_response = requests.get(url + article_url)
#     links.append(url + article_url)

# #     # parse the HTML content of the article using BeautifulSoup
#     article_soup = BeautifulSoup(article_response.content, "html.parser")
    
# #     # find the main text content of the article and print it
#     article_text = article_soup.find_all("div", class_="duet--article--article-body-component")
#     paras = []
#     concatenated_text = ""
#     for para in article_text:
#         concatenated_text += para.text + " "
#     l.append(concatenated_text.rstrip(" "))

# timeStamps = soup.find_all("time", class_="text-gray-63 dark:text-gray-94")
# time_stamps = [element.text for element in timeStamps]
# time_stamps = time_stamps[1:6]


# div_tags = soup.find_all('div', class_='relative block w-full aspect-square')
# img_tags = []

# for div in div_tags:
#     img_tags.extend(div.find_all('img'))

# # Extract the 'src' attribute from each image tag and filter out data URIs
# img_urls = [img['src'] for img in img_tags if 'src' in img.attrs and img['src'].startswith(('http', 'https'))]



# tokenizer = T5TokenizerFast.from_pretrained("t5-small", model_max_length=512)
# model = T5ForConditionalGeneration.from_pretrained("t5-small")

summaries = ["Summary1", "summary2", "Summary3"]

# for n, i in enumerate(l):
#     inputs = tokenizer.encode("summarize: " + i, return_tensors="pt", max_length=512, truncation=True)
#     outputs = model.generate(inputs, max_length=200, min_length=80, length_penalty=2.0, num_beams=4, early_stopping=True)
#     summary = tokenizer.decode(outputs[0])
#     clean_summary = summary.replace('<pad> ', '').replace('</s>', '')
#     summaries.append(clean_summary)



app = Flask(__name__)


@app.route("/")
def helloo():
  return render_template("home.html", summariesLinksImagesStamps=zip(summaries))



if __name__ == '__main__':
  app.run(host='0.0.0.0',port=int(os.environ.get("FLASK_RUN_PORT", 5000)), debug=True)