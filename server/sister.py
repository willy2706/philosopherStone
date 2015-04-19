import md5
import time
import calendar
import json

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
    def __init__(self):
        self.registeredUser = {}
        self.loggedUser = {}
        self.loadMap('map.json')

    def signup(self, name, password):
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
