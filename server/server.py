import SocketServer
import sys
import threading
import json

import sister
import helpers
import sisterexceptions


class ThreadedSisterRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        """
        Main handle method.
        """

        # receive JSON from other machine (tracker/client)
        everything = ''

        while True:
            self.request.settimeout(3)
            data = self.request.recv(4096)
            everything += data
            if helpers.containsValidJSON(everything):
                break

        # debug
        # print 'Request from %s:%d :' % self.request.getpeername()
        # print everything
        mJSON = json.loads(everything)

        # process the request
        toSend = {}
        method = mJSON['method']

        try:
            if method == 'serverStatus':
                serverLogic.serverStatus(mJSON['server'])
            elif method == 'signup':
                serverLogic.signup(mJSON['username'], mJSON['password'])
            elif method == 'login':
                token, x, y, actionTime, serverTime = serverLogic.login(mJSON['username'], mJSON['password'])
                toSend['token'] = token
                toSend['x'] = x
                toSend['y'] = y
                toSend['time'] = actionTime
                toSend['serverTime'] = serverTime

            elif method == 'inventory':
                res = serverLogic.getInventory(mJSON['token'])
                toSend['inventory'] = res

            elif method == 'mixitem':
                res = serverLogic.mixItem(mJSON['token'], mJSON['item1'], mJSON['item2'])
                toSend['item'] = res

            elif method == 'map':
                name, width, height = serverLogic.getMap(mJSON['token'])
                toSend['name'] = name
                toSend['width'] = width
                toSend['height'] = height

            elif method == 'move':
                actionTime = serverLogic.move(mJSON['token'], mJSON['x'], mJSON['y'])
                toSend['time'] = actionTime

            elif method == 'field':
                item = serverLogic.field(mJSON['token'])
                toSend['item'] = item

            elif method == 'offer':
                serverLogic.putOffer(mJSON['token'], mJSON['offered_item'], mJSON['n1'],
                                     mJSON['demanded_item'], mJSON['n2'])

            elif method == 'tradebox':
                offers = serverLogic.tradebox(mJSON['token'])
                toSend['offers'] = offers

            elif method == 'sendfind':
                res = serverLogic.sendFind(mJSON['token'], mJSON['item'])
                toSend['offers'] = res

            elif method == 'findoffer':
                offers = serverLogic.findOffer(mJSON['item'])
                toSend['offers'] = offers

            elif method == 'sendaccept':
                serverLogic.sendAccept(mJSON['token'], mJSON['offer_token'])
            elif method == 'accept':
                serverLogic.accept(mJSON['offer_token'])
            elif method == 'fetchitem':
                serverLogic.fetchItem(mJSON['token'], mJSON['offer_token'])
            elif method == 'canceloffer':
                serverLogic.cancelOffer(mJSON['token'], mJSON['offer_token'])

            toSend['status'] = 'ok'

        except (sisterexceptions.OfferException, sisterexceptions.IndexItemException, sisterexceptions.MixtureException,
                sisterexceptions.TokenException, sisterexceptions.UsernameException,
                sisterexceptions.ActionException) as e:
            # any custom exceptions is a failure
            toSend['status'] = 'fail'
            toSend['description'] = str(e)

        # except Exception as e:
        # toSend['status'] = 'error'
        #     toSend['description'] = str(e)

        serverLogic.closeConnection()

        # send response to client
        sToSend = json.dumps(toSend)

        # debug mode
        # print 'Response to %s:%d :' % self.request.getpeername()
        # print sToSend
        self.request.sendall(sToSend)


if __name__ == '__main__':
    if len(sys.argv) > 4:
        # tracker mode
        myIP = sys.argv[1]
        port = int(sys.argv[2])
        trackerAddress = (sys.argv[3], int(sys.argv[4]))
        serverLogic = sister.SisterServerLogic((myIP, port), trackerAddress)

    elif len(sys.argv) == 2:
        # local mode
        port = int(sys.argv[1])
        serverLogic = sister.SisterServerLogic()

    elif len(sys.argv) == 1:
        # local mode with auto port
        port = 0
        serverLogic = sister.SisterServerLogic()

    else:
        print 'Usage: python %s <serverPort>' % sys.argv[0]
        print '  -or- python %s' % sys.argv[0]
        print '  -or- python %s <serverIP> <serverPort> <trackerIP> <trackerPort>' % sys.argv[0]
        sys.exit()

    address = ('', port)
    server = SocketServer.ThreadingTCPServer(address, ThreadedSisterRequestHandler)
    # find out what port we were given
    ip, port = server.server_address

    t = threading.Thread(target=server.serve_forever)
    t.start()

    print 'Server up on %s:%s' % (ip, port)

    t.join()
    print 'Server down'
