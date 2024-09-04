
# TASK 2

Apa itu **runas**? runas adalah file binary yang dimana biasanya untuk login **active directory** yang tidak di ketehaui tempat login active directory tersebut. EXAMPLE:

```powershell
runas.exe /netonly /user:<domain>\<username> cmd.exe
```


#### Parameter:

- **/netonly:**
  - Digunakan ketika kita tidak tergabung dalam domain.
  - Memuat kredensial untuk otentikasi jaringan tetapi tidak mengautentikasi terhadap pengontrol domain.
  - Perintah yang dijalankan secara lokal akan berjalan dalam konteks akun Windows standar.
  - Koneksi jaringan akan menggunakan akun yang ditentukan.

- **/user:**
  - Menyediakan detail domain dan nama pengguna.
  - Sebaiknya gunakan Nama Domain yang Sepenuhnya Memenuhi Syarat (FQDN) daripada nama domain NetBIOS untuk membantu penyelesaian.

- **cmd.exe:**
  - Program yang ingin dijalankan setelah kredensial dimasukkan.
  - Pilihan paling aman adalah `cmd.exe` karena dapat digunakan untuk meluncurkan program lain dengan kredensial yang dimasukkan.

#### Contoh Penggunaan:

```powershell
runas.exe /netonly /user.com\nama pengguna cmd.exe
```

**Configurasi DNS Manual**

```powershell
$dnsip = "<DC IP>"
$index = Get-NetAdapter -Name 'Ethernet' | Select-Object -ExpandProperty 'ifIndex'
Set-DnsClientServerAddress -InterfaceIndex $index -ServerAddresses $dnsip
```

##### IP vs Nama Host

#### Pertanyaan:
Apakah ada perbedaan antara perintah `dir \\za.tryhackme.com\SYSVOL` dan `dir \\<DC IP>\SYSVOL` dan mengapa ada keributan besar tentang DNS?

#### Jawaban:
Ya, ada perbedaan signifikan yang berkaitan dengan metode otentikasi yang digunakan:

1. **Nama Host:**
   - Menggunakan nama host (`\\za.tryhackme.com\SYSVOL`) akan mencoba melakukan otentikasi Kerberos terlebih dahulu.
   - Kerberos bergantung pada nama host yang tertanam dalam tiket.

2. **Alamat IP:**
   - Menggunakan alamat IP (`\\<DC IP>\SYSVOL`) dapat memaksa penggunaan otentikasi NTLM.
   - Ini terjadi karena Kerberos tidak dapat menggunakan IP address untuk otentikasi, sehingga otentikasi beralih ke NTLM.

#### Kesimpulan:
Perbedaan ini menekankan pentingnya DNS dalam otentikasi jaringan, karena metode otentikasi yang digunakan (Kerberos vs. NTLM) dapat mempengaruhi keamanan dan performa.


## Task 4

### Menggunakan Perintah `net` untuk Mencantumkan Pengguna di Domain AD

Kita bisa menggunakan perintah `net` dengan sub-opsi `user` untuk mencantumkan semua pengguna di domain Active Directory (AD).

#### Perintah:

```powershell
net user /domain
```

#### Fungsi: 
- **net user /domain:** 
- Menampilkan daftar semua pengguna yang ada di domain AD.

**Melihat detail user pada domain:***

```poweshell
net user zoe.marshall /domain
```

**Response:**
```poweshell
The request will be processed at a domain controller for domain za.tryhackme.com.

User name                    zoe.marshall
Full Name                    Zoe Marshall
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            2/24/2022 11:06:06 PM
Password expires             Never
Password changeable          2/24/2022 11:06:06 PM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   Never

Logon hours allowed          All

Local Group Memberships
Global Group memberships     *Domain Users         *Internet Access
The command completed successfully.
```


#### GROUP

Kita bisa menggunakan `net` perintah untuk menghitung grup domain dengan menggunakan `group` sub-opsi:

```powershell
C:\>net group /domain
The request will be processed at a domain controller for domain za.tryhackme.com

Group Accounts for \\THMDC

-------------------------------------------------------------------------------
*Cloneable Domain Controllers
*DnsUpdateProxy
*Domain Admins
*Domain Computers
*Domain Controllers
*Domain Guests
*Domain Users
[...]
*Schema Admins
*Server Admins
*Tier 0 Admins
*Tier 1 Admins
*Tier 2 Admins
The command completed successfully.
```

**Mendapatkan Detail Group pada domain:***

