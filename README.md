# Identitas
- Nama    : Ahmad Rizki Daffaa
- NPM     : 2506543640
- Kelas   : PBP B

**Tautan deployment (PWS):** http://ahmad-rizki53-myportofolio.pws.cs.ui.ac.id

## Deskripsi Proyek
Web portofolio pribadi saya untuk mata kuliah Pemrograman Berbasis Platform (PBP). Halaman depannya berisi profil singkat plus tiga entri terbaru dari experience, achievement, dan project. Semua item dari ketiga section tersebut ada di punya halamannya masing-masing yang bisa dibuka lewat navbar.

Datanya sudah tidak ditulis langsung di HTML. Semua konten portofolio sekarang jadi model di app `main` dan diambil lewat Django ORM, jadi kalau ada pengalaman atau proyek baru tinggal ditambahkan lewat Django Admin. Isi awalnya saya tanam lewat data migration, jadi database yang baru dibuat langsung ada isinya, entah SQLite di laptop saya atau PostgreSQL di PWS.

Ada light/dark mode yang pilihannya disimpan di localStorage, navbar sticky yang berubah jadi dropdown di layar kecil, sertifikat yang bisa diklik untuk diperbesar, durasi tiap experience yang dihitung JavaScript dari tanggal mulainya, dan animasi salju menggunakan CSS keyframes yang tiap butirnya dibuat dengan JavaScript.

### Tech Stack
| Komponen | Keterangan |
| --- | --- |
| Bahasa | Python 3.13 |
| Framework | Django 6.1 |
| Database | SQLite (lokal), PostgreSQL (production) |
| Static files | WhiteNoise |
| WSGI server | Gunicorn (production) |
| Konfigurasi | `python-dotenv` (berkas `.env`) |
| Frontend | HTML5, CSS, JavaScript |
| Deployment | Pacil Web Service (PWS) |

Django memilih databasenya sendiri di `portofolio/settings.py`. Kalau variabel `PRODUCTION` bernilai `True`, Django pakai PostgreSQL dengan kredensial dari `.env`. Selain itu dia pakai `db.sqlite3` yang ada di root.

### Struktur Proyek
```
.
├── env/
├── main/                       # app utama, isi semua konten portofolio
│   ├── models.py               # model Experience, Achievement, Project
│   ├── views.py                # empat view: landing page + satu per section
│   ├── urls.py                 # routing app, app_name = "main"
│   ├── admin.py                # registrasi ketiga model ke Django Admin
│   ├── tests.py                # unit test
│   └── migrations/             # termasuk data migration yang menanam isi awal
├── portofolio/                 # konfigurasi proyek
│   ├── settings.py             # pemilihan database, WhiteNoise, static files
│   ├── urls.py                 # 'admin/' -> Django Admin, sisanya ke main.urls
│   ├── asgi.py
│   └── wsgi.py
├── static/
│   ├── css/style.css           # styling responsive, tema terang/gelap, salju
│   ├── js/script.js            # toggle tema, dropdown navbar, modal image, salju
│   └── img/                    # foto profil dan sertifikat (img/cert/)
├── templates/
│   ├── base.html               # head, navbar, footer, dipakai semua halaman
│   ├── index.html              # landing page
│   ├── experience.html         # halaman per section
│   ├── achievement.html
│   ├── project.html
│   └── sections/               # markup tiap section, di-include index & halamannya
├── .env
├── .env.prod
├── .gitignore
├── db.sqlite3
├── manage.py                   # entry point perintah Django
├── Procfile                    # perintah release & web untuk PWS
├── README.md
└── requirements.txt            # daftar dependensi
```

Direktori `env/` (virtual environment), berkas `.env` serta `.env.prod`, dan `db.sqlite3` tercantum di `.gitignore` sehingga tidak ada di repository github.

Markup tiap section saya taruh terpisah di `templates/sections/`. Berkas itu di-include oleh landing page maupun oleh halaman sectionnya sendiri, jadi kalau mau ubah tampilan satu section saya cukup edit satu berkas.

## Instruksi Setup
Perintah dijalankan dari direktori root repositori. Contoh di bawah pakai Git Bash di Windows, jadi aktivasi virtual environment silakan menyesuaikan shell masing-masing.

