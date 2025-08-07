import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials


def save_to_csv(df, output_path='products.csv'):
    """Menyimpan DataFrame ke dalam file CSV dengan penanganan kesalahan."""
    try:
        df.to_csv(output_path, index=False)
        print(f"✅ Data berhasil disimpan ke {output_path}")
        return True
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat menyimpan file CSV: {e}")
        return False

def save_to_google_sheets(df, sheet_id, credentials_file='google-sheets-api.json'):
    """Menyimpan DataFrame ke Google Sheets dengan penanganan kesalahan."""
    try:
        print("🚀 Memuat data ke Google Sheets...")
        
        # Mengonversi kolom timestamp ke string agar bisa diserialisasi
        df['timestamp'] = df['timestamp'].astype(str)
        
        # Otorisasi menggunakan service account
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Buka sheet dan pilih worksheet pertama
        sheet = client.open_by_key(sheet_id).sheet1
        
        # Hapus semua data lama dan tulis data baru
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        
        print(f"✅ Data berhasil disimpan ke Google Sheets. Link: https://docs.google.com/spreadsheets/d/{sheet_id}")
        return True
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat menyimpan ke Google Sheets: {e}")
        return False

def run_load(df):
    """Fungsi utama untuk menjalankan proses pemuatan data."""
    if df is not None:
        # Konfigurasi
        # Ganti dengan Google Sheet ID milik Anda
        google_sheet_id = "1Yhf4Cqj7EkGq89987ujYMB7u-h6yTmKf-Bk2uH4TGBQ"
        
        # Jalankan proses pemuatan
        save_to_csv(df)
        save_to_google_sheets(df, google_sheet_id)
        
    else:
        print("❌ Tidak ada data untuk dimuat. Proses dibatalkan.")

if __name__ == '__main__':
    # Contoh penggunaan dengan data dummy
    df_dummy = pd.DataFrame({
        'title': ['test1'], 'price': [16000], 'rating': [4.5],
        'colors': [3], 'size': ['M'], 'gender': ['Men'], 'timestamp': [datetime.now()]
    })
    run_load(df_dummy)