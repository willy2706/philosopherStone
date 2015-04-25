import hashlib
import json
import sqlite3
import random
import helpers
import os
<<<<<<< HEAD
import helpers
=======
>>>>>>> parent of 969db33... harusnya sudah bisa testing secara local, ayo testing :3

import foreignOffers
import sisterexceptions


DATABASE_FILE = 'sister.db'


class SisterServerLogic():
    """
    The Logic of Server.
    Instance objects:
    -> loggedUser: map of token @ username
    -> gameMap: {'name', 'width', 'height', 'map': matrix}
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
    -> conn: sqlite3 database
    -> actionTime: int, you can only move / fetch after this time
    """

    def __init__(self):
        """
        Initialize the serverLogic.
        :return: None
        """
        if os.path.isfile(DATABASE_FILE):
            # new database
            # database akan otomatis dibikin kalau ga ada
            self.conn = sqlite3.connect('sister.db', check_same_thread = False)

            c = self.conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARCHAR(255) NOT NULL, "
                      "R11 INT UNSIGNED NOT NULL DEFAULT 0, R12 INT UNSIGNED NOT NULL DEFAULT 0, R13 INT UNSIGNED NOT NULL DEFAULT 0, "
                      "R14 INT UNSIGNED NOT NULL DEFAULT 0, R21 INT UNSIGNED NOT NULL DEFAULT 0, R22 INT UNSIGNED NOT NULL DEFAULT 0, "
                      "R23 INT UNSIGNED NOT NULL DEFAULT 0, R31 INT UNSIGNED NOT NULL DEFAULT 0, R32 INT UNSIGNED NOT NULL DEFAULT 0, "
                      "R41 INT UNSIGNED NOT NULL DEFAULT 0, X INT NOT NULL DEFAULT 0, Y INT NOT NULL DEFAULT 0, "
                      "action_time INT UNSIGNED NOT NULL DEFAULT 0, PRIMARY KEY(username))")
            c.execute("CREATE TABLE IF NOT EXISTS offers (offer_token VARCHAR(255), username VARCHAR(255) NOT NULL, "
                      "offered_item INT NOT NULL, num_offered_item INT NOT NULL, demanded_item INT NOT NULL, "
                      "num_demanded_item INT NOT NULL, availability TINYINT NOT NULL, PRIMARY KEY(offer_token), "
                      "FOREIGN KEY (username) REFERENCES users(username))")
            # buat save
            self.conn.commit()

        else:
            self.conn = sqlite3.connect('sister.db')

        # self.c.execute(
        # "INSERT INTO users(username, password) VALUES ('willy2', '%s')" % hashlib.md5('1234').hexdigest())

        self.loggedUser = {}
        self.allOffers = {}
        self.actionTime = {}
        self.loadMap('map.json')
        self.salt = 'mi0IUsW4'
        self.foreignOffers = foreignOffers.ServerDealer()

    def serverStatus(self, servers):
        """
        Set the list of servers.
        :param servers: list of {'ip': string, 'port': int}
        :return: None
        """

        self.foreignOffers.setServers(servers)

    def signup(self, name, password):
        """
        Signup a user.

        :param name: string
        :param password: string
        :return: None
        :exception: UsernameException
        """

        if self.isUsernameRegistered(name):
            raise sisterexceptions.UsernameException('username exists')

        self.registerUserWithPassword(name, password)

    def login(self, name, password):
        """
        Login a user. Return  on success.

        :param name: string
        :param password: string
        :return: (token, x, y, time)
        :exception: UsernameException
        """

        mRecord = self.getRecordByName(name)

        if mRecord.get('password') != hashlib.md5(password).hexdigest():
            raise sisterexceptions.UsernameException('username/password combination is not found')
        
        unixTime = mRecord.get('actionTime')
        token = hashlib.md5(name).hexdigest()

        self.setLogin(token, name)
        return (token, mRecord.get('x'), mRecord.get('y'), unixTime)

    def getInventory(self, userToken):
        """
        Get the inventory of a userToken.
        :param userToken: string
        :return: [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]
        :exception: TokenException
        """

        username = self.getNameByToken(userToken)

        return self.getRecordByName(username).get('inventory')

    def mixItem(self, userToken, item1, item2):
        """
        Mix 3 items of 2 categories to 1 higher quality item.

        :param userToken: string
        :param item1: int
        :param item2: int
        :return: int, itemID of created item
        :exception: IndexItemException, TokenException, MixtureException
        """

        self.validateIndexItem(item1)
        self.validateIndexItem(item2)

        username = self.getNameByToken(userToken)
        record = self.getRecordByName(username)

        mInventory = record.get('inventory')

        if mInventory.get(item1) < 3:
            raise sisterexceptions.MixtureException('first item is not enough')
        if mInventory.get(item2) < 3:
            raise sisterexceptions.MixtureException('second item is not enough')

        # get the id of the resulting item
        itemRes = self.processMix(item1, item2)

        # mixing OK, reduce item1, item2, increase itemRes
        numItem1 = mInventory.get(item1) - 3  # item 1 jumlahnya kurang 3
        numItem2 = mInventory.get(item2) - 3  # item 2 jumlahnya kurang 3
        numItemRes = mInventory.get(itemRes) + 1  # item hasil gabung jumlahnya tambah 1

        mInventory[item1] = numItem1
        mInventory[item2] = numItem2
        mInventory[itemRes] = numItemRes

        self.updateRecord(username, {'inventory': mInventory})
        return numItemRes

    def processMix(self, item1, item2):
        """
        Determine the itemID of the mix of item1 and item2.

        :param item1: int
        :param item2: int
        :return: int, itemID of created item.
        """
        res = self.mix(item1, item2)

        if res == None:
            res = self.mix(item2, item1)
        if res == None:
            raise sisterexceptions.MixtureException('no combination of the items')

        return res

    def mix(self, item1, item2):
        """
        Determine the itemID of the mix of item1 and item2.
        This method will fail if the item1 > item2.

        :param item1: int
        :param item2: int
        :return: int, itemID of the result
        """

        if (item1 == 0 and item2 == 1):
            return 4
        elif (item1 == 1 and item2 == 2):
            return 5
        elif (item1 == 2 and item2 == 3):
            return 6
        elif (item1 == 4 and item2 == 5):
            return 7
        elif (item1 == 5 and item2 == 6):
            return 8
        elif (item1 == 7 and item2 == 8):
            return 9

    def getMap(self, userToken):
        """
        Returns the name, width, and height of the map in this server.

        :param userToken: string
        :return: (name, width, height)
        """

        self.getNameByToken(userToken)

        name = self.gameMap['name']
        width = self.gameMap['width']
        height = self.gameMap['height']
        return (name, width, height)

    def move(self, userToken, x, y):
        """
        Move a user.
        :param userToken: string
        :param x: int
        :param y: int
        :return: int, completion time in unix time
        :exception: TokenException, MoveException
        """

        username = self.getNameByToken(userToken)

        if x < 0 or x >= self.gameMap.get('width') or y < 0 or y >= self.gameMap.get('height'):
            raise sisterexceptions.MoveException('position out of bounds')

        record = self.getRecordByName(username)
        prevX = record.get('x')
        prevY = record.get('y')

        if prevX == x and prevY == y:
            raise sisterexceptions.MoveException('invalid move')

        currTime = helpers.getCurrentTime()
        if record.get('actionTime') > currTime:
            raise sisterexceptions.MoveException('you are still moving')

        # time in seconds
        eachStep = 1
        timeNeeded = (abs(prevX-x) + abs(prevY-y)) * eachStep

        unixTime = currTime + timeNeeded
        self.actionTime = unixTime
        self.updateRecord(username, {'x': x, 'y': y, 'actionTime': unixTime})
        return unixTime

    def field(self, userToken):
        """
        Collect item from current position.

        :param userToken: string
        :return: int, itemID of fetched item
        :exception: TokenException
        """

        username = self.getNameByToken(userToken)

        mRecord = self.getRecordByName(username)

        if mRecord.get('actionTime') > helpers.getCurrentTime():
            raise sisterexceptions.MoveException('you are still moving')

        x = mRecord.get('x')
        y = mRecord.get('y')
        nameItem = self.gameMap.get('map')[x][y]
        index = self.mappingNameItemToIndex(nameItem)
        mRecord['inventory'][index] += 1

        self.updateField(username, mRecord)



    """
    Get all trade for a user token.
    Possible Exceptions: TokenException
    """

    def tradebox(self, token):
        username = self.getNameByToken(token)

        return self.getOffersByName(username)

    """
    Put an offer.
    Possible Exceptions: TokenException, OfferException
    """

    def putOffer(self, token, offeredItem, n1, demandedItem, n2):
        username = self.getNameByToken(token)

        mRecord = self.getRecordByName(username)
        numItem = mRecord['inventory'][offeredItem]

        if numItem < n1:
            raise sisterexceptions.OfferException('insufficient number of offered item')

        # userOffers = self.registeredUser[username].get('offers')
        # if not userOffers:
        # userOffers = {}

        # generate offer
        unixTime = helpers.getCurrentTime()
        lOfferToken = [token, str(unixTime)]
        lOfferToken += [self.salt, str(random.randint(-2147483648, 2147483647))]
        lOfferToken += [chr(ord('A') + offeredItem), str(n1)]
        lOfferToken += [chr(ord('A') + demandedItem), str(n2)]
        offerToken = hashlib.md5(''.join(lOfferToken)).hexdigest()

        self.addOffer(username, offerToken, offeredItem, n1, demandedItem, n2, True)
        # userOffers[offerToken] = [offeredItem, n1, demandedItem, n2, True]
        # allOffers[offerToken] = username



    def sendFind(self, userToken, item):
        """
        Find an item from all servers.

        :param userToken: string
        :param item: int
        :return: list of (offeredItem, n1, demandedItem, n2, availability, offerToken)
        :exception: IndexItemException, TokenException, MixtureException.
        """
        self.validateIndexItem(item)
        username = self.getNameByToken(userToken)

        # get local server offers
        res = [tuple(val[:-1]) + (key,) for key, val in self.getAllOffers().items()
               if val[0] == item and val[-1] != username]

        # get foreign servers offers
        res += self.foreignOffers.findOffers(item)

        return res

    def findOffer(self, item):
        """
        Find an item on local server.
        This is only called from servers.
        throwable: IndexItemException
        :return: tuple of (offeredItem, n1, demandedItem, n2, availability)
        """
        self.validateIndexItem(item)

        # ASSUME only return available offers
        return tuple(tuple(val[:-1]) + (key,) for key, val
                     in self.getOffersByName() if val[0] == item and val[4])

    def sendAccept(self, userToken, offerToken):
        """
        Accept an offer, can be from other servers.

        :param userToken: string
        :param offerToken: string
        :return: None
        """

        username = self.getNameByToken(userToken)

        # find on local machine
        offer = self.getOfferByToken(offerToken)

        # get user inventory
        inventory = self.getRecordByName(username).get('inventory')

        if offer:
            # on local server
            if username == offer[-1]:
                raise sisterexceptions.OfferException('you cannot accept item you offer')

            if (inventory[offer[2]] < offer[3]):
                raise sisterexceptions.OfferException("you don't have enough item %s" %
                                                      self.mappingIndexItemToName(offer[2]))

            self.accept(offerToken)

        else:
            # on foreign server
            # TODO: modify foreign record
            offerDetails = self.foreignOffers.accept(offerToken, inventory)

        # change user inventory
        inventory[offerDetails[0]] += offerDetails[1]
        inventory[offerDetails[2]] -= offerDetails[3]
        self.updateRecord(username, {'inventory': inventory})

    def accept(self, offerToken):
        """
        Accept a local offer.
        """

        offer = self.getOfferByToken(offerToken)
        offer[4] = False
        self.updateOfferToken(offerToken, offer)

    def fetchItem(self, token, offer_token):
        """
        Fetch the item from our accepted offer.
        Our offer must be on local server.
        """
        username = self.getNameByToken(token)
        userOffer = self.getOfferByToken(offer_token)

        if username != userOffer[-1]:
            raise sisterexceptions.OfferException("it wasn't your offer")

        if userOffer[4]:
            raise sisterexceptions.OfferException("you cannot fetch item that hasn't been accepted")

        # add to inventory
        record = self.getRecordByName(username)
        record['inventory'][userOffer[2]] += userOffer[3]

        # delete the offer to prevent user taking the offer item multiple times
        self.deleteOfferByToken(offer_token)

    def cancelOffer(self, token, offerToken):
        """
        Cancel an offer.
        All the offered item returned to inventory.
        """

        username = self.getNameByToken(token)
        offer = self.getOfferByToken(offerToken)

        if username != offer[-1]:
            raise sisterexceptions.OfferException("you can't cancel an offer that isn't yours")

        if not offer[4]:
            raise sisterexceptions.OfferException("you can't cancel an offer that is no longer available")

        # remove offer
        self.deleteOfferByToken(offerToken)

    def mappingIndexItemToName(self, index):
        """
        Return the itemCode from itemID
        :param index: int
        :return: string, itemCode
        """

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
        """
        Return the itemID from the itemCode
        :param name: string
        :return: int
        """
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

    def validateIndexItem(self, index):
        """
        Validate the itemID.
        :param index: int
        :return: None
        :exception: IndexItemExcetpion
        """
        if index < 0 or index > 9:
            raise sisterexceptions.IndexItemException('invalid item')

    def loadMap(self, filename):
        """
        Load map from JSON file on current directory.
        :param filename: string
        :return: None
        """

        mapFile = open(filename, 'r+')
        mapText = mapFile.read()
        mapFile.close()

        self.gameMap = json.loads(mapText)


    def isUsernameRegistered(self, username):
        """
        Check whether username is registered within the system.
        :param username: string
        :return: boolean
        """

        c = self.conn.cursor()
        res = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return res != None

    def registerUserWithPassword(self, username, password):
        """
        Register a user.
        Password is hashed using md5.
        :param username: string
        :param password: string
        :return: None
        """

        record = {'password': hashlib.md5(password).hexdigest()}

        # save to database
        c = self.conn.cursor()
        c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, hashlib.md5(password).hexdigest()))
        self.conn.commit()

    def getRecordByName(self, username):
        """
        Get record of user.

        :param username: string
        :return: {'x': int, 'y': int, 'password': string, 'inventory': <inventory list>, 'actionTime': int}
        :exception: UsernameException
        """

        c = self.conn.cursor()
        res = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if res == None:
            return sisterexceptions.UsernameException('username not found in database')

        record = {}
        record['x'] = res[12]
        record['y'] = res[13]
        record['password'] = res[1]
        record['inventory'] = [res[i] for i in range(2, 12)]
        record['actionTime'] = res[14]
        return record

    def setLogin(self, token, username):
        """
        Login the user.

        :param token: string
        :param username: string
        :return: None
        """

        self.loggedUser[token] = username

    def updateRecord(self, username, updated):
        """
        Update the record of a user.
        """
        self.registeredUser.update(updated)

        # c.execute("UPDATE users SET " + mappingIndexItemToName[item1] + " = " + numItem1 + ", " + mappingIndexItemToName[item2] + " = " + numItem2 + ", " + mappingIndexItemToName[itemRes] + " = " + numItemRes + " WHERE username = " + username)
        # conn.commit()
        #self.synchronizeInventories()



    def getNameByToken(self, token):
        """
        Get the username of a userToken.
        """
        # print result
        result = self.loggedUser.get(token)
        if result:
            return result
        else:
            raise sisterexceptions.TokenException('invalid token')


    def addOffer(self, username, offerToken, offeredItem, n1, demandedItem, n2, availability):
        """
        Add an offer to the system.
        """
        self.allOffers[offerToken] = [offeredItem, n1, demandedItem, n2, availability, username]
        c = self.conn.cursor()

        res = self.getRecordByName(username)
        numCurrOfferedItem = res['inventory'][offeredItem]
        numOfferedItemNow = numCurrOfferedItem - n1
        name = self.mappingIndexItemToName(offeredItem)
        
        # c.execute("UPDATE users SET ? = ? WHERE username = ?", (name, numOfferedItemNow, username)) #ga jalan
        #jangan diubah kode dibawah #willy
        c.execute("UPDATE users SET "+name+" = ? WHERE username = ?", (numOfferedItemNow, username))
        c.execute("INSERT INTO offers (offer_token, username, offered_item, num_offered_item, demanded_item, num_demanded_item, availability) VALUES (?,?,?,?,?,?,?)", (offerToken, username, offeredItem, n1, demandedItem, n2, availability))
        self.conn.commit()

    def getOfferByToken(self, offerToken):
        """
        Get local offer by offerToken.
        :param offerToken: string
        :return: (offeredItem, n1, demandedItem, n2, availability, offerToken)
        """
        res = self.allOffers.get(offerToken)
        if res:
            return res
        else:
            raise sisterexceptions.TokenException('invalid offerToken')


    def updateOfferToken(self, offerToken, updates):
        """
        Update the offer with offerToken.
        :param offerToken: string
        :param updates: map
        :return: None
        """

        self.allOffers[offerToken].update(updates)

    def deleteOfferByToken(self, offerToken):
        """
        Delete the offer with offerToken from local server.
        :param offerToken: string
        :return:
        """
        self.allOffers.pop(offerToken)


    def getOffersByName(self, username):
        """
        Get local offers for a username.
        :return: tuple of (offeredItem, n1, demandedItem, n2, availability, offerToken)
        """
        c = self.conn.cursor()
        res = c.execute("SELECT * FROM offers WHERE username = ?", (username,))
        
        return tuple([row[2], row[3], row[4], row[5], True if row[6] == 1 else False, row[0]] for row in res)
        # return [row[2], row[3], row[4], row[5], True if row[6] == 1 else False, row[0]]
        
        # return tuple(tuple(val[:-1]) + (key,) for key, val in self.allOffers.items() if val[-1] == username)


    def getAllOffers(self):
        """
        Get all local offers.
        :return: tuple of (offeredItem, n1, demandedItem, n2, availability, offerToken)
        """
        return tuple(tuple(val[:-1]) + (key,) for key, val in self.allOffers.items())

