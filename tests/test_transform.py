# tests/test_transform.py
import pytest
import pandas as pd
from utils import transform
import numpy as np

@pytest.fixture
def sample_data():
    """Membuat DataFrame mentah untuk pengujian."""
    data = {
        'title': ['T-shirt 1', 'T-shirt 1', 'Unknown Product', 'Hoodie'],
        'price': ['$100.00', '$100.00', 'Invalid Price', '$496.88'],
        'rating': ['⭐ 4.5 / 5', '⭐ 4.5 / 5', 'Invalid Rating', '⭐ 4.8 / 5'],
        'colors': ['3 Colors', '3 Colors', 'No Color Info', '5 Colors'],
        'size': ['Size: M', 'Size: M', 'Size: L', 'Size: XXL'],
        'gender': ['Gender: Men', 'Gender: Men', 'Gender: Women', 'Gender: Unisex'],
        'timestamp': [
            pd.Timestamp('2025-01-01'), 
            pd.Timestamp('2025-01-01'), 
            pd.Timestamp('2025-01-02'), 
            pd.Timestamp('2025-01-03')
        ]
    }
    return pd.DataFrame(data)

def test_clean_data(sample_data):
    """Menguji pembersihan data secara menyeluruh."""
    df = transform.clean_data(sample_data)
    
    # Memastikan duplikat, null, dan invalid data dihapus
    assert len(df) == 1
    
    # Memeriksa konversi dan pembersihan kolom
    assert df.iloc[0]['title'] == 'Hoodie'
    assert df.iloc[0]['price'] == 7950080
    assert df.iloc[0]['rating'] == 4.8
    assert df.iloc[0]['colors'] == 5
    assert df.iloc[0]['size'] == 'XXL'
    assert df.iloc[0]['gender'] == 'Unisex'