1. **Klon repositori dan masuk ke direktorinya**
   ```bash
   git clone https://github.com/demtcsre/myportofolio.git
   cd myportofolio
   ```

2. **Buat dan aktifkan virtual environment**
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
   Untuk pengembangan lokal cukup satu baris berikut supaya Django pakai SQLite:
   ```env
   PRODUCTION=False
   ```
   Kalau mau jalan dengan PostgreSQL, isi juga `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, dan `SCHEMA`, lalu ubah `PRODUCTION` jadi `True`.

5. **Jalankan migrasi**
   ```bash
   python manage.py migrate
   ```
   Perintah ini sekaligus mengisi database dengan konten portofolio lewat data migration, jadi halamannya tidak akan kosong waktu pertama dibuka.

6. **Nyalakan server pengembangan**
   ```bash
   python manage.py runserver
   ```
   Halaman portofolio bisa diakses di `http://127.0.0.1:8000/` atau `localhost:8000`. Hentikan server dengan `Ctrl + C`, dan keluar dari virtual environment dengan `deactivate`.

7. **Jalankan unit test** (opsional)
   ```bash
   python manage.py test
   ```

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
2. Tantangan utama dalam mengatur tata letak responsif adalah menumpuk struktur _multiple column_ dari layar _desktop_ menjadi satu kolom di layar _mobile_ tanpa merusak hierarki informasi. Saat resolusi mengecil menjadi di bawah 47.5rem (dikonversikan dari 760px), container hero-grid menggunakan _flex_ dengan `flex-direction: column;` dan semua item diatur agar _centered_, lebar foto dibatasi maksimal 17.5rem (dikonversikan dari 280px) agar tetap proporsional, lalu diakhiri oleh teks bio. Selain itu, menu navigasi horizontal diubah posisinya menjadi menu _dropdown_ vertikal yang dapat disembunyikan agar tampilan layar kecil tidak terlalu padat.
3. Data web saat ini masih hardcoded, bakal repot kalau ada pembaruan _portofolio_ (_project_, _experience_, _achievement_) karena harus mengedit template HTML secara manual. Memanfaatkan ***Django ORM*** dan fitur bawaan ***Django Admin*** untuk membuat _database_ dinamis. Fokus utamanya adalah membuat _app_ atau _model blogs_ agar saya bisa langsung mengelola dan memublikasikan `write-up` CTF (sebagai player maupun problem setter) atau blog _random_ melalui panel admin, tanpa perlu menyentuh kode lagi.

#### AI Disclosure
AI Chat Session Link: https://claude.ai/share/2e619a2b-ded2-4d77-91e4-37f7c2c814df

##### Penggunaan AI
- Fitur _light_/_dark_ mode yang menyimpan nilai _theme_ di _local storage_ mereka sehingga tema tersebut tetap berlaku saat halaman dimuat ulang maupun pada kunjungan berikutnya. Termasuk animasi transisi ketika _switch theme_.
- Menambahkan beberapa _section_, yaitu _experience_, _achievement_, dan _project_. Data yang menjadi isi konten di tiap _section tersebut_ disediakan oleh saya pribadi, bukan digenerate AI.
- Membuat background _header_/_navbar_ yang semulanya transparent menjadi _solid_. Adapun `position: sticky; top: 0;` pada `.site-header` header sudah tambahkan sebelum menggunakan AI.
- Membuat _navbar_ pada _header_ menjadi _dropdown menu_ ketika berada pada tampilan _mobile_ (_width_ < 760px) dan men-_centered_ list pada _navbar_ tersebut.
- Membuat tiap _achievement_ dan _project_ menggunakan `grid` agar memiliki tampilan seperti kartu.
- Membuat _section_ _experience_ dalam tampilan seperti _timeline_ yang disusun berdasarkan bulan memulai _experience_ tersebut dengan _experience_ paling atas merupakan _experience_ terakhir.
- Durasi _experience_ dihitung dengan cara menghitung _range_ (inklusif) bulan saat ini dan bulan memulai _experience_.
- Membuat _modal images_ untuk gambar sertifikat di _achievement_.
- Mengganti unit `px` menjadi `rem` di `/static/css/style.css`.

