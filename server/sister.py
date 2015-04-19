import md5
import time
import calendar

'''
The Exception raised when the server is having problem with usernames.
'''
class UsernameException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

'''
The Logic of Server.
Instance objects:
-> registeredUser
-> loggedUser
'''
class SisterServerLogic():
    def __init__(self):
        self.registeredUser = {}
        self.loggedUser = {}

    def register(name, password):
        if name in self.registeredUser:
            raise UsernameException('username exists')
        
        self.registeredUser[name] = password

    '''
    Login a user. Return (token, x, y, time) on success.
    Possible Exceptions:
    -> UsernameException
    '''
    def login(name, password):
        mPassword = self.registeredUser.get(name)
        if mPassword:
            if mPassword != password:
                raise UsernameException('username/password combination is not found')

            unixTime = calendar.timegm(time.gmtime())
            token = md5.new(name+password+str(unixTime))
            return (token, 0, 0, unixTime)
            
        else:
            raise UsernameException('username/password combination is not found')    
