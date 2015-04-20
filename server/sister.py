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
The Logic of Server.
Instance objects:
-> registeredUser: map of username @ map
   -> password: string
   -> offers: map of offerToken @ tuple
       0> int: oferred item id
       1> int: number of offered item
       2> int: demanded item id
       3> int: number of demanded item
       4> boolean: availability, false means already sold
-> loggedUser: map of token @ username
-> gameMap
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

    def signup(self, name, password):
        c.execute("INSERT INTO users(username, password) VALUES ("+"'"+name+"', '"+ password + "'" +")") #belum testing
        print 'sign up'
        print res
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
            token = md5.new(name+password+str(unixTime)).hexdigest()

            self.loggedUser[token] = name
            self.registeredUser[name]['loggedOn'] = True
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
    Get all trade for a user token
    '''
    def tradebox(self, token):
        username = self.loggedUser.get(token)

        if username:
            return tuple(val + (key,) for key, val in
                  self.registeredUser[username].get('offers', {}))
        
        else: # token not found
            raise TokenException('invalid token')

    def getInventory(self, token): #belum testing
        username = self.loggedUser.get(token)
        if username:
            res = c.execute('SELECT * FROM inventories')
            return res
        else:
            raise TokenException('invalid token')
