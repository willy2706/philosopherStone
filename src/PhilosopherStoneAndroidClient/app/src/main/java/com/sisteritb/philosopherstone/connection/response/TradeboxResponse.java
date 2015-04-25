package com.sisteritb.philosopherstone.connection.response;


import com.sisteritb.philosopherstone.entity.TradeOffer;

import org.json.simple.JSONArray;
import org.json.simple.parser.ParseException;

public class TradeboxResponse extends Response{
    private final TradeOffer[] offers;

    public TradeboxResponse(String jsonString) throws ParseException, ResponseFailException, ResponseErrorException {
        super(jsonString);
        
        JSONArray jsonOffers = (JSONArray) responseJson.get("offers");
        int offersSize = jsonOffers.size();
        offers = new TradeOffer[offersSize];
        for(int i=0; i<offersSize; i++){
            JSONArray jsonOffer = (JSONArray) jsonOffers.get(i);
            long offeredItem = (long) jsonOffer.get(0);
            long offeredAmmount = (long) jsonOffer.get(1);
            long demandedItem = (long) jsonOffer.get(2);
            long demandedAmmout = (long) jsonOffer.get(3);
            boolean availability = (boolean) jsonOffer.get(4);
            String offerToken = (String) jsonOffer.get(5);
            TradeOffer offer = new TradeOffer(offerToken, offeredItem, 
                    offeredAmmount, demandedItem, demandedAmmout,availability);
            offers[i] = offer;
        }
        
    }

    /**
     * @return the offers
     */
    public TradeOffer[] getOffers() {
        return offers;
    }
    
}