```powershell
C:\>net group "Tier 1 Admins" /domain
The request will be processed at a domain controller for domain za.tryhackme.com

Group name     Tier 1 Admins
Comment

Members

-------------------------------------------------------------------------------
t1_arthur.tyler          t1_gary.moss             t1_henry.miller
t1_jill.wallis           t1_joel.stephenson       t1_marian.yates
t1_rosie.bryant
The command completed successfully.
```

##### Password Policy

Kita bisa menggunakan `net` perintah untuk menghitung kebijakan kata sandi domain dengan menggunakan `accounts` sub-opsi:

```powershell
C:\>net accounts /domain
The request will be processed at a domain controller for domain za.tryhackme.com

Force user logoff how long after time expires?:       Never
Minimum password age (days):                          0
Maximum password age (days):                          Unlimited
Minimum password length:                              0
Length of password history maintained:                None
Lockout threshold:                                    Never
Lockout duration (minutes):                           30
Lockout observation window (minutes):                 30
Computer role:                                        PRIMARY
The command completed successfully.
```

### Informasi yang Diperoleh dari `net accounts /domain`

Perintah `net accounts /domain` memberikan informasi berguna seperti:

- **Panjang Riwayat Kata Sandi:**
  - Jumlah kata sandi unik yang harus diberikan pengguna sebelum dapat menggunakan kembali kata sandi lama.

- **Ambang Batas Penguncian:**
  - Jumlah upaya kata sandi yang salah sebelum akun dikunci dan durasi penguncian akun.

- **Panjang Minimum Kata Sandi:**
  - Panjang minimum yang harus dipenuhi oleh kata sandi pengguna.

- **Usia Maksimum Kata Sandi:**
  - Durasi maksimum kata sandi dapat digunakan sebelum harus diubah, menunjukkan apakah rotasi kata sandi diperlukan secara berkala.


### Kekurangan

- Perintah `net` harus dijalankan dari mesin yang bergabung dengan domain. Jika tidak, mesin akan menggunakan domain WORKGROUP secara default.
- Perintah `net` mungkin tidak menampilkan semua informasi. Misalnya, jika pengguna adalah anggota lebih dari sepuluh grup, tidak semua grup akan ditampilkan di output.


## Task 5 PowerShell


**Get-ADUser:**
fungsi GetADUser adalah untuk melihat detail pengguna AD:

```powershell
PS C:\Users\david.cook> Get-ADUser -Identity aaron.harris -Server za.tryhackme.com -Properties *


AccountExpirationDate                :
accountExpires                       : 9223372036854775807
AccountLockoutTime                   :
AccountNotDelegated                  : False
AllowReversiblePasswordEncryption    : False
AuthenticationPolicy                 : {}
AuthenticationPolicySilo             : {}
BadLogonCount                        : 0
badPasswordTime                      : 0
badPwdCount                          : 0
CannotChangePassword                 : False
CanonicalName                        : za.tryhackme.com/People/Finance/aaron.harris
Certificates                         : {}
City                                 :
CN                                   : aaron.harris
codePage                             : 0
Company                              :
CompoundIdentitySupported            : {}
Country                              :
countryCode                          : 0
Created                              : 2/24/2022 10:05:11 PM
createTimeStamp                      : 2/24/2022 10:05:11 PM
Deleted                              :
Department                           : Finance
Description                          :
DisplayName                          : Aaron Harris
DistinguishedName                    : CN=aaron.harris,OU=Finance,OU=People,DC=za,DC=tryhackme,DC=com
Division                             :
DoesNotRequirePreAuth                : False
dSCorePropagationData                : {1/1/1601 12:00:00 AM} 
EmailAddress                         :
EmployeeID                           :
EmployeeNumber                       :
Enabled                              : True
Fax                                  :
GivenName                            : Aaron
HomeDirectory                        :
HomedirRequired                      : False
HomeDrive                            :
HomePage                             :
HomePhone                            :
Initials                             :
instanceType                         : 4
isDeleted                            :
KerberosEncryptionType               : {}
LastBadPasswordAttempt               :
LastKnownParent                      :
lastLogoff                           : 0
lastLogon                            : 0
LastLogonDate                        :
LockedOut                            : False
logonCount                           : 0
LogonWorkstations                    :
Manager                              :
MemberOf                             : {CN=Internet Access,OU=Groups,DC=za,DC=tryhackme,DC=com}
MNSLogonAccount                      : False
MobilePhone                          :
Modified                             : 2/24/2022 10:05:11 PM
modifyTimeStamp                      : 2/24/2022 10:05:11 PM
msDS-User-Account-Control-Computed   : 0
Name                                 : aaron.harris
nTSecurityDescriptor                 : System.DirectoryServices.ActiveDirectorySecurity
ObjectCategory                       : CN=Person,CN=Schema,CN=Configuration,DC=za,DC=tryhackme,DC=com
ObjectClass                          : user
ObjectGUID                           : 34f3c068-f4d3-4dee-9176-18d06deb7048
objectSid                            : S-1-5-21-3330634377-1326264276-632209373-1598
Office                               :
OfficePhone                          :
Organization                         :
OtherName                            :
PasswordExpired                      : False
PasswordLastSet                      : 2/24/2022 10:05:11 PM
PasswordNeverExpires                 : False
PasswordNotRequired                  : False
POBox                                :
PostalCode                           :
PrimaryGroup                         : CN=Domain Users,CN=Users,DC=za,DC=tryhackme,DC=com
primaryGroupID                       : 513
PrincipalsAllowedToDelegateToAccount : {}
ProfilePath                          :
ProtectedFromAccidentalDeletion      : False
pwdLastSet                           : 132902139115950227
SamAccountName                       : aaron.harris
sAMAccountType                       : 805306368
ScriptPath                           :
sDRightsEffective                    : 0
ServicePrincipalNames                : {}
SID                                  : S-1-5-21-3330634377-1326264276-632209373-1598
SIDHistory                           : {}
SmartcardLogonRequired               : False
sn                                   : Harris
State                                :
StreetAddress                        :
Surname                              : Harris
Title                                : Mid-level
TrustedForDelegation                 : False
TrustedToAuthForDelegation           : False
UseDESKeyOnly                        : False
userAccountControl                   : 512
userCertificate                      : {}
UserPrincipalName                    :
uSNChanged                           : 17296
uSNCreated                           : 17292
whenChanged                          : 2/24/2022 10:05:11 PM
whenCreated                          : 2/24/2022 10:05:11 PM
```

