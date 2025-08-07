# utils/extract.py
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """Mengambil konten HTML dari URL dengan penanganan kesalahan."""
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"❌ Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None

def extract_product_data(card_element):
    """Mengambil data produk dari elemen div (collection-card) dengan penanganan kesalahan."""
    product_data = {
        'title': None, 'price': None, 'rating': None,
        'colors': None, 'size': None, 'gender': None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        title_elem = card_element.find('h3', class_='product-title')
        if title_elem:
            product_data['title'] = title_elem.get_text().strip()

        price_elem = card_element.find('span', class_='price')
        if price_elem:
            product_data['price'] = price_elem.get_text().strip()
        
        info_paragraphs = card_element.find_all('p', style=lambda x: x and 'color: #777' in x)
        for p in info_paragraphs:
            text = p.get_text().strip()
            if 'Rating:' in text:
                product_data['rating'] = text.replace('Rating:', '').strip()
            elif 'Colors:' in text:
                product_data['colors'] = text.replace('Colors:', '').strip()
            elif 'Size:' in text:
                product_data['size'] = text.replace('Size: ', '').strip()
            elif 'Gender:' in text:
                product_data['gender'] = text.replace('Gender: ', '').strip()
    except Exception as e:
        print(f"⚠️ Kesalahan saat mengekstrak data produk: {e}")
        return None
    return product_data

def scrape_fashion_studio(base_url, start_page=1, end_page=50, delay=1):
    """Fungsi utama untuk mengambil data dari situs dengan penanganan kesalahan."""
    all_products = []
    try:
        for page_number in range(start_page, end_page + 1):
            url = base_url.format(page_number)
            print(f"Scraping halaman: {url}")
            content = fetching_content(url)
            if content:
                soup = BeautifulSoup(content, "html.parser")
                product_cards = soup.find_all('div', class_='collection-card')
                for card in product_cards:
                    product = extract_product_data(card)
                    if product:
                        all_products.append(product)
                time.sleep(delay)
            else:
                print(f"Gagal mendapatkan konten dari {url}. Menghentikan scraping.")
                break
    except Exception as e:
        print(f"❌ Terjadi kesalahan pada proses scraping: {e}")
    return all_products

def run_extract():
    """Menjalankan proses ekstraksi dan menyimpan hasilnya."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/?page={}'
    print("🚀 Memulai proses ekstraksi...")
    all_products_data = scrape_fashion_studio(BASE_URL, start_page=1, end_page=50)
    if all_products_data:
        try:
            df = pd.DataFrame(all_products_data)
            df.to_csv('raw_data.csv', index=False)
            print(f"✅ Data berhasil disimpan ke raw_data.csv. Total data: {len(df)}")
            return True
        except Exception as e:
            print(f"❌ Gagal menyimpan data ke CSV: {e}")
            return False
    else:
        print("❌ Gagal mendapatkan data, file tidak dibuat.")
        return False