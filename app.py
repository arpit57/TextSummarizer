
import streamlit as st
import sqlite3
from streamlit.components.v1 import html


# Connect to the database
conn = sqlite3.connect('NewsSummarizer.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Select all rows from the 'verge' table
sql_command = "SELECT * FROM verge"
cursor.execute(sql_command)

summaries_final = []s
links_final = []
# Fetch all rows and print them
rows = cursor.fetchall()
for row in rows:
    summaries_final.append(row[0])
    links_final.append(row[1])    

# Close the database connection
conn.close()



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
#     article_text = article_soup.find("div", class_="clearfix").get_text()
#     l.append(article_text)

# def get_first_thousand_words(text):
#     words = re.findall(r'\b\w+\b|[^\w\s]', text)
#     return ' '.join(words[:800])

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# summaries = []
# for i in l:
#     i = get_first_thousand_words(i)

#     summaries.append(summarizer(i, max_length=300, min_length=100))

# summariesText = [i[0]["summary_text"] for i in summaries]



st.title("Live tech news summarizer")
text = " Read full article here"

for n, i in enumerate(summaries_final):
    st.write(f"<div style='font-weight:normal'>{i}<a href='{links_final[n]}'>{text}</a></div><br>", unsafe_allow_html=True)




#     html_string = f"<div style='font-weight:normal'>{i}</div>"
# html(f"<div style='font-weight:normal'>{i}</div>")