import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfplumber
from collections import Counter

def extract_pdf_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = []
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.pdf'):
            pdf_links.append(urljoin(url, href))
    
    return pdf_links

def count_words_in_pdf(link):
    response = requests.get(link)
    with open("temp.pdf", "wb") as f:
        f.write(response.content)
    
    with pdfplumber.open("temp.pdf") as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    
    # Remove unwanted characters and split the text into words
    words = text.lower().split()
    
    # Count word occurrences
    word_count = Counter(words)
    
    return word_count

def get_top_words(word_count, top_n=20):
    top_words = word_count.most_common(top_n)
    return top_words

# Main code
url = input("Enter the URL to scrape PDF documents from: ")
pdf_links = extract_pdf_links(url)

print("PDF Links:")
for link in pdf_links:
    print(link)
    word_count = count_words_in_pdf(link)
    top_words = get_top_words(word_count)
    
    print("Top 20 Words:")
    for word, count in top_words:
        print(f"{word}: {count}")
    
    print()
