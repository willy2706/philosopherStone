import SocketServer
import threading
import json
import sister

serverLogic = sister.SisterServerLogic()

class ThreadedSisterRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # receive JSON from other machine (tracker/client)
        everything = ''
        
        while True:
            data = self.request.recv(4096)
            everything += data
            if self.containsValidJSON(everything):
                break

        mJSON = json.load(everything)

        # process the request
        toSend = {}
        method = mJSON['method']
        
        if method == 'signup':
            # prcess signup
            try:
                serverLogic.signup(mJSON['username'], mJSON['password'])
                toSend['status'] = 'ok'
                
            except UsernameException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)
                
            except:
                toSend['status'] = 'error'
            
        elif method == 'login':
            # process login
            try:
                token, x, y, time = serverLogic.login(mJSON['username'], mJSON['password'])
                toSend['status'] = 'ok'
                toSend['token'] = token
                toSend['x'] = x
                toSend['y'] = y
                toSend['time'] = time

            except UsernameException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)
                
            except as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        # send response to client
        sToSend = json.dumps(toSend)

        self.request.sendall(sToSend)
        

    '''
    Check wether data contains a valid JSON or not.
    This function can't handle JSON with curly braces elements.
    '''
    def containsValidJSON(self, data):
        balance = 0
        found = False
        
        for c in data:
            if c == '{':
                if not found:
                    found = True
                balance += 1
                
            elif c == '}':
                if found:
                    balance -= 1
                    if balance == 0:
                        return True

        return False
    # End of containsValidJSON

if __name__ == '__main__':
    import sys

    port = 0
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    address = ('', port)
    server = SocketServer.ThreadingTCPServer(address, ThreadedSisterRequestHandler)
    # find out what port we were given
    ip, port = server.server_address

    t = threading.Thread(target=server.serve_forever)
    t.start()

    print 'Server up on %s:%s' % (ip, port)

    t.join()
    print 'Server down'