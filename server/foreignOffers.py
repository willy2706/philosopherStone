import threading

import sisterexceptions
import helpers


class OffersFinder():
    '''
    Class to find offers from list of addresses.
    Attributes:
    -> offers: map addressItem (ip:string, port:int, item:int) @ map
        -> lastUpdate: timestamp
        -> offers: map offerToken @ [offeredItem, n1, demandedItem, n2, availability]
    -> addresses: list/tuple of address (ip:string, port:int)
    -> item: int
    -> timeout: float: timeout in seconds
    '''

    def __init__(self, addresses, item, timeout=3):
        '''
        Initiate this class.
        @addresses list/tuple of address (ip:string, port:int)
        @timout float: timeout in seconds
        '''
        self.offers = {}
        self.deadServers = []
        self.addresses = addresses
        self.item = item
        self.timeout = timeout

    def find(self):
        """
        Start finding by making threads.
        @returns map addressItem (ip:string, port:int, item:int) @ map
            -> lastUpdate: timestamp
            -> offers: map offerToken @ [offeredItem, n1, demandedItem, n2, availability]
            , list of address (ip, port)
        """

        # create many TCP sockets to addresses and run each with it's own thread
        running = []
        for address in self.addresses:
            t = threading.Thread(target=self.sendFindOfferWithExceptionHandling,
                                 args=(address, self.item, self.timeout))
            running.append(t)
            t.start()

        for t in running:
            t.join()

        return self.offers, self.deadServers

    def sendFindOfferWithExceptionHandling(self, address, item, timeout):
        '''
        This method is just the same as sendFindOffer, except this method includes exception handling
        '''
        try:
            self.sendFindOffer(address, item, timeout)

        except Exception as e:
            self.deadServers.append(address)
            print 'Address %s:%d is dead' % address
            print 'Cause:', e

    def sendFindOffer(self, address, item, timeout):
        '''
        The method to be called for each thread.
        Finds the offer with itemId(item) of an address.
        @address (ip: string, port: int)
        @item: int
        @timeout float: timeout in seconds
        '''

        # structure data
        toSend = {'method': 'findoffer',
                  'item': item}

        # setup connection
        mJSON = helpers.sendJSON(address, toSend, timeout)

        offers = mJSON['offers']

        # convert back to our offer representation and update offers
        ref = self.offers[(address) + (item,)] = {}

        ref['lastUpdate'] = helpers.getCurrentTime()
        ref0 = ref['offers'] = {}
        for offer in offers:
            ref0[offer[-1]] = offer[:-1]


class ServerDealer():
    '''
    Class that deals with other servers.
    -> foreignOffers: map addressItem (ip:string, port:int, item:int) @ map
        -> lastUpdate: timestamp
        -> offers: map offerToken @ (offeredItem, n1, demandedItem, n2, availability)
    -> servers: list of map
        -> ip: string
        -> port: int
    '''

    def __init__(self, myAddress, cacheTimeout=300):
        '''
        Initiate attributes.
        :param cacheTimeout: int, number of seconds until the local cache times out
        '''
        self.foreignOffers = {}
        self.servers = []
        self.myAddress = myAddress
        self.cacheTimeout = cacheTimeout


    def setServers(self, servers):
        '''
        Set the list of foreign servers.
        @servers list of map
            ->ip: string
            ->port: int
        '''
        self.servers = servers

    def accept(self, offerToken, inventory, timeout=3.0):
        '''
        Send accept to other server.

        :param offerToken: string
        :return: None
        '''

        found = False
        deadServer = False
        theServer = None

        # search for offers with offerToken
        for key, record in self.foreignOffers.items():
            offers = record['offers']
            if offerToken in offers:
                # check whether inventory have enough stuff
                offer = offers[offerToken]

                if inventory[offer[2]] < offer[3]:
                    # the number of item in inventory is not enough.
                    raise sisterexceptions.OfferException("you don't have enough item %s" %
                                                          helpers.mappingIndexItemToName(offer[2]))

                # send accept to other server
                toSend = {'method': 'accept',
                          'offer_token': offerToken}

                try:
                    mJSON = helpers.sendJSON(key[:2], toSend, timeout)

                except:
                    # server is dead
                    deadServer = True
                    theServer = key[:2]
                    break

                status = mJSON['status']

                res = offers.pop(offerToken)

                if status == 'fail':
                    raise sisterexceptions.OfferException('offer no longer available')
                elif status == 'error':
                    raise sisterexceptions.OfferException(mJSON['description'])

                found = True
                break

        if deadServer:
            self.removeServer(theServer)
            raise sisterexceptions.OfferException('offer server is dead')

        if not found:
            raise sisterexceptions.OfferException('offer not found')

        return res


    def findOffers(self, item):
        """
        Find Offers from foreign servers.
        :return: list of (offerid, n1, demandid, n2, availability, offerToken)
        """

        # list of servers need to be searched for offers
        toSend = []

        # result variable to return
        res = []

        for address in self.servers:
            addressItem = (address.get('ip'), address.get('port'), item)

            if addressItem[:2] == self.myAddress:
                continue

            record = self.foreignOffers.get(addressItem)
            hit = False

            if record:
                # hit, check validity with timestamp
                unixTime = helpers.getCurrentTime()

                if unixTime < record.get('lastUpdate') + self.cacheTimeout:
                    # hit!
                    res += [tuple(val) + (key,) for key, val in record.get('offers').items()]
                    hit = True

            if not hit:
                # not hit, delete record and find on that server
                if record:
                    self.foreignOffers.pop(addressItem)
                toSend.append(addressItem[:2])

        oFinder = OffersFinder(toSend, item, 3)
        uncached, deadServers = oFinder.find()
        self.foreignOffers.update(uncached)
        for server in deadServers:
            self.removeServer(server)

        for key1, val1 in uncached.items():
            res += [tuple(val0) + (key0,) for key0, val0 in val1.get('offers').items()]

        return res

    def removeServer(self, address):
        """
        Remove a server from the cache, all the offers are removed too.

        :param address: (ip, port)
        :return: None
        """
        # remove server
        print 'remove server', address
        self.servers.remove({'ip': address[0], 'port': address[1]})

        # remove all offer with that server
        toPop = []
        for key, val in self.foreignOffers.items():
            if key[:2] == address:
                toPop.append(key)

        for key in toPop:
            self.foreignOffers.pop(key)