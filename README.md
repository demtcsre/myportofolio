# Identitas
- Nama    : Ahmad Rizki Daffaa
- NPM     : 2506543640
- Kelas   : PBP B

**Tautan _deployment_ (PWS):** http://ahmad-rizki53-myportofolio.pws.cs.ui.ac.id

## Deskripsi Proyek
Repositori ini berisi web portofolio pribadi yang dibangun untuk mata kuliah Pemrograman Berbasis Platform (PBP). Halaman utamanya menampilkan profil singkat, _experience_ dalam bentuk _timeline_, _achievement_ beserta _modal image_ untuk sertifikat, dan daftar _project_. Fitur tambahan di sisi klien mencakup _light_/_dark mode_ yang preferensinya disimpan di `localStorage`, _navbar_ _sticky_ yang berubah menjadi _dropdown_ pada tampilan _mobile_, serta tata letak responsif berbasis CSS `grid`.

Aplikasi berjalan di atas ***Django*** dengan satu _view_ sederhana (`landing_page`) yang merender `templates/index.html` pada URL _root_. Seluruh konten halaman saat ini masih _hardcoded_ di dalam _template_. Tahap berikutnya adalah memindahkan data _experience_, _achievement_, dan _project_ ke _database_ melalui Django ORM, lalu menambahkan _app_ blog agar `write-up` CTF dapat dipublikasikan langsung dari ***Django Admin*** tanpa menyentuh kode.

### Tech Stack
| Komponen | Keterangan |
| --- | --- |
| Bahasa | Python 3.13 |
| _Framework_ | Django 6.1 |
| _Database_ | SQLite (lokal), PostgreSQL (_production_) |
| _Static files_ | WhiteNoise |
| _WSGI server_ | Gunicorn (_production_) |
| Konfigurasi | `python-dotenv` (berkas `.env`) |
| _Frontend_ | HTML5, CSS, JavaScript |
| _Deployment_ | Pacil Web Service (PWS) |

Pemilihan _database_ dilakukan otomatis di `portofolio/settings.py`: jika variabel `PRODUCTION` bernilai `True`, Django memakai PostgreSQL dengan kredensial dari `.env`; selain itu memakai `db.sqlite3` di direktori _root_.

### Struktur Proyek
```
.
├── env/
├── portofolio/                 # konfigurasi keseluruhan app utama
│   ├── settings.py             # konfigurasi proyek, pemilihan database, WhiteNoise
│   ├── urls.py                 # routing: '' -> landing_page, 'admin/' -> Django Admin
│   ├── views.py                # view landing_page merender index.html
│   ├── asgi.py
│   └── wsgi.py
├── static/
│   ├── css/style.css           # styling website secara responsive
│   ├── js/script.js            # toggle tema, dropdown navbar, modal image
│   └── img/                    # foto profil dan sertifikat (img/cert/)
├── templates/
│   └── index.html              # keseluruhan halaman portofolio
├── .env     
├── .env.prod
├── .gitignore
├── db.sqlite3
├── manage.py                   # entry point perintah Django
├── README.md
└── requirements.txt            # daftar dependensi
```

Direktori `env/` (_virtual environment_), berkas `.env` serta `.env.prod`, dan `db.sqlite3` tercantum di `.gitignore` sehingga tidak ada di repository github.

## Instruksi Setup
Perintah dijalankan dari direktori _root_ repositori. Contoh di bawah memakai Git Bash pada Windows; aktivasi _virtual environment_ menyesuaikan _shell_ masing-masing.

1. **Klon repositori dan masuk ke direktorinya**
   ```bash
   git clone https://github.com/demtcsre/myportofolio.git
   cd myportofolio
   ```

2. **Buat dan aktifkan _virtual environment_**
   ```bash
   python -m venv env
   source env/Scripts/activate     # Git Bash (Windows)
   # env\Scripts\activate.bat      # Command Prompt (Windows)
   # env\Scripts\Activate.ps1      # PowerShell (Windows)
   # source env/bin/activate       # Linux / macOS
   ```

3. **Pasang dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Siapkan berkas `.env`**
   Untuk pengembangan lokal cukup satu baris berikut agar Django memakai SQLite:
   ```env
   PRODUCTION=False
   ```
   Jika ingin menjalankan dengan PostgreSQL, isi juga `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, dan `SCHEMA`, lalu ubah `PRODUCTION` menjadi `True`.

5. **Jalankan migrasi**
   ```bash
   python manage.py migrate
   ```

6. **Nyalakan server pengembangan**
   ```bash
   python manage.py runserver
   ```
   Halaman portofolio dapat diakses di `http://127.0.0.1:8000/` atau `localhost:8000`. Hentikan server dengan `Ctrl + C`, dan keluar dari _virtual environment_ dengan `deactivate`.

## Tugas Individu
### Tugas 1
Melanjutkan halaman "About Me" dari Tutorial 1. Halaman masih dirender oleh satu _view_ statis (`landing_page`), sehingga seluruh konten ditulis langsung di `templates/index.html` tanpa menyentuh _database_ maupun arsitektur MVT.

#### Progres
- Menambahkan tiga section baru pada halaman yang sama:
  - **Experience**; 3 entri, ditampilkan sebagai _timeline_ vertikal terurut dari pengalaman terbaru.
  - **Achievement**; 3 kartu sertifikat, masing-masing dapat diperbesar melalui _modal image_ berbasis elemen `<dialog>`.
  - **Project**; 2 kartu proyek beserta tautan repositorinya.