Parameter digunakan untuk hal berikut:

-  -Identitas - Nama akun yang kami enumerasi
- -Properti - Properti mana yang terkait dengan akun yang akan ditampilkan, * akan menampilkan semua properti
- -Server - Karena kita tidak tergabung dalam domain, kita harus menggunakan parameter ini untuk mengarahkannya ke pengontrol domain kita

**Filter:**
kita juga dapat menggunakan `-Filter` parameter yang memungkinkan kontrol lebih besar atas enumerasi dan penggunaan `Format-Table` cmdlet untuk menampilkan hasil seperti berikut dengan rapi:

```powershell
PS C:\Users\david.cook> Get-ADUser -Filter 'Name -like "*stevens"' -Server za.tryhackme.com | Format-Table Name,SamAccountName -A

Name             SamAccountName   
----             --------------
chloe.stevens    chloe.stevens
samantha.stevens samantha.stevens
mohammed.stevens mohammed.stevens
jacob.stevens    jacob.stevens
timothy.stevens  timothy.stevens
trevor.stevens   trevor.stevens
owen.stevens     owen.stevens
jane.stevens     jane.stevens
janice.stevens   janice.stevens
gordon.stevens   gordon.stevens
```

**Group:**
kita bisa menggunakan group untuk melihat detail group AD:

```powershell
PS C:\> Get-ADGroup -Identity Administrators -Server za.tryhackme.com


DistinguishedName : CN=Administrators,CN=Builtin,DC=za,DC=tryhackme,DC=com
GroupCategory     : Security
GroupScope        : DomainLocal
Name              : Administrators
ObjectClass       : group
ObjectGUID        : f4d1cbcd-4a6f-4531-8550-0394c3273c4f
SamAccountName    : Administrators
SID               : S-1-5-32-544
```

```powershell
PS C:\Users\david.cook> Get-ADGroup -Identity "Domain Users" -Server za.tryhackme.com


DistinguishedName : CN=Domain Users,CN=Users,DC=za,DC=tryhackme,DC=com
GroupCategory     : Security
GroupScope        : Global
Name              : Domain Users
ObjectClass       : group
ObjectGUID        : 5a8a92da-1fad-414b-86ac-4dc612d72fda
SamAccountName    : Domain Users
SID               : S-1-5-21-3330634377-1326264276-632209373-513
```

**Get-ADGroupMember:**
kita bisa menggunakan `Get-ADGroupMember` untuk menghitung keanggotaan group (Kaya ngasih tau semua user yang ada di group / domain itu)

