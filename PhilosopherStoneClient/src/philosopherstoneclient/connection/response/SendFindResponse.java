/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package philosopherstoneclient.connection.response;

import org.json.simple.JSONArray;
import org.json.simple.parser.ParseException;
import philosopherstoneclient.entity.TradeOffer;

/**
 *
 * @author winsxx
 */
public class SendFindResponse extends Response{
    private final TradeOffer[] offers;

    public SendFindResponse(String jsonString) throws ParseException, ResponseFailException, ResponseErrorException {
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
