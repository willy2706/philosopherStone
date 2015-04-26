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
localOffer list:
map of offerToken -> [offeredItem, n1, demandedItem, n2, availability, username]
inventory list:
[n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]
userRecord:
{'x': int, 'y': int, 'password': string, 'inventory': <inventory list>, 'actionTime': int}
gameMap:
{'name', 'width', 'height', 'map': matrix}

Design database:
----------------
users = (<u>username</u>, password, R11, R12, R13, R14, R21, R22, R23, R31, R32, R33, R41, x, y, action_time, last_field)
offers = (<u>offer_token</u>, username, offered_item, num_offered_item, demanded_item, num_demanded_item, availability)

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