```powershell
PS C:\Users\david.cook> Get-ADGroupMember -Identity Administrators -Server za.tryhackme.com


distinguishedName : CN=Domain Admins,CN=Users,DC=za,DC=tryhackme,DC=com
name              : Domain Admins
objectClass       : group
objectGUID        : 8a6186e5-e20f-4f13-b1b0-067f3326f67c
SamAccountName    : Domain Admins
SID               : S-1-5-21-3330634377-1326264276-632209373-512

distinguishedName : CN=Enterprise Admins,CN=Users,DC=za,DC=tryhackme,DC=com 
name              : Enterprise Admins
objectClass       : group
objectGUID        : 93846b04-25b9-4915-baca-e98cce4541c6
SamAccountName    : Enterprise Admins
SID               : S-1-5-21-3330634377-1326264276-632209373-519

distinguishedName : CN=vagrant,CN=Users,DC=za,DC=tryhackme,DC=com 
name              : vagrant
objectClass       : user
objectGUID        : ed901eff-9ec0-4851-ba32-7a26a8f0858f
SamAccountName    : vagrant
SID               : S-1-5-21-3330634377-1326264276-632209373-1000

distinguishedName : CN=Administrator,CN=Users,DC=za,DC=tryhackme,DC=com 
name              : Administrator
objectClass       : user
objectGUID        : b10fe384-bcce-450b-85c8-218e3c79b30f
SamAccountName    : Administrator
SID               : S-1-5-21-3330634377-1326264276-632209373-500

```


## AD Objects

### Pencarian Objek AD Menggunakan `Get-ADObject`

Pencarian umum untuk objek AD dapat dilakukan menggunakan cmdlet `Get-ADObject`. Misalnya, untuk mencari semua objek AD yang diubah setelah tanggal tertentu:

```powershell
Get-ADObject -Filter 'WhenChanged -gt "YYYY-MM-DD"'
```

```powershell
PS C:\> $ChangeDate = New-Object DateTime(2022, 02, 28, 12, 00, 00)
PS C:\> Get-ADObject -Filter 'whenChanged -gt $ChangeDate' -includeDeletedObjects -Server za.tryhackme.com

Deleted           :
DistinguishedName : DC=za,DC=tryhackme,DC=com
Name              : za
ObjectClass       : domainDNS
ObjectGUID        : 518ee1e7-f427-4e91-a081-bb75e655ce7a

Deleted           :
DistinguishedName : CN=Administrator,CN=Users,DC=za,DC=tryhackme,DC=com
Name              : Administrator
ObjectClass       : user
ObjectGUID        : b10fe384-bcce-450b-85c8-218e3c79b30f
```

## Domain

### Mengambil Informasi Domain Menggunakan `Get-ADDomain`

Untuk mengambil informasi tambahan tentang domain tertentu, kita bisa menggunakan cmdlet `Get-ADDomain`:

```powershell
Get-ADDomain
```


```powershell
PS C:\Users\david.cook> Get-ADDomain -Server za.tryhackme.com

AllowedDNSSuffixes                 : {}
ChildDomains                       : {}
ComputersContainer                 : CN=Computers,DC=za,DC=tryhackme,DC=com
DeletedObjectsContainer            : CN=Deleted Objects,DC=za,DC=tryhackme,DC=com
DistinguishedName                  : DC=za,DC=tryhackme,DC=com
DNSRoot                            : za.tryhackme.com
DomainControllersContainer         : OU=Domain Controllers,DC=za,DC=tryhackme,DC=com
DomainMode                         : Windows2012R2Domain
DomainSID                          : S-1-5-21-3330634377-1326264276-632209373
ForeignSecurityPrincipalsContainer : CN=ForeignSecurityPrincipals,DC=za,DC=tryhackme,DC=com
Forest                             : za.tryhackme.com
InfrastructureMaster               : THMDC.za.tryhackme.com
LastLogonReplicationInterval       :
LinkedGroupPolicyObjects           : {CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=za,DC=tryhackme,DC=com}
LostAndFoundContainer              : CN=LostAndFound,DC=za,DC=tryhackme,DC=com
ManagedBy                          :
Name                               : za
NetBIOSName                        : ZA
ObjectClass                        : domainDNS
ObjectGUID                         : 518ee1e7-f427-4e91-a081-bb75e655ce7a
ParentDomain                       :
PDCEmulator                        : THMDC.za.tryhackme.com
PublicKeyRequiredPasswordRolling   :
QuotasContainer                    : CN=NTDS Quotas,DC=za,DC=tryhackme,DC=com
ReadOnlyReplicaDirectoryServers    : {}
ReplicaDirectoryServers            : {THMDC.za.tryhackme.com}
RIDMaster                          : THMDC.za.tryhackme.com
SubordinateReferences              : {DC=ForestDnsZones,DC=za,DC=tryhackme,DC=com, DC=DomainDnsZones,DC=za,DC=tryhackme,DC=com, CN=Configuration,DC=za,DC=tryhackme,DC=com}
SystemsContainer                   : CN=System,DC=za,DC=tryhackme,DC=com
UsersContainer                     : CN=Users,DC=za,DC=tryhackme,DC=com
```


