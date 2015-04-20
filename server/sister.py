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
OfferException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

'''
The Logic of Server.
Instance objects:
-> registeredUser: map of username @ map
   -> password: string
   -> loggedOn: boolean
   -> offers: map of offerToken @ list
       0> int: oferred item id
       1> int: number of offered item
       2> int: demanded item id
       3> int: number of demanded item
       4> boolean: availability, false means already sold
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
    

    def getInventory(self, token): #belum testing
        username = self.loggedUser.get(token)
        if username:
            res = c.execute('SELECT * FROM inventories')
            return res
        else:
            raise TokenException('invalid token')
