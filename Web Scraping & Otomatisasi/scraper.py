import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"

print("Sedang mengambil data dari website...\n")

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')
    
    print("--- HASIL SCRAPING ---")
    for i, quote in enumerate(quotes, 1):
        teks_quote = quote.find('span', class_='text').text
        penulis = quote.find('small', class_='author').text
        print(f"{i}. \"{teks_quote}\"")
        print(f"   — Penulis: {penulis}\n")
else:
    print("Gagal mengakses website!")

    # fungsi dari proyek ini adalah untuk mengambil data dari sebuah web dengan cepat, dengan membuka inspect dan melihat tag dari data yang ingin kita ambil