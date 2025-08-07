from utils import extract, transform, load

def main():
    """Mengorkestrasi seluruh alur kerja ETL."""
    print("Mulai proses ETL...")
    
    # 1. Tahap Ekstraksi
    success = extract.run_extract()
    if not success:
        print("Proses ETL dihentikan karena tahap ekstraksi gagal.")
        return

    # 2. Tahap Transformasi
    transformed_df = transform.run_transform()
    if transformed_df is None:
        print("Proses ETL dihentikan karena tahap transformasi gagal.")
        return

    # 3. Tahap Pemuatan
    load.run_load(transformed_df)
    
    print("🎉 Proses ETL selesai!")

if __name__ == '__main__':
    main()