# Proyek Analisis Data: E-Commerce Public Dataset

Proyek ini merupakan submission akhir kelas analisis data, menggunakan E-Commerce Public Dataset. Analisis mencakup proses data wrangling, exploratory data analysis, RFM analysis, dan geospatial analysis, dilengkapi dengan dashboard interaktif menggunakan Streamlit.

## Struktur Direktori

```
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───data
│   ├───customers_dataset.csv
│   ├───geolocation_dataset.csv
│   ├───order_items_dataset.csv
│   ├───order_payments_dataset.csv
│   ├───order_reviews_dataset.csv
│   ├───orders_dataset.csv
│   ├───product_category_name_translation.csv
│   ├───products_dataset.csv
│   └───sellers_dataset.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Cara Menjalankan Dashboard Secara Local

1. Pastikan Python 3.9 ke atas sudah terpasang di komputer Anda.
2. Buat dan aktifkan virtual environment (opsional tetapi disarankan).

```
python -m venv venv
source venv/bin/activate        # untuk MacOS/Linux
venv\Scripts\activate           # untuk Windows
```

3. Install seluruh library yang dibutuhkan.

```
pip install -r requirements.txt
```

4. Masuk ke folder `dashboard`, lalu jalankan aplikasi Streamlit.

```
cd dashboard
streamlit run dashboard.py
```

5. Dashboard akan otomatis terbuka di browser pada alamat `http://localhost:8501`. Jika tidak terbuka otomatis, salin alamat tersebut ke browser secara manual.

## Cara Menjalankan Notebook Analisis

1. Install seluruh library pada `requirements.txt` beserta `jupyter`.
2. Buka `notebook.ipynb` menggunakan Jupyter Notebook, JupyterLab, atau Google Colab.
3. Jalankan seluruh cell secara berurutan dari atas ke bawah (Run All). Notebook membaca dataset dari folder `data/`, jadi pastikan struktur folder tidak diubah.

## Ringkasan Pertanyaan Bisnis

1. Bagaimana tren jumlah pesanan bulanan sepanjang Januari 2017 - Agustus 2018, dan kategori produk apa yang memberikan kontribusi revenue terbesar?
2. Bagaimana segmentasi pelanggan berdasarkan RFM Analysis, dan segmen mana yang perlu diprioritaskan untuk kampanye retensi?
3. Negara bagian mana di Brazil yang memiliki rata-rata waktu pengiriman paling lama, dan bagaimana hubungannya dengan skor ulasan pelanggan?

## Deployment

Tautan dashboard yang sudah dideploy ke Streamlit Community Cloud dapat dilihat pada berkas `url.txt`.