##### Perbaikan Manual
- Menambahkan `text-align: justify;` ke _class_ `.entry-note` dan `.bio` agar teks pada class tersebut "rata kiri-kanan".
- Awalnya, ketika _modal image_ diklik/dibuka, gambar tersebut tidak _centered_ dan halaman website masih bisa di-_scroll_. Perbaikan yang saya lakukan ialah menambahkan `margin: auto;` di element dengan id `lightbox` serta `overflow: hidden;` pada body ketika _modal image_ diklik/dibuka, `overflow` akan kembali `visible` ketika _modal image_ ditutup.

### Tugas 2
Di Tugas 1 semua isi portofolio masih ditulis langsung di HTML. Di tugas ini isinya dipindah ke database lewat app `main`, jadi model, routing, dan templatenya berdiri sendiri, dan datanya diambil pakai Django ORM.

#### Progres
- Membuat app `main` dan mendaftarkannya di `INSTALLED_APPS`.
- Menambahkan tiga model di `main/models.py`:
  - **Experience**; title, organization, description, category, thumbnail, started_at, ended_at, plus properti `is_ongoing`.
  - **Achievement**; title, organizer, awarded_at, certificate.
  - **Project**; name, kicker, url, description, order.
- Mengatur `Meta.ordering` di tiap model. Experience dan Achievement urut dari tanggal terbaru. Project saya kasih field `order` sendiri karena urutan berdasarkan nama ternyata beda antara SQLite dan PostgreSQL, dan saya tidak mau urutannya berubah waktu di-deploy.
- Mengganti routing proyek. `portofolio/urls.py` sekarang memanggil `include('main.urls')`, dan `portofolio/views.py` saya hapus karena `landing_page` sudah digantikan `show_main`.
- Mendaftarkan empat rute bernama di `main/urls.py` dengan `app_name = "main"`: `show_main` di `/`, lalu `show_experience`, `show_achievement`, dan `show_project`.
- Menulis empat view di `main/views.py`. `show_main` ambil tiga baris teratas tiap model pakai slice `[:3]`, tiga view sisanya ambil semuanya.
- Membagi template jadi `base.html` yang memuat navbar dan footer, serta partial per section di `templates/sections/` yang di-include landing page maupun halaman sectionnya sendiri.
- Mengganti navbar dari anchor `#section` ke tag `{% url %}`.
- Mengisi data awal lewat data migration `0003_seed_portfolio_content.py` sehingga database yang baru dibuat tidak kosong. Primary keynya diturunkan pakai `uuid5` supaya SQLite di laptop dan PostgreSQL di PWS sepakat soal id tiap baris.
- Menulis 35 unit test di `main/tests.py`: akses URL, template yang kepakai, data yang tampil, dan pesan empty state.
- Menambahkan `Procfile` berisi perintah `release` dan `web`, agar PWS tidak `migrate`.

#### Pertanyaan Reflektif
1. Contoh yang digunakan adalah ketika membuka halaman`/experience/`. Request GET ditangani `portofolio/urls.py` duluan, karena file itu yang ditunjuk `ROOT_URLCONF` di settings. Karena tidak ada yang cocok selain `''`, yang isinya `include('main.urls')`, jadi sisa URL-nya dilempar ke app. `main/urls.py` yang mencocokkan `experience/` dengan view `show_experience`.

   Rutenya diberi nama `main:show_experience`. Nama ini yang dipakai tag `{% url %}` di navbar, sehingga jikr URL-nya akan berubah maka tautan di navbar ikut berubah sendiri tanpa menyentuh HTML-nya. View memanggil `Experience.objects.all()` sebagai argumen untuk parameter context di fungsi `render()`. Kemudian ORM memroses fungsi tersebut, lengkap dengan urutan dari `Meta.ordering`.

   Tampilannya ada di folder template. `experience.html` extends `base.html` agar navbar dan footernya sama dengan halaman lain, lalu include `sections/experience.html` yang isinya `{% for %}` untuk menjabarkan queryset tadi jadi baris HTML, dengan `{% empty %}` kalau tabelnya kosong. Hasilnya dibungkus `HttpResponse` dan dikirim balik. Saat di browser, `script.js` mengisi label durasi tiap entri dari atribut `data-start` yang ditulis template.

