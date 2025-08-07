# tests/test_extract.py
import pytest
from utils import extract
from unittest.mock import patch, Mock
import time
import requests

# Data HTML palsu untuk pengujian
MOCK_HTML_CONTENT = """
<div class="collection-card">
    <h3 class="product-title">T-shirt 1</h3>
    <span class="price">$100.00</span>
    <p style="color: #777">Rating: ⭐ 4.5 / 5</p>
    <p style="color: #777">Colors: 3 Colors</p>
    <p style="color: #777">Size: M</p>
    <p style="color: #777">Gender: Men</p>
</div>
<div class="collection-card">
    <h3 class="product-title">Pants 2</h3>
    <span class="price">$200.00</span>
    <p style="color: #777">Rating: ⭐ 3.0 / 5</p>
    <p style="color: #777">Colors: 5 Colors</p>
    <p style="color: #777">Size: L</p>
    <p style="color: #777">Gender: Women</p>
</div>
"""

@patch('utils.extract.requests.get')
@patch('utils.extract.time.sleep', return_value=None)
def test_scrape_single_page(mock_sleep, mock_get):
    """Menguji scraping satu halaman dengan data mock."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = MOCK_HTML_CONTENT.encode('utf-8')
    mock_get.return_value = mock_response

    products = extract.scrape_fashion_studio("https://fake-url.com/?page={}", start_page=1, end_page=1, delay=0)
    
    assert len(products) == 2
    assert products[0]['title'] == 'T-shirt 1'
    assert products[0]['price'] == '$100.00'
    assert products[0]['rating'] == '⭐ 4.5 / 5'
    assert products[0]['colors'] == '3 Colors'
    assert products[0]['size'] == 'M'
    assert products[0]['gender'] == 'Men'

@patch('utils.extract.requests.get')
@patch('utils.extract.time.sleep', return_value=None)
def test_scrape_single_page_on_error(mock_sleep, mock_get):
    """Menguji ketika ada error dari requests."""
    mock_get.side_effect = requests.exceptions.RequestException("Test error")
    
    products = extract.scrape_fashion_studio("https://fake-url.com/?page={}", start_page=1, end_page=1, delay=0)
    
    assert len(products) == 0