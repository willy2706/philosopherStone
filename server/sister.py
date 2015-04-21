import md5
import time
import calendar
import json
import sqlite3

'''
The Exception raised when the server is having problem with usernames.
'''
class UsernameException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

'''
The Exception raised when the server is having problem with tokens.
'''
class TokenException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

'''
The Exception raised when the server is having problem with offers.
'''
class OfferException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value


'''
The Exception raised when the server is having problem with mixture.
'''
class MixtureException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value


'''
The Exception raised when the server is having problem with item's index.
'''
class IndexItemException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

'''
The Exception raised when the server is having problem with logic.
'''
class LogicException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

'''
The Logic of Server.
Instance objects:
-> registeredUser: map of username @ map
   -> x: integer
   -> y: integer
   -> password: string
   -> loggedOn: boolean
   -> offers: map of offerToken @ list
       0> int: oferred item id
       1> int: number of offered item
       2> int: demanded item id
       3> int: number of demanded item
       4> boolean: availability, false means already sold
   -> inventories: list 
-> loggedUser: map of token @ username
-> gameMap
-> allOffers: map offerToken @ username
-> salt: string appended to be hashed
'''
class SisterServerLogic():
    def printUser(self):
        res = c.execute("SELECT * FROM users")
        for row in res:
            print row[0]
            print row[1]

    def mix(self, item1, item2):
        if (item1 == 0 and item2 == 1):
            return 4
        elif (item1 == 1 and item2 ==  2):
            return 5
        elif (item1 == 2 and item2 == 3):
            return 6
        elif (item1 == 4 and item2 == 5):
            return 7
        elif (item1 == 5 and item2 == 6):
            return 8
        elif (item1 == 7 and item2 == 8):
            return 9

    def processMix (self, item1, item2):
        res = self.mix(item1, item2)
        if res == None:
            res = self.mix(item2, item1)
            if res == None:
                raise MixtureException ('no combination of the items')
            else:
                return res
        else:  
            return res

    def mappingIndexItemToName (self, index):
        if index == 0:
            return 'R11'
        elif index == 1:
            return 'R12'
        elif index == 2:
            return 'R13'
        elif index == 3:
            return 'R14'
        elif index == 4:
            return 'R21'
        elif index == 5:
            return 'R22'
        elif index == 6:
            return 'R23'
        elif index == 7:
            return 'R31'
        elif index == 8:
            return 'R32'
        elif index == 9:
            return 'R41'

    def mappingNameItemToIndex(self, name):
        if name == 'R11':
            return 0
        elif name == 'R12':
            return 1
        elif name == 'R13':
            return 2
        elif name == 'R14':
            return 3
        elif name == 'R21':
            return 4
        elif name == 'R22':
            return 5
        elif name == 'R23':
            return 6
        elif name == 'R31':
            return 7
        elif name == 'R32':
            return 8
        elif name == 'R41':
            return 9

    def validateIndexItem (self, index):
        if (index < 0 or index > 9):
            raise IndexItemException ('invalid item')

    def synchronizeInventories(self):
        for i in range (0,10):
            self.registeredUser[username]['inventories'][i] = res[i+2]

    def __init__(self):
        conn = sqlite3.connect('sister.db') #otomatis bikin kalau ga ada
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARCHAR(255), R11 INT, R12 INT, R13 INT, R14 INT, R21 INT, R22 INT, R23 INT, R31 INT, R32 INT, R41 INT, PRIMARY KEY(username))")
        # try:
        try:
            c.execute("INSERT INTO users(username, password) VALUES ('willy', '1234')")
        except Exception, e:
            print 'uda dimasukkan'

        conn.commit() #buat save
        print "database create and connect successfully"
        self.registeredUser = {}
        self.loggedUser = {}
        self.loadMap('map.json')
        self.salt = 'mi0IUsW4'

    '''
    Signup a user
    '''
    def signup(self, name, password):
        # c.execute("INSERT INTO users(username, password) VALUES ("+"'"+name+"', '"+ password + "'" +")") #belum testing

        if name in self.registeredUser:
            raise UsernameException('username exists')
        
        self.registeredUser[name] = {'password': password}


    '''
    Login a user. Return (token, x, y, time) on success.
    Possible Exceptions:
    -> UsernameException
    '''
    def login(self, name, password):
        mPassword = self.registeredUser.get(name)
        if mPassword:
            if mPassword != password:
                raise UsernameException('username/password combination is not found')

            unixTime = calendar.timegm(time.gmtime())
            token = md5.new(name).hexdigest()

            self.loggedUser[token] = name
            self.registeredUser[name]['loggedOn'] = True
            # TODO: x, y itu apa? posisi dia sebelumnya ya?
            return (token, 0, 0, unixTime)
            
        else:
            raise UsernameException('username/password combination is not found')    

    '''
    Returns the name, width, and height of the map in this server.
    '''
    def getMap(self, token):
        if token not in self.loggedUser:
            raise TokenException('invalid token')

        name = self.gameMap['name']
        width = self.gameMap['width']
        height = self.gameMap['height']
        return (name, width, height)
        
    '''
    Load map from file containg a JSON, on current directory.
    '''
    def loadMap(self, filename):
        mapFile = open(filename, 'r+')
        mapText = mapFile.read()
        mapFile.close()

        self.gameMap = json.loads(mapText)

    '''
    Get all trade for a user token.
    '''
    def tradebox(self, token):
        username = self.loggedUser.get(token)

        if username:
            return tuple(tumple(val) + (key,) for key, val in
                  self.registeredUser[username].get('offers', {}))
        
        else: # token not found
            raise TokenException('invalid token')

    '''
    Put an offer.
    '''
    def putOffer(self, token, offered_item, n1, demanded_item, n2):
        username = self.loggedUser.get(token)
        if username:
            # TODO: dapatkan banyak barang dengan id offered_item pada inventory user
            numItem = 5

            if numItem < n1:
                raise OfferException('insufficient')
            
            userOffers = self.registeredUser[username].get('offers')
            if not userOffers:
                userOffers = {}

            # generate offer
            unixTime = calendar.timegm(time.gmtime())
            lOfferToken = [token, str(unixTime)]
            lOfferToken += [salt, str(random.randint(-2147483648, 2147483647))]
            lOfferToken += [chr(ord('A')+offered_item), str(n1)]
            lOfferToken += [chr(ord('A')+demanded_item), str(n2)]
            offerToken = md5.new(''.join(lOfferToken)).hexdigest()
            
            userOffers[offerToken] = [offered_item, n1, demanded_item, n2, True]
            allOffers[offerToken] = username
            
        else:
            raise TokenException('invalid token')

    '''
    Accept an offer.
    '''
    def accept(self, offerToken):
        username = self.allOffers.get(offerToken)
        if username:
            if self.registeredUser[username]['offers'][offerToken][4]:
                self.registeredUser[username]['offers'][offerToken][4] = False
            else:
                raise OfferException('offer is not available')
        
        else:
            raise OfferException('offer is not available')
    

    '''
    Get the inventory of a user.
    throwable: IndexItemException.
    '''
    def getInventory(self, token): #belum testing
        username = self.loggedUser.get(token)
        if username:
            res = c.execute("SELECT * FROM users WHERE username = " + username).fetchone()
            self.synchronizeInventories()
            return (res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[10], res[11])
        else:
            raise TokenException('invalid token')

    '''
    Mix 2 categories with 3 each to 1
    throwable: IndexItemException, TokenException, MixtureException.
    '''
    def mixItem (self, token, item1, item2):
        username = self.loggedUser.get(token)
        if username:
            self.validateIndexItem(item1)
            self.validateIndexItem(item2)
            res = c.execute("SELECT * FROM users WHERE username = " + username).fetchone()
            if res[item1+2] < 3: #2 karena R11 ada di kolom 2 di database, index 0 == kolom 2
                raise MixtureException('first item is not enough')
            elif res[item2+2] < 3:
                raise MixtureException('second item is not enough')
            else:
                numItem1 = res[item1+2] - 3 #item 1 jumlahnya kurang 3
                numItem2 = res[item2+2] - 3 #item 2 jumlahnya kurang 3
                itemRes = self.processMix(item1, item2) # dapatkan index item hasil penggabungan, ini ada potensi throw exception
                numItemRes = res[itemRes+2] + 1 #item hasil gabung jumlahnya kurang 3
                c.execute("UPDATE users SET " + mappingIndexItemToName[item1] + " = " + numItem1 + ", " + mappingIndexItemToName[item2] + " = " + numItem2 + ", " + mappingIndexItemToName[itemRes] + " = " + numItemRes + " WHERE username = " + username)
                conn.commit()
                self.synchronizeInventories()
                return numItemRes
        else:
            raise TokenException('invalid token')

    '''
    Mix 2 categories with 3 each to 1
    throwable: IndexItemException, TokenException, MixtureException.
    '''
    def sendFind (self, token, item):
        username = self.loggedUser.get(token)
        retTup = {}
        if username:
            self.validateIndexItem(item1)
            for un, m in self.registeredUser:
                if un != username: #kan mau nya find offer yang bukan punya dia
                    offerLists = m['offers']
                    for offerToken, offers in offerLists:
                        if (offers[0] == item and offers[4] == True):
                            tup1 = offers + (key,)
                            retTup = retTup + (tup,)
                    return retTup
        else:
            raise TokenException('invalid token')

    def fetchItem(self, token, offer_token):
        username = self.loggedUser.get(token)
        username_offer = self.allOffers.get(offer_token)

        if username:
            if username_offer:
                if username != username_offer:
                    raise LogicException('you do not offer the item. Logic error?')
                if self.registeredUser[username]['offers'][offerToken][4]:
                    raise LogicException('you cannot fetch item that has not been accept')
                else:
                    offered_id = self.registeredUser[username]['offers'][offerToken][0]
                    num_offered_id = self.registeredUser[username]['offers'][offerToken][1]
                    demand_id = self.registeredUser[username]['offers'][offerToken][2]
                    num_demand_id = self.registeredUser[username]['offers'][offerToken][3]
                    # self.registeredUser[username]['inventories'][offered_id] -= num_offered_id #TODO: INI SEBELUMNYA UDA KURANG YA?
                    self.registeredUser[username]['inventories'][demand_id] += num_demand_id 
                    #self.registeredUser[username]['offers'].pop(offer_token)
                    del self.registeredUser[username]['offers'][offerToken]
            else:
                raise TokenException('invalid offer_token')    
        else:
            raise TokenException('invalid token')

    def cancelOffer(self, token, offer_token):
        username = self.loggedUser.get(token)
        username_offer = self.allOffers.get(offer_token)

        if username:
            if username_offer:
                if username != username_offer:
                    raise LogicException('you do not offer the item. Logic error?')
                if self.registeredUser[username]['offers'][offerToken][4]:
                    offered_id = self.registeredUser[username]['offers'][offerToken][0]
                    num_offered_id = self.registeredUser[username]['offers'][offerToken][1]
                    #dibalikin, item yang di offer bertambah
                    self.registeredUser[username]['inventories'][offered_id] += num_offered_id
                    del self.registeredUser[username]['offers'][offerToken]
                else:
                    raise LogicException('you cannot fetch item that has not been accept')
            else:
                raise TokenException('invalid offer_token')    
        else:
            raise TokenException('invalid token')

    def move(self, token, x, y):
        username = self.loggedUser.get(token)
        if username:
            unixTime = calendar.timegm(time.gmtime())

            self.registeredUser[username]['x'] = x
            self.registeredUser[username]['y'] = y
            return unixTime
        else:
            raise TokenException('invalid token')    

    def field(self, token):
        username = self.loggedUser.get(token)
        if username:
            x = self.registeredUser[username]['x']
            y = self.registeredUser[username]['y']
            nameItem = self.gameMap['map'][x][y]
            index = self.mappingNameItemToIndex(nameItem)
            self.registeredUser[username]['inventories'][index] += 1 
        else:
            raise TokenException('invalid token')