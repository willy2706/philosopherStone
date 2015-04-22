import hashlib
import time
import calendar
import json
import sqlite3
import random

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
   -> inventory: list
-> loggedUser: map of token @ username
-> gameMap
-> allOffers: map offerToken @ list
   -> offeredItem
   -> n1
   -> demandedItem
   -> n2
   -> availability
   -> username
-> salt: string appended to be hashed
-> servers: list of map
   -> ip: string
   -> port: int
'''
class SisterServerLogic():
    def printUser(self):
        res = c.execute("SELECT * FROM users")
        for row in res:
            print row[0]
            print row[1]

    def getUser(self, username):
        res = c.execute("SELECT * FROM users WHERE username = " + username).fetchone()
        return res

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
            raise IndexItemException('invalid item')

    def synchronizeInventories(self):
        for i in range (0,10):
            self.registeredUser[username]['inventory'][i] = res[i+2]

    def __init__(self):
        self.conn = sqlite3.connect('sister.db', check_same_thread=False) #otomatis bikin kalau ga ada
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARCHAR(255) NOT NULL, R11 INT NOT NULL DEFAULT 0, R12 INT NOT NULL DEFAULT 0, R13 INT NOT NULL DEFAULT 0, R14 INT NOT NULL DEFAULT 0, R21 INT NOT NULL DEFAULT 0, R22 INT NOT NULL DEFAULT 0, R23 INT NOT NULL DEFAULT 0, R31 INT NOT NULL DEFAULT 0, R32 INT NOT NULL DEFAULT 0, R41 INT NOT NULL DEFAULT 0, X INT NOT NULL DEFAULT 0, Y INT NOT NULL DEFAULT 0, PRIMARY KEY(username))")
        self.c.execute("CREATE TABLE IF NOT EXISTS offers (offer_token VARCHAR(255), username VARCHAR(255) NOT NULL, offered_item INT NOT NULL, num_offered_item INT NOT NULL, demanded_item INT NOT NULL, num_demanded_item INT NOT NULL, availability TINYINT NOT NULL, PRIMARY KEY(offer_token), FOREIGN KEY(username) REFERENCES users(username))")
        try:
            self.c.execute("INSERT INTO users(username, password) VALUES ('willy2', '%s')"%hashlib.md5('1234').hexdigest())
        except Exception, e:
            print e

        self.conn.commit() #buat save
        print "database create and connect successfully"
        self.registeredUser = {}
        self.loggedUser = {}
        self.loadMap('map.json')
        self.salt = 'mi0IUsW4'
        self.allOffers = {}

    '''
    Set the list of servers
    '''
    def serverStatus(self, servers):
        self.servers = servers

    '''
    Signup a user.
    Possible Exceptions: UsernameException
    '''
    def signup(self, name, password):
        if self.isUsernameRegistered(name):
            raise UsernameException('username exists')

        self.registerUserWithPassword(name, password)

    '''
    Login a user. Return (token, x, y, time) on success.
    Possible Exceptions:
    -> UsernameException
    '''
    def login(self, name, password):
        mRecord = self.getRecordByName(name)
        
        if mRecord.get('password') != hashlib.md5(password).hexdigest():
            raise UsernameException('username/password combination is not found')

        unixTime = calendar.timegm(time.gmtime())
        token = hashlib.md5(name).hexdigest()

        self.setLogin(token, name)
        return (token, 0, 0, unixTime)

    '''
    Get the inventory of a token.
    '''
    def getInventory(self, token):
        username = self.getNameByToken(token)

        return self.getInventory0(username)

    '''
    Get the inventory of a user.
    '''
    def getInventory0(self, username):
        return self.registeredUser[username].get('inventory')

        '''
        res = c.execute("SELECT * FROM users WHERE username = " + username).fetchone()
        self.synchronizeInventories()
        return (res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[10], res[11])
        '''

    '''
    Mix 2 categories with 3 each to 1 higher quality item.
    throwable: IndexItemException, TokenException, MixtureException.
    '''
    def mixItem (self, token, item1, item2):
        self.validateIndexItem(item1)
        self.validateIndexItem(item2)

        username = self.getNameByToken(token)
        record = self.getRecordByName(username)
        mInventory = record.get('inventory')

        if mInventory.get(item1) < 3:
            raise MixtureException('first item is not enough')
        if mInventory.get(item2) < 3:
            raise MixtureException('second item is not enough')

        numItem1 = mInventory.get(item1) - 3 #item 1 jumlahnya kurang 3
        numItem2 = mInventory.get(item2) - 3 #item 2 jumlahnya kurang 3

        itemRes = self.processMix(item1, item2) # dapatkan index item hasil penggabungan, ini ada potensi throw exception

        numItemRes = mInventory.get(itemRes) + 1 #item hasil gabung jumlahnya kurang 3

        mInventory[item1] = numItem1
        mInventory[item2] = numItem2
        mInventory[itemRes] = numItemRes

        self.updateRecord(username, {'inventory':mInventory})
        return numItemRes

    '''
    Returns the name, width, and height of the map in this server.
    '''
    def getMap(self, token):
        self.getNameByToken(token)

        name = self.gameMap['name']
        width = self.gameMap['width']
        height = self.gameMap['height']
        return (name, width, height)

    '''
    Move a user.
    Possible Exceptions: TokenException
    '''
    def move(self, token, x, y):
        username = self.getNameByToken(token)

        unixTime = calendar.timegm(time.gmtime())
        self.updateRecord(username, {'x':x,'y':y})
        return unixTime

    '''
    Collect item from current position.
    Possible Exceptions: TokenException
    '''
    def field(self, token):
        username = self.getNameByToken(token)

        mRecord = self.getRecordByName(username)

        x = mRecord.get('x')
        y = mRecord.get('y')
        nameItem = self.gameMap.get('map')[x][y]
        index = self.mappingNameItemToIndex(nameItem)
        mRecord['inventory'][index] += 1

        self.updateField(username, mRecord)

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
    Possible Exceptions: TokenException
    '''
    def tradebox(self, token):
        username = self.getNameByToken(token)

        return self.getOffers(username)

    '''
    Put an offer.
    Possible Exceptions: TokenException, OfferException
    '''
    def putOffer(self, token, offeredItem, n1, demandedItem, n2):
        username = self.getNameByToken(token)

        mRecord = self.getRecordByName(username)
        numItem = mRecord['inventory'].get(offeredItem)

        if numItem < n1:
            raise OfferException('insufficient')

        # userOffers = self.registeredUser[username].get('offers')
        # if not userOffers:
        #    userOffers = {}

        # generate offer
        unixTime = calendar.timegm(time.gmtime())
        lOfferToken = [token, str(unixTime)]
        lOfferToken += [self.salt, str(random.randint(-2147483648, 2147483647))]
        lOfferToken += [chr(ord('A')+offeredItem), str(n1)]
        lOfferToken += [chr(ord('A')+demandedItem), str(n2)]
        offerToken = hashlib.md5(''.join(lOfferToken)).hexdigest()

        self.addOffer(username, offerToken, offeredItem, n1, demandedItem, n2, True)
        # userOffers[offerToken] = [offeredItem, n1, demandedItem, n2, True]
        # allOffers[offerToken] = username

    '''
    Accept an offer from client.
    '''
    def sendAccept(self, token, offerToken):
        #TODO gabung dengan accept
        username = self.loggedUser.get(token)
        retTup = {}
        if username:
            username_offers = self.allOffers.get(offerToken)
            if username == username_offers:
                raise LogicException('you cannot accept item you offer')
            else:
                offers = self.registeredUser[username]['offers'][offerToken]
                offeredItem = offers[0]
                numOfferedItem = offers[1]
                demandItem = offers[2]
                numDemandItem = offers[3]
                availability = offers[4]
                if availability:
                    if self.registeredUser[username]['inventory'][demandItem] > numDemandItem:
                        self.registeredUser[username]['inventory'][offeredItem] += numOfferedItem
                        self.registeredUser[username]['inventory'][demandItem] -= numDemandItem
                    else:
                        raise OfferException('you have not enough the demanded item')
                else:
                    raise OfferException('offered not available anymore')
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
    Find an item that requested from client
    throwable: IndexItemException, TokenException, MixtureException.
    '''
    def sendFind (self, token, item):
        #TODO gabung dengan find offer
        username = self.getNameByToken(token)

        retTup = []
        self.validateIndexItem(item1)
        for un, m in self.registeredUser:
            if un != username: #kan mau nya find offer yang bukan punya dia
                offerLists = m['offers']
                for offerToken, offers in offerLists:
                    if (offers[0] == item and offers[4] == True):
                        tup1 = offers + (key,)
                        retTup = retTup + (tup,)
                return retTup

    '''
    Find an item that requested from server
    throwable: IndexItemException, MixtureException.
    '''
    def findOffer (self, item):
        retTup = {}
        self.validateIndexItem(item1)
        for un, m in self.registeredUser:
            offerLists = m['offers']
            for offerToken, offers in offerLists:
                if (offers[0] == item and offers[4] == True):
                    tup1 = offers + (key,)
                    retTup = retTup + (tup,)
            return retTup

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
                    self.registeredUser[username]['inventory'][demand_id] += num_demand_id
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
                    self.registeredUser[username]['inventory'][offered_id] += num_offered_id
                    del self.registeredUser[username]['offers'][offerToken]
                else:
                    raise LogicException('you cannot fetch item that has not been accept')
            else:
                raise TokenException('invalid offer_token')    
        else:
            raise TokenException('invalid token')

    '''
    Check whether username is registered within the system.
    '''
    def isUsernameRegistered(self, username):
        res = self.c.execute("SELECT * FROM users WHERE username = '" + username + "'").fetchone()
        return res != None
        # TODO: tanya eric kode dibawah gimana?
        # return username in self.registeredUser

    '''
    Register a user.
    '''
    def registerUserWithPassword(self, username, password):
        self.registeredUser[username] = {'password': hashlib.md5(password).hexdigest()}
        self.c.execute("INSERT INTO users(username, password) VALUES ('%s', '%s')"%(username,hashlib.md5(password).hexdigest()))
        self.conn.commit()


    '''
    Get record of user.
    Possible Exceptions: UsernameException
    '''
    def getRecordByName(self, username):
        res = self.c.execute("SELECT * FROM users WHERE username = '" + username + "'").fetchone()
        if res == None:
            return UsernameException('username not found in database')
        record = {}
        record['x'] = res[12]
        record['y'] = res[13]
        print 'kkk'
        record['password'] = res[1]
        record['inventory'] = [res[i] for i in range(2, 12)]
        record['loggedOn'] = False
        if record:
            return record
        else:
            raise UsernameException('username/password combination is not found')

    '''
    Login the user and set token.
    '''
    def setLogin(self, token, username):
        self.loggedUser[token] = username
        self.updateRecord(username, {'loggedOn':True})

    '''
    Update the record of a user.
    '''
    def updateRecord(self, username, updated):
        self.registeredUser.update(updated)

        #c.execute("UPDATE users SET " + mappingIndexItemToName[item1] + " = " + numItem1 + ", " + mappingIndexItemToName[item2] + " = " + numItem2 + ", " + mappingIndexItemToName[itemRes] + " = " + numItemRes + " WHERE username = " + username)
        #conn.commit()
        #self.synchronizeInventories()

    '''
    Get the username of a userToken.
    '''
    def getNameByToken(self, token):
        result = self.loggedUser.get(token)
        if result:
            return result
        else:
            raise TokenException('invalid token')

    '''
    Add an offer to the system.
    '''
    def addOffer(self, username, offerToken, offeredItem, n1, demandedItem, n2, availability):
        self.allOffers[offerToken] = [offeredItem, n1, demandedItem, n2, availability, username]

    '''
    Get offers for a username.
    '''
    def getOffers(self, username):
        return tuple(tuple(val[:-1]) + (key,) for key, val in
              self.allOffers.items() if val[-1] == username)
