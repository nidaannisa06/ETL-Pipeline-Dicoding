import pytest
import pandas as pd
from utils import load
from unittest.mock import patch, Mock
from datetime import datetime

@pytest.fixture
def mock_df():
    """Membuat DataFrame dummy untuk pengujian load."""
    return pd.DataFrame({
        'title': ['T-shirt 1'],
        'price': [1600000],
        'rating': [4.5],
        'colors': [3],
        'size': ['M'],
        'gender': ['Men'],
        'timestamp': [datetime.now()]
    })

def test_save_to_csv(mock_df):
    """Menguji penyimpanan ke CSV."""
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        result = load.save_to_csv(mock_df)
        mock_to_csv.assert_called_once_with('products.csv', index=False)
        assert result is True

@patch('utils.load.gspread')
@patch('utils.load.Credentials')
def test_save_to_google_sheets(mock_credentials, mock_gspread, mock_df):
    """Menguji penyimpanan ke Google Sheets."""
    mock_client = Mock()
    mock_gspread.authorize.return_value = mock_client
    mock_sheet = Mock()
    mock_client.open_by_key.return_value.sheet1 = mock_sheet

    result = load.save_to_google_sheets(mock_df, 'test_sheet_id', 'test_creds.json')
    
    mock_credentials.from_service_account_file.assert_called_once()
    mock_gspread.authorize.assert_called_once()
    mock_sheet.clear.assert_called_once()
    mock_sheet.update.assert_called_once()
    assert result is True