# Aplikasi Perpustakaan Sederhana

Program ini adalah aplikasi perpustakaan berbasis terminal yang ditulis dengan C++.
Data contoh memuat minimal 50 buku dan disimpan pada `data/books.csv`. Tampilan tabel
menggunakan pemformatan kolom agar rapi dan mudah dibaca.

## Fitur
- Menampilkan seluruh koleksi buku dalam tabel rapi.
- Pencarian buku berdasarkan judul atau penulis (tidak peka huruf besar/kecil).
- Peminjaman dan pengembalian buku dengan pengecekan ketersediaan.
- Ringkasan koleksi (total judul, tersedia, dan sedang dipinjam).
- Penyimpanan perubahan status ke `data/books.csv` sebelum keluar.

## Menjalankan
Pastikan g++ terpasang, kemudian kompilasi dan jalankan:

```bash
g++ -std=c++17 main.cpp -o library_app
./library_app
```

File CSV disertakan dengan status awal buku (tersedia/dipinjam). Anda dapat
mengubah isinya secara manual atau melalui aplikasi.
