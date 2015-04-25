import json
import socket
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
        self.addresses = addresses
        self.item = item
        self.timeout = timeout

    def find(self):
        """
        Start finding by making threads.
        @returns map addressItem (ip:string, port:int, item:int) @ map
            -> lastUpdate: timestamp
            -> offers: map offerToken @ [offeredItem, n1, demandedItem, n2, availability]
        """

        # create many TCP sockets to addresses and run each with it's own thread
        running = []
        for address in self.addresses:
            t = threading.Thread(target=self.sendFindOfferWithExceptionHandling,
                                 args=(address, self.item, self.timeout))
            running.append(t)

        for t in running:
            t.join()

        return self.offers

    def sendFindOfferWithExceptionHandling(self, address, item, timeout):
        '''
        This method is just the same as sendFindOffer, except this method includes exception handling
        '''
        try:
            self.sendFindOffer(address, item, timeout)

        except Exception as e:
            print e

    def sendFindOffer(self, address, item, timeout):
        '''
        The method to be called for each thread.
        Finds the offer with itemId(item) of an address.
        @address (ip: string, port: int)
        @item: int
        @timeout float: timeout in seconds
        '''

        # structure data
        toSend = {}
        toSend['method'] = 'findoffer'
        toSend['item'] = item

        # setup connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(address)

        # send and receive
        s.sendall(json.dumps(toSend))

        everything = ''
        while True:
            data = s.recv(4096)
            everything += data
            if helpers.containsValidJSON(everything):
                break

        mJSON = json.loads(everything)

        offers = mJSON['offers']

        # convert back to our offer representation
        self.offers[(address) + (item,)] = {}
        ref = self.offers[(address) + (item,)]
        ref['lastUpdate'] = helpers.getCurrentTime()
        ref['offers'] = {}
        ref0 = ref['offers']
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

    def __init__(self, cacheTimeout=30):
        '''
        Initiate attributes.
        :param cacheTimeout: int, number of seconds until the local cache times out
        '''
        self.foreignOffers = {}
        self.cacheTimeout = cacheTimeout
        self.servers = []

    def setServers(self, servers):
        '''
        Set the list of foreign servers.
        @servers list of map
            ->ip: string
            ->port: int
        '''
        self.servers = servers

    def accept(self, offerToken, inventory, timeout=3):
        '''
        Send accept to other server.

        :param offerToken: string
        :return: None
        '''

        # search for offers with offerToken
        for key, record in self.foreignOffers.items():
            offers = record['offers']
            if offerToken in offers:
                # check whether inventory have enough stuff
                offer = offers[offerToken]

                if inventory[offer[2]] < offer[3]:
                    # the number of item in inventory is not enough.
                    raise sisterexceptions.OfferException("you don't have enough item %s" %
                                                          self.mappingIndexItemToName(offer[2]))

                # send accept to other server
                toSend = {'method': 'accept',
                          'offerToken': offerToken}
                
                mJSON = helpers.sendJSON(key[:2], toSend, timeout)

                status = mJSON['status']

                if status == 'fail':
                    offers.pop(offerToken)
                    raise sisterexceptions.OfferException('offer no longer available')
                elif status == 'ok':
                    res = offers.pop(offerToken)
                else:
                    raise Exception(mJSON['description'])

                found = True
                break

        if not found:
            raise sisterexceptions.OfferException('offer not found')

        return res


    def findOffers(self, item):
        """
        Find Offers from foreign servers.
        :return: list of [offerid, n1, demandid, n2, availability, offerToken]
        """

        # list of servers need to be searched for offers
        toSend = []

        # result variable to return
        res = []

        for address in self.servers:
            addressItem = (address.get('ip'), address.get('port'), item)
            record = self.foreignOffers.get(addressItem)
            hit = False

            if record:
                # hit, check validity with timestamp
                unixTime = helpers.getCurrentTime()

                if unixTime < record.get('lastUpdate') + self.cacheTimeout:
                    # hit!
                    res += [tuple(val) + (key,) for key, val in record.get('offers')]
                    hit = True

            if not hit:
                # not hit, delete record and find on that server
                if record:
                    self.foreignOffers.pop(addressItem)
                toSend.append(addressItem[:2])

        oFinder = OffersFinder(toSend, item, 3)
        uncached = oFinder.find()
        self.foreignOffers.update(uncached)

        for uncachedRecord in uncached:
            res += [tuple(val) + (key,) for key, val in uncachedRecord.get('offers')]

        return res