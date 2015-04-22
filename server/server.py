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

        #debug
        print 'Request:', everything
        mJSON = json.loads(everything)

        # process the request
        toSend = {}
        method = mJSON['method']

        if method == 'serverStatus':
            try:
                serverLogic.serverStatus(mJSON['server'])
                toSend['status'] = 'ok'

            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'signup':
            # process signup
            try:
                serverLogic.signup(mJSON['username'], mJSON['password'])
                toSend['status'] = 'ok'
                
            except sister.UsernameException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)
                
            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)
            
        elif method == 'login':
            # process login
            try:
                token, x, y, time = serverLogic.login(mJSON['username'], mJSON['password'])
                toSend['status'] = 'ok'
                toSend['token'] = token
                toSend['x'] = x
                toSend['y'] = y
                toSend['time'] = time

            except sister.UsernameException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)
                
            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'inventory':
            try:
                res = serverLogic.getInventory(mJSON['token'])
                toSend['status'] = 'ok'
                toSend['inventory'] = res

            except sister.TokenException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)

            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'mixitem':
            try:
                res = serverLogic.mixItem(mJSON['token'], mJSON['item1'], mJSON['item2'])
                toSend['status'] = 'ok'
                toSend['item'] = res

            except (sister.TokenException, sister.MixtureException, sister.IndexItemException) as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)

            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'map':
            # process map request
            try:
                name, width, height = serverLogic.getMap(mJSON['token'])
                toSend['status'] = 'ok'
                toSend['name'] = name
                toSend['width'] = width
                toSend['height'] = height

            except sister.TokenException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)
            
            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'move':
            try:
                time = serverLogic.move(mJSON['token'], mJSON['x'], mJSON['y'])
                toSend['status'] = 'ok'
                toSend['time'] = time

            except sister.TokenException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)

            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'field':
            try:
                item = serverLogic.field(mJSON['token'])
                toSend['status'] = 'ok'
                toSend['item'] = item

            except sister.TokenException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)

            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'offer':
            # process offer
            try:
                serverLogic.putOffer(mJSON['token'], mJSON['offered_item'], mJSON['n1'],
                                     mJSON['demanded_item'], mJSON['n2'])
                toSend['status'] = 'ok'

            except (sister.OfferException, sister.TokenException) as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)

            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'tradebox':
            # process tradebox request
            try:
                offers = serverLogic.tradebox(mJSON['token'])
                toSend['status'] = 'ok'
                toSend['offers'] = offers

            except sister.TokenException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)

            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'sendfind':
            try:
                res = serverLogic.sendFind(mJSON['token'], mJSON['item'])
                toSend['status'] = 'ok'
                toSend['offers'] = res

            except (sister.TokenException, sister.IndexItemException) as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)

            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)

        elif method == 'accept':
            # process accept
            try:
                serverLogic.accept(mJSON['offer_token'])

            except sister.OfferException as e:
                toSend['status'] = 'fail'
                toSend['description'] = str(e)

            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = str(e)



        elif method == 'fetchitem':
            try:
                serverLogic.fetchItem(mJSON['token'], mJSON['offer_token'])
                toSend['status'] = 'ok'
            except (sister.TokenException, sister.LogicException) as e:
                toSend['status'] = 'fail'
                toSend['description'] = e
            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = e

        elif method == 'canceloffer':
            try:
                serverLogic.cancelOffer(mJSON['token'], mJSON['offer_token'])
                toSend['status'] = 'ok'
            except (sister.TokenException, sister.LogicException) as e:
                toSend['status'] = 'fail'
                toSend['description'] = e
            except Exception as e:
                toSend['status'] = 'error'
                toSend['description'] = e



        # send response to client
        sToSend = json.dumps(toSend)

        self.request.sendall(sToSend)
        # debug mode
        print 'Response:', sToSend
        

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
