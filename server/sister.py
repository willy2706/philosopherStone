import hashlib
import json
import sqlite3
import random
import os
import threading

import helpers
import foreignOffers
import sisterexceptions


DATABASE_FILE = 'sister.db'

threadLocal = threading.local()


class SisterServerLogic():
    """
    The Logic of Server.
    Instance objects:
    -> loggedUser: map of token:string @ username:string
    -> gameMap: {'name':string, 'width':int, 'height':int, 'map': matrix}
    -> salt: string appended to be hashed
    -> sendFindLock: Lock
    -> foreignOffers: foreignOffers.ServerDealer
    -> myAddress: (ip: string, port: int)
    """

    def __init__(self, myAddress=None, trackerAddress=None):
        """
        Initialize the serverLogic.

        :return: None
        """

        if not os.path.isfile(DATABASE_FILE):
            # File not found, create a new database

            conn = sqlite3.connect(DATABASE_FILE)
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARCHAR(255) NOT NULL, "
                      "R11 INT UNSIGNED NOT NULL DEFAULT 0, R12 INT UNSIGNED NOT NULL DEFAULT 0, R13 INT UNSIGNED NOT NULL DEFAULT 0, "
                      "R14 INT UNSIGNED NOT NULL DEFAULT 0, R21 INT UNSIGNED NOT NULL DEFAULT 0, R22 INT UNSIGNED NOT NULL DEFAULT 0, "
                      "R23 INT UNSIGNED NOT NULL DEFAULT 0, R31 INT UNSIGNED NOT NULL DEFAULT 0, R32 INT UNSIGNED NOT NULL DEFAULT 0, "
                      "R41 INT UNSIGNED NOT NULL DEFAULT 0, X INT NOT NULL DEFAULT 0, Y INT NOT NULL DEFAULT 0, "
                      "action_time INT UNSIGNED NOT NULL DEFAULT 0, last_field INT UNSIGNED, PRIMARY KEY(username))")
            c.execute("CREATE TABLE IF NOT EXISTS offers (offer_token VARCHAR(255), username VARCHAR(255) NOT NULL, "
                      "offered_item INT NOT NULL, num_offered_item INT NOT NULL, demanded_item INT NOT NULL, "
                      "num_demanded_item INT NOT NULL, availability TINYINT NOT NULL, PRIMARY KEY(offer_token), "
                      "FOREIGN KEY (username) REFERENCES users(username))")

            # buat save
            conn.commit()
            conn.close()

        self.loggedUser = {}
        self.loadMap('map.json')
        self.salt = 'mi0IUsW4'
        self.foreignOffers = foreignOffers.ServerDealer(myAddress)
        self.sendFindLock = threading.Lock()
        self.myAddress = myAddress

        if trackerAddress:
            # connect to tracker
            request = {'method': 'join',
                       'ip': myAddress[0],
                       'port': myAddress[1]}
            response = helpers.sendJSON(trackerAddress, request)
            if response['status'] == 'ok':
                self.serverStatus(response['value'])
            else:
                raise sisterexceptions.TrackerException('Tracker Failed')


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

        if name == '' or '{' in name or '}' in name:
            raise sisterexceptions.UsernameException('please use a good username')

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

        if name == '' or '{' in name or '}' in name:
            raise sisterexceptions.UsernameException('please use a good username')

        mRecord = self.getRecordByName(name)

        if mRecord.get('password') != hashlib.md5(password).hexdigest():
            raise sisterexceptions.UsernameException('username/password combination is not found')

        actionTime = mRecord.get('actionTime')
        serverTime = helpers.getCurrentTime()
        token = hashlib.md5(name).hexdigest()

        self.setLogin(token, name)
        return token, mRecord.get('x'), mRecord.get('y'), actionTime, serverTime

    def getInventory(self, userToken):
        """
        Get the inventory of a userToken.
        :param userToken: string
        :return: [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]
        :exception: TokenException
        """

        username = self.getNameByToken(userToken)
        record = self.getRecordByName(username)

        return record['inventory']

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

        if mInventory[item1] < 3:
            raise sisterexceptions.MixtureException('first item is not enough')
        if mInventory[item2] < 3:
            raise sisterexceptions.MixtureException('second item is not enough')

        # get the id of the resulting item
        itemRes = self.processMix(item1, item2)

        # mixing OK, reduce item1, item2, increase itemRes
        numItem1 = mInventory[item1] - 3  # item 1 jumlahnya kurang 3
        numItem2 = mInventory[item2] - 3  # item 2 jumlahnya kurang 3
        numItemRes = mInventory[itemRes] + 1  # item hasil gabung jumlahnya tambah 1

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
            raise sisterexceptions.ActionException('position out of bounds')

        record = self.getRecordByName(username)
        prevX = record.get('x')
        prevY = record.get('y')

        if prevX == x and prevY == y:
            raise sisterexceptions.ActionException('invalid move')

        currTime = helpers.getCurrentTime()
        if record.get('actionTime') > currTime:
            raise sisterexceptions.ActionException('you are still moving')

        # time in seconds
        eachStep = 10
        timeNeeded = (abs(prevX - x) + abs(prevY - y)) * eachStep

        unixTime = currTime + timeNeeded
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
            raise sisterexceptions.ActionException('you are still moving')

        curX = mRecord.get('x')
        curY = mRecord.get('y')
        pos = mRecord.get('lastField')
        width = self.gameMap.get('width')
        if pos:
            x = pos % width
            y = pos / width
            if x == curX and y == curY:
                raise sisterexceptions.ActionException('you already took that item')

        nameItem = self.gameMap.get('map')[curX][curY]
        index = helpers.mappingNameItemToIndex(nameItem)
        inventory = mRecord.get('inventory')
        inventory[index] += 1

        self.updateRecord(username, {'inventory': inventory, 'lastField': curY * width + curX})
        return index


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

        # jadi di dalam add offer, otomatis uda dikurangi demanded item nya
        self.addOffer(username, offerToken, offeredItem, n1, demandedItem, n2, True)


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
        res = [offer[:6] for offer in self.getAllOffers()
               if offer[0] == item and offer[-1] != username]

        # get foreign servers offers
        try:
            self.sendFindLock.acquire()
            res += self.foreignOffers.findOffers(item)

        finally:
            self.sendFindLock.release()

        return res


    def findOffer(self, item):
        """
        Find an item on local server.
        This is only called from servers.
        throwable: IndexItemException
        :return: tuple of (offeredItem, n1, demandedItem, n2, availability, offerToken)
        """
        self.validateIndexItem(item)

        # only return available offers
        return tuple(row[:6] for row in self.getAllOffers() if row[0] == item and row[4])

    def sendAccept(self, userToken, offerToken):
        """
        Accept an offer, can be from other servers.

        :param userToken: string
        :param offerToken: string
        :return: None
        """

        username = self.getNameByToken(userToken)

        # find on local machine
        try:
            offer = self.getOfferByToken(offerToken)

        except sisterexceptions.OfferException as e:
            # for this case its okay, it might be an offer from other server
            offer = None

        # get user inventory
        inventory = self.getRecordByName(username).get('inventory')

        if offer:
            # on local server
            if username == offer[-1]:
                raise sisterexceptions.OfferException('you cannot accept item you offer')

            if (inventory[offer[2]] < offer[3]):
                raise sisterexceptions.OfferException("you don't have enough item %s" %
                                                      helpers.mappingIndexItemToName(offer[2]))

            offerDetails = offer[:5]
            self.accept(offerToken)

        else:
            # on foreign server
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

        if not offer[4]:
            raise sisterexceptions.OfferException('the offer has been taken')
        else:
            self.setOfferNotAvailable(offerToken)


    def fetchItem(self, token, offerToken):
        """
        Fetch the item from our accepted offer.
        Our offer must be on local server.
        """

        username = self.getNameByToken(token)
        userOffer = self.getOfferByToken(offerToken)
        # print userOffer
        if username != userOffer[5]:
            raise sisterexceptions.OfferException("it wasn't your offer")

        if userOffer[4]:
            raise sisterexceptions.OfferException("you cannot fetch item that hasn't been accepted")

        # add to inventory
        record = self.getRecordByName(username)
        inventory = record.get('inventory')
        inventory[userOffer[2]] += userOffer[3]
        self.updateRecord(username, {'inventory': inventory})

        # delete the offer to prevent user taking the offer item multiple times
        self.deleteOfferByToken(offerToken)

    def cancelOffer(self, token, offerToken):
        """
        Cancel an offer.
        All the offered item returned to inventory.
        """

        username = self.getNameByToken(token)
        offer = self.getOfferByToken(offerToken)

        if username != offer[5]:
            raise sisterexceptions.OfferException("you can't cancel an offer that isn't yours")

        if not offer[4]:
            raise sisterexceptions.OfferException("you can't cancel an offer that is no longer available")

        # remove offer
        record = self.getRecordByName(username)
        inventory = record.get('inventory')
        inventory[offer[0]] += offer[1]
        self.updateRecord(username, {'inventory': inventory})
        self.deleteOfferByToken(offerToken)


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

        conn = self.getConnection()
        c = conn.cursor()
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
        conn = self.getConnection()
        c = conn.cursor()
        c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, hashlib.md5(password).hexdigest()))
        conn.commit()

    def getRecordByName(self, username):
        """
        Get record of user.

        :param username: string
        :return: {'x': int, 'y': int, 'password': string, 'inventory': <inventory list>, 'actionTime': int}
        :exception: UsernameException
        """

        conn = self.getConnection()
        c = conn.cursor()
        res = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if res == None:
            raise sisterexceptions.UsernameException('username not found in database')

        record = {}
        record['x'] = res[12]
        record['y'] = res[13]
        record['password'] = res[1]
        record['inventory'] = [res[i] for i in range(2, 12)]
        record['actionTime'] = res[14]
        record['lastField'] = res[15]
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

        # build the query depending on the updated map
        query = ''
        args = []
        for key, val in updated.items():
            if key == 'x':
                query += 'X = ?, '
                args.append(val)

            elif key == 'y':
                query += 'Y = ?, '
                args.append(val)

            elif key == 'actionTime':
                query += 'action_time = ?, '
                args.append(val)

            elif key == 'lastField':
                query += 'last_field = ?, '
                args.append(val)

            elif key == 'inventory':
                idx = 0
                for item in val:
                    query += '%s = ?, ' % helpers.mappingIndexItemToName(idx)
                    args.append(item)
                    idx += 1

        if len(query) == 0:
            # no need to do anything
            return

        query = 'UPDATE users SET ' + query[:-2] + ' WHERE username = ?'
        # print 'updateQuery:', query
        args.append(username)

        # insert into the database
        conn = self.getConnection()
        c = conn.cursor()
        c.execute(query, tuple(args))
        conn.commit()


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
        res = self.getRecordByName(username)
        numCurrOfferedItem = res.get('inventory')[offeredItem]
        numOfferedItemNow = numCurrOfferedItem - n1
        name = helpers.mappingIndexItemToName(offeredItem)

        conn = self.getConnection()
        c = conn.cursor()
        c.execute("UPDATE users SET " + name + " = ? WHERE username = ?", (numOfferedItemNow, username))
        c.execute(
            "INSERT INTO offers (offer_token, username, offered_item, num_offered_item, demanded_item, num_demanded_item, availability) VALUES (?,?,?,?,?,?,?)",
            (offerToken, username, offeredItem, n1, demandedItem, n2, availability))
        conn.commit()

    def getOfferByToken(self, offerToken):
        """
        Get local offer by offerToken.

        :param offerToken: string
        :return: (offeredItem, n1, demandedItem, n2, availability, offerToken)
        """
        conn = self.getConnection()
        c = conn.cursor()
        res = c.execute("SELECT * FROM offers WHERE offer_token = ?", (offerToken,)).fetchone()

        if res == None:
            raise sisterexceptions.OfferException('offer not found in database. token mismatch?')

        return (res[2], res[3], res[4], res[5], res[6], res[1])

    def setOfferNotAvailable(self, offerToken):
        """
        Set the availability to false.

        :param offerToken: string
        :return: None
        """

        conn = self.getConnection()
        c = conn.cursor()
        c.execute("UPDATE offers SET availability = '0' WHERE offer_token = ?", (offerToken,))
        conn.commit()

    def deleteOfferByToken(self, offerToken):
        """
        Delete the offer with offerToken from local server.
        :param offerToken: string
        :return:
        """

        conn = self.getConnection()
        c = conn.cursor()
        c.execute("DELETE FROM offers WHERE offer_token = ?", (offerToken,))
        conn.commit()


    def getOffersByName(self, username):
        """
        Get local offers for a username.
        :return: tuple of (offeredItem, n1, demandedItem, n2, availability, offerToken)
        """

        conn = self.getConnection()
        c = conn.cursor()
        res = c.execute("SELECT * FROM offers WHERE username = ?", (username,))

        return tuple((row[2], row[3], row[4], row[5], row[6] == 1, row[0]) for row in res)

    def getAllOffers(self):
        """
        Get all local offers.

        :return: tuple of (offeredItem, n1, demandedItem, n2, availability, offerToken, username)
        """

        conn = self.getConnection()
        c = conn.cursor()
        res = c.execute("SELECT * FROM offers")

        return tuple((row[2], row[3], row[4], row[5], row[6] == 1, row[0], row[1]) for row in res)

    def getConnection(self):
        """
        Return a local sqlite3 connection.

        :return: sqlite3 connection
        """

        conn = getattr(threadLocal, 'conn', None)
        if conn is None:
            conn = sqlite3.connect(DATABASE_FILE)
            threadLocal.conn = conn

        return conn

    def closeConnection(self):
        """
        Close the sqlite3 connection.

        :return: None
        """

        conn = getattr(threadLocal, 'conn', None)
        if conn:
            conn.close()