### Mengubah Objek AD Menggunakan `Set-ADAccountPassword`

Cmdlet AD-RSAT memungkinkan pembuatan objek AD baru atau mengubah objek yang sudah ada. Fokus jaringan ini adalah pencacahan, sedangkan pembuatan atau perubahan objek dianggap sebagai eksploitasi AD, yang akan dibahas di modul AD nanti.

Contoh mengubah kata sandi pengguna AD menggunakan cmdlet `Set-ADAccountPassword`:

```powershell
Set-ADAccountPassword -Identity <Username> -NewPassword (ConvertTo-SecureString -AsPlainText "<NewPassword>" -Force)
```


### Manfaat

- Cmdlet PowerShell dapat menghitung lebih banyak informasi daripada perintah `net` dari Command Prompt.
- Kita dapat menentukan server dan domain untuk menjalankan perintah menggunakan `runas` dari mesin yang tidak bergabung dengan domain.
- Kita dapat membuat cmdlet sendiri untuk menghitung informasi spesifik.
- Cmdlet AD-RSAT dapat digunakan untuk mengubah objek AD secara langsung, seperti mengatur ulang kata sandi atau menambahkan pengguna ke grup tertentu.

### Kekurangan

- PowerShell sering lebih dipantau oleh tim biru dibandingkan Command Prompt.
- Perkakas AD-RSAT harus diinstal, atau menggunakan skrip lain yang berpotensi terdeteksi untuk enumerasi PowerShell.

## Task 6 

Bloodhound adalah sebuat tool untuk enum AD yang sangat kuat, Sharphound dan Bloodhound itu tidak sama. Sharphound adalah alat enumerasi Bloodhound. ini di gunakan untuk menghitung informasi AD yang kemudian di tampilkan secara visual oleh di Bloodhound.

**Ada tiga kolektor Sharphound yang berbeda:**

- **Sharphound.ps1** - Skrip PowerShell untuk menjalankan Sharphound. Namun rilis terbaru Sharphound telah berhenti merilis versi skrip Powershell. Versi ini bagus untuk digunakan dengan RAT karena skrip dapat dimuat langsung ke memori, menghindari AV pada disk. pemindaian  
    
- **Sharphound.exe** - Versi Windows yang dapat dijalankan untuk menjalankan Sharphound.

- **AzureHound.ps1** - Skrip PowerShell untuk menjalankan instans Sharphound untuk Azure (Microsoft Cloud Computing Services). Bloodhound dapat menyerap data yang dihitung dari Azure untuk menemukan jalur serangan yang terkait dengan konfigurasi Azure Identity and Access Management.

example jalankan script

```powershell
Sharphound.exe --CollectionMethods <Methods> --Domain za.tryhackme.com --ExcludeDCs
```

**Parameter dijelaskan:**

- **CollectionMethods** - Menentukan jenis data apa yang akan dikumpulkan Sharphound. Opsi yang paling umum adalah Default atau Semua. Selain itu, karena Sharphound menyimpan informasi dalam cache, setelah proses pertama selesai, Anda hanya dapat menggunakan metode pengumpulan Sesi untuk mengambil sesi pengguna baru guna mempercepat proses.

- **Domain** - Di sini, kita menentukan domain yang ingin kita enumerasi. Dalam beberapa kasus, Anda mungkin ingin menghitung domain induk atau domain lain yang memiliki kepercayaan terhadap domain Anda yang sudah ada. Anda dapat memberi tahu Sharphound domain mana yang harus dihitung dengan mengubah parameter ini.

- **ExcludeDCs** -Ini akan menginstruksikan Sharphound untuk tidak menyentuh pengontrol domain, yang mengurangi kemungkinan bahwa Sharphound dijalankan akan memunculkan peringatan.
