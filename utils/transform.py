import pandas as pd
import numpy as np

def clean_data(df):
    """
    Membersihkan dan mentransformasi data dengan penanganan kesalahan.
    """
    try:
        # Menghapus duplikat
        print("🔧 Menghapus duplikat...")
        df.drop_duplicates(inplace=True)
        
        # Mengubah 'None' string menjadi NaN
        df.replace('None', np.nan, inplace=True)
        
        # Menghapus baris dengan nilai null
        print("🔧 Menghapus data null...")
        df.dropna(inplace=True)
        
        # Membersihkan dan mengonversi kolom 'price'
        print("🔧 Mengonversi mata uang 'Price' ke Rupiah...")
        df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).str.strip()
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df.dropna(subset=['price'], inplace=True)
        df['price'] = (df['price'] * 16000).astype(int)
        
        # Membersihkan dan mengonversi 'Rating'
        print("🔧 Membersihkan dan mengonversi 'Rating'...")
        df['rating'] = df['rating'].astype(str).str.replace('⭐ ', '', regex=False).str.replace(' / 5', '', regex=False).str.strip()
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df.dropna(subset=['rating'], inplace=True)
        
        # Membersihkan dan mengonversi 'Colors'
        print("🔧 Membersihkan dan mengonversi 'Colors'...")
        df['colors'] = df['colors'].astype(str).str.replace(' Colors', '', regex=False).str.strip()
        df['colors'] = pd.to_numeric(df['colors'], errors='coerce')
        df.dropna(subset=['colors'], inplace=True)
        df['colors'] = df['colors'].astype(int)
        
        # Membersihkan kolom 'Size'
        print("🔧 Membersihkan kolom 'Size'...")
        df['size'] = df['size'].astype(str).str.replace('Size: ', '', regex=False).str.strip()
        
        # Membersihkan kolom 'Gender'
        print("🔧 Membersihkan kolom 'Gender'...")
        df['gender'] = df['gender'].astype(str).str.replace('Gender: ', '', regex=False).str.strip()
        
        # Menghapus data invalid
        print("🔧 Menghapus data invalid...")
        df = df[~df['title'].isin(['Unknown Product', ''])]
        
        return df

    except Exception as e:
        print(f"❌ Terjadi kesalahan pada proses transformasi data: {e}")
        return pd.DataFrame()

def run_transform():
    """Fungsi utama untuk menjalankan proses transformasi."""
    print("🚀 Memulai proses transformasi...")
    try:
        df = pd.read_csv('raw_data.csv')
        transformed_df = clean_data(df)
        if transformed_df is not None:
            return transformed_df
    except FileNotFoundError:
        print("❌ File raw_data.csv tidak ditemukan. Jalankan extract.py terlebih dahulu.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat memuat file CSV: {e}")
    return None