2. Agar data yang ingin ditampilkan di banyak halaman dapat sinkron dan tidak perlu banyak perubahan kode secara manual. Landing page cuma menampilkan tiga entri terbaru, halaman sectionnya menampilkan semua. Waktu masih hardcoded, artinya harus menulis entri yang sama di dua tempat yang berbeda dan perubahan di satu tempat harus terjadi di tempat lainnya. Sekarang keduanya diambil dari data yang sama sehingga tampilan di keduanya sinkron.

   Urutan tampilan juga tidak lagi bergantung pada urutan baris di HTML, tapi ditentukan oleh `Meta.ordering`, jadi entri baru langsung masuk ke posisi yang benar tanpa digeser manual. Ketika datanya ada di database, dia bisa diperlakukan sebagai data: diambil tiga teratas dengan `[:3]`, difilter, nanti dicari atau dipaginasi. Kalau masih HTML statis, artinya perlu edit manual satu per satu. Lebih efisien juga jika mau mengubah desain kartunya karena cukup ubah di satu tempat dan tiap entri akan mengikuti.

3. In short, `makemigrations` menulis, `migrate` menjalankan. `makemigrations` membaca `models.py`, membandingkannya dengan keadaan model menurut migrasi yang sudah ada, lalu membuat berkas migrasi baru berisi langkah perubahannya. Database sama sekali tidak disentuh di tahap ini. `migrate` yang menjalankan berkas-berkas itu ke database, lalu mencatat namanya di tabel `django_migrations` supaya tidak dijalankan dua kali.

   Contohnya ada di proyek ini. Isi `EXPERIENCE_CHOICES` di `main/models.py` diganti dari daftar lama jadi delapan employment type LinkedIn. Setelah disimpan, yang berubah baru berkas Pythonnya, kolom `category` di database belum tahu kalau ada perubahan. `python manage.py makemigrations` membuat `main/migrations/0004_alter_experience_category.py` berisi operasi `AlterField`. Baru setelah `python manage.py migrate`, perubahannya benar-benar masuk ke database.

   Satu hal yang sempat terlewat ialah melakukan migrate mengganti daftar pilihan tidak otomatis memperbaiki data yang sudah tersimpan. Data lama masih menyimpan kategori yang sudah tidak ada di daftar baru. Makanya di file migrate yang sama ditambahkan `RunPython` untuk memetakan ulang nilainya. Migrasi juga tidak selalu soal struktur database, `0003_seed_portfolio_content.py` di proyek ini tidak mengubah kolom apa pun dan cuma mengisi data.

#### AI Disclosure
Model AI: Claude Code Opus 5 Extra High effort
AI Chat Session Link: https://claude.ai/code/session_019PEDDe9qcKUsx8KD1kFoD1

##### Penggunaan AI
- Merancang ketiga model dan pemilihan tipe fieldnya, termasuk mengubah `started_at` dari `DateTimeField` ber-`auto_now_add` jadi `DateField` supaya tanggal mulainya bisa saya isi sendiri.
- Membuat `main/urls.py` dan mengubah `portofolio/urls.py` supaya memakai `include`.
- Menulis keempat view, termasuk slice `[:3]` untuk landing page.
- Memecah template jadi `base.html` dan partial per section di `templates/sections/`.
- Membuat data migration `0003_seed_portfolio_content.py` dan migrasi `0004_alter_experience_category.py`.
- Menulis seluruh 35 unit test di `main/tests.py`.
- Membuat animasi salju di `static/css/style.css` beserta generator elemennya di `static/js/script.js`.
- Membuat `Procfile` untuk PWS.
- Menulis bagian Deskripsi Proyek dan memperbarui Struktur Proyek di `README.md`.

##### Perbaikan Manual
- Halaman achievement dan project sempat tampak lebih sempit dari section lain. AI menyimpulkan container keempat section sudah identik dan menyarankan perbaikan CSS, yang ternyata kurang tepat. Penyebabnya karena ada `<div class="container">` yang tidak pernah ditutup di `index.html`, sehingga kedua section itu tersarang di container kedua dan kehilangan lebar sebesar dua kali padding.
- Menentukan sendiri kategori tiap experience: TA DDP1 sebagai contract, staf CTF COMPFEST dan member NetSOS SIG sebagai seasonal.
- Mengubah tautan navbar, dan menyetel `z-index` lapisan salju jadi `-1` supaya saljunya jatuh di belakang teks.
- Menyetel padding `.section` dan `.entry-link`, serta jumlah dan ukuran butiran salju.
- Merapikan kode yang ditulis AI.