- Menulis aturan CSS khusus untuk tiap section baru di `static/css/style.css`: tata letak `grid` untuk kartu Achievement dan Project, struktur `timeline` dengan penanda garis untuk Experience, serta efek _hover_ dan transisi pada kartu.
- Mendesain ulang tampilan keseluruhan halaman di luar checklist minimum: skema warna berbasis _custom property_ dengan _toggle_ _light_/_dark mode_ yang persisten di `localStorage`, dan _header_ _sticky_ yang berubah menjadi menu _dropdown_ di bawah lebar 760px.
- Mengonversi seluruh satuan `px` menjadi `rem` agar ukuran mengikuti preferensi ukuran font peramban.
- Menghitung durasi tiap _experience_ secara dinamis di `static/js/script.js` dari atribut `data-start`, sehingga labelnya tidak perlu diperbarui manual tiap bulan.

#### Pertanyaan Reflektif
1. Ya, saya menggunakan elemen semantik HTML5 seperti `<header>`, `<main>`, `<section>`, `<nav>`, dan `<footer>`. Penggunaan elemen-elemen ini sangat membantu dalam membuat struktur kode menjadi jauh lebih rapi, membagi area konten secara jelas, serta meningkatkan aksesibilitas web. Saya belum menggunakan elemen `<article>` maupun `<aside>` karena halaman portofolio saat ini murni berisi informasi per _section_ tertentu (_project_, _experience_, _achievement_), sehingga belum ada konten independen seperti artikel blog maupun _sidebar_ pendukung.
2. Tantangan utama dalam mengatur tata letak responsif adalah menumpuk struktur _multiple column_ dari layar _desktop_ menjadi satu kolom di layar _mobile_ tanpa merusak hierarki informasi. Saat resolusi mengecil menjadi di bawah 47.5rem (dikonversikan dari 760px), saya mengubah hero grid menjadi tampilan _flex_ dengan `flex-direction: column;` dan semua item diatur agar _centered_, lalu lebar foto dibatasi maksimal 17.5rem (dikonversikan dari 280px) agar tetap proporsional, lalu diakhiri oleh teks bio. Selain itu, menu navigasi horizontal diubah posisinya menjadi menu _dropdown_ vertikal yang dapat disembunyikan agar tampilan layar kecil tidak terlalu padat.
3. Data web saat ini masih hardcoded, bakal repot kalau ada pembaruan _portofolio_ (_project_, _experience_, _achievement_) karena harus mengedit template HTML secara manual. Memanfaatkan ***Django ORM*** dan fitur bawaan ***Django Admin*** untuk membuat _database_ dinamis. Fokus utamanya adalah membuat _app_ atau _model blogs_ agar saya bisa langsung mengelola dan memublikasikan `write-up` CTF (sebagai player maupun problem setter) atau blog _random_ melalui panel admin, tanpa perlu menyentuh kode lagi.

#### AI Disclosure
AI Chat Session Link: https://claude.ai/share/2e619a2b-ded2-4d77-91e4-37f7c2c814df

##### Penggunaan AI
- Fitur _light_/_dark_ mode yang menyimpan nilai _theme_ di _local storage_ mereka sehingga tema tersebut tetap berlaku saat halaman dimuat ulang maupun pada kunjungan berikutnya. Termasuk animasi transisi ketika _switch theme_.
- Menambahkan beberapa _section_, yaitu _experience_, _achievement_, dan _project_. Data yang menjadi isi konten di tiap _section tersebut_ disediakan oleh saya pribadi, bukan digenerate AI.
- Membuat background _header_/_navbar_ yang semulanya transparent menjadi _solid_. Adapun `position: sticky; top: 0;` pada `.site-header` header sudah tambahkan sebelu menggunakan AI.
- Membuat _navbar_ pada _header_ menjadi _dropdown menu_ ketika berada pada tampilan _mobile_ (_width_ < 760px) dan men-_centered_ list pada _navbar_ tersebut.
- Membuat tiap _achievement_ dan _project_ menggunakan `grid` agar memiliki tampilan seperti kartu.
- Membuat _section_ _experience_ dalam tampilan seperti _timeline_ yang disusun berdasarkan bulan memulai _experience_ tersebut dengan _experience_ paling atas merupakan _experience_ terakhir.
- Durasi _experience_ dihitung dengan cara menghitung _range_ (inklusif) bulan saat ini dan bulan memulai _experience_.
- Membuat _modal images_ untuk gambar sertifikat di _achievement_.
- Mengganti unit `px` menjadi `rem` di `/static/css/style.css`.

##### Perbaikan Manual
- Menambahkan `text-align: justify;` ke _class_ `.entry-note` dan `.bio` agar teks pada class tersebut "rata kiri-kanan".
- Awalnya, ketika _modal image_ diklik/dibuka, gambar tersebut tidak _centered_ dan halaman website masih bisa di-_scroll_. Perbaikan yang saya lakukan ialah menambahkan `margin: auto;` di element dengan id `lightbox` serta `overflow: hidden;` pada body ketika _modal image_ diklik/dibuka, `overflow` akan kembali `visible` ketika _modal image_ ditutup.
