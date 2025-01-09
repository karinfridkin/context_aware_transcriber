import requests
from bs4 import BeautifulSoup

# Function to extract context from a text file
def extract_text_from_file(file_path):
    with open(file_path, "r") as file:
        text = file.read()
        print("the text is:", text)
    return text

# Function to extract context from a URL
def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    return text