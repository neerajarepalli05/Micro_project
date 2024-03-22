from flask import Flask, render_template, request
from googlesearch import search
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch text content from a URL
def get_page_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text content from the page
        text = ' '.join([p.text for p in soup.find_all('p')])
        return text
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return ""

# Function to perform Google search and generate a paragraph of text
def generate_paragraph(query, num_results):
    paragraph = ""
    for j, result in enumerate(search(query, num=num_results, stop=num_results, pause=2)):
        result_text = get_page_text(result)
        paragraph += result_text + " "
    return paragraph

@app.route('/', methods=['GET', 'POST'])
def index():
    paragraph = None
    if request.method == 'POST':
        query = request.form['query']
        num_results = int(request.form['num_results'])
        paragraph = generate_paragraph(query, num_results)
    return render_template('index.html', paragraph=paragraph)

if __name__ == '__main__':
    app.run(debug=True)
