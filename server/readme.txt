Usage:
------
run the command "python server.py" without quotes from the command-line.

Environment:
------------
-> Python 2, tested on Python 2.7.6

===========================================

data types
----------
lOffer:
[offeredItem, n1, demandedItem, n2, availability, offerToken]
tOffer:
(offeredItem, n1, demandedItem, n2, availability, offerToken)
offers tuple:
tuple of (offeredItem, n1, demandedItem, n2, availability, offerToken)

Implementasi:
-------------
01. Server Status : 
02. Signup        : 80%, Eric belum dihubungkan dengan database dan belum ditest
03. Login Eric    : 70%, Eric masih ada issues dan belum ditest
04. Inventory     : 90%, Willy belum testing endpoint dan database
05. MixItem       : 90%, Willy belim testing endpoint dan database
06. Map           : 90%, Eric belum ditest
07. Move          : 80%, Willy belum testing endpoint dan database, belum dihubungkan dengan database
08. Field         : 80%, Willy belum testing endpoint dan database, belum dihubungkan dengan database
09. Offer         : 80%, Eric belum dihubungkan dengan database dan belum ditest
10. Tradebox      : 90%, Eric belum ditest
11. SendFind      : 60%, Willy belum testing endpoint dan database, belum dihubungkan dengan database, belum dengan server lain
12. FindOffer     : 80%, Willy belum testing endpoint dan database, belum dihubungkan dengan database
13. SendAccept    : 80%, Willy belum testing endpoint dan database, belum dihubungkan dengan database
14. Accept        : 80%, Eric belum dihubungkan dengan database dan belum ditest
15. FetchItem     : 80%, Willy belum testing endpoint dan database, belum dihubungkan dengan database
16. CancelOffer   : 80%, Willy belum testing endpoint dan database, belum dihubungkan dengan database

Testing:
--------
02. Login         : DONE

Design database:
----------------
users = (<u>username</u>, password, R11, R12, R13, R14, R21, R22, R23, R31, R32, R33, R41, x, y)
offers = (<u>offer_token</u>, offered_item, num_offered_item, demanded_item, num_demanded_item)

Pembagian kerja:
----------------
Eric   : 2 3 6 9 10 14
Willy  : 1 4 5 7 8 11 12 13 15 16

camelCase:
----------
Camel Case adalah penamaan variabel/method yang intuitif. Arti dari variabel atau
fungsi dari method langsung tercermin dari namanya. Pemberian nama dilakukan
dengan kata-kata yang mendeskripsikan variabel/method, dimana kata pertama
diawali huruf kecil dan kata berikutnya ditambahkan secara langsung (kontinu)
dengan huruf kapital untuk huruf pertama kata tanpa menggunakan. Sebagai contoh:
temperature
temperatureInKelvin
getAbsis()
getOrdinat()
getAbsisAndOrdinat()
toJSONValue()
JSONArray()

Terdapat beberapa pengecualian untuk huruf pertama, yaitu jika kata pertama
merupakan singkatan dari yang lain seperti JSON (Java Script Object Notation).
Untuk definisi lengkapnya silahkan dilihat di 
http://en.wikipedia.org/wiki/CamelCase.

Notes tgl 19 April 2015
-----------------------
Silahkan dipelajari implementasi server yang sudah jadi, dan ikut berkontribusi
dalam pengerjaan server ini.

Saya telah membagi tugas dengan random kepada 3 orang yaitu gw sendiri, Willy, 
dan Aurelia. Winson tidak diberikan tugas dalam pengerjaan server karena dia 
mengerjakan client.

Pembagian kerja dapat dilihat di atas pada bagian pembagian kerja.

Tentu saja pembagian kerja ini tidak optimal karena dirandom. Jika anda ingin
mengerjakan hal yang diberikan ke orang lain silahkan didiskusikan, minimal 
dengan orang yang diberikan tugas tersebut. Setelah terjadi kesepakatan silahkan
langsung diganti pembagian kerja di atas.

Cara Berkontribusi:
sister.py - bagian logika dari server
server.py - bagian penanganan koneksi dari server

Secara umum berikut langkah kerja yang akan anda lakukan dalam pengerjaan fitur:
0. Lakukan perubahan terhadap daftar implementasi di atas dengan menambahkan
   0%, <nama anda>. Daftar tersebut akan digunakan untuk melihat progress
   pengerjaan.

1. Lakukan perubahan pada sister.py dengan menambahkan fungsi yang sesuai dengan
   membuat method baru. Anda dapat menambahkan atribut baru pada kelas sesuai
   dengan kebutuhan. Penamaan atribut dan kelas harap menggunakan konvensi 
   camelCase. Penjelasan mengenai camelCase terdapat di atas.
   
   Jika anda ingin mengubah method/atribut yang sudah ada diharapkan untuk
   mendiskusikan dengan Eric terlebih dahulu.

2. Lakukan perubahan pada server.py pada bagian method handle pada 
   ThreadedSisterRequestHandler dengan menambahkan percabangan untuk fitur anda.
   Silahkan tambahkan fungsi yang anda butuhkan sebagai method dari
   ThreadedSisterRequestHandler.
   
   Jika anda kebingungan dengan menambahkan fitur pada server.py silahkan 
   hubungi Eric. Anda dapat saja kebingungan karena ThreadedSisterRequestHandler
   yang kita buat tidak menggunakan lifecyclenya secara utuh.
   
   Seperti sebelumnya, jika anda ingin mengubah method/atribut yang sudah ada
   diharapkan untuk mendiskusikan dengan Eric terlebih dahulu.

3. Update tabel Implementasi di atas sesuai dengan progress anda.