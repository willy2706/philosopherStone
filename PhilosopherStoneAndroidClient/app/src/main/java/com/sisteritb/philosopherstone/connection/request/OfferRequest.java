/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.sisteritb.philosopherstone.connection.request;

import java.util.LinkedHashMap;
import java.util.Map;
import org.json.simple.JSONValue;

/**
 *
 * @author winsxx
 */
public class OfferRequest extends Request{
    
    public String token;
    public int offeredItem, demandedItem;
    public int offeredItemAmmount, demandedItemAmmunt;

    public OfferRequest() {
        method = "offer";
    }
    
    @Override
    public String toString() {
        Map obj = new LinkedHashMap();
        
        obj.put("method", method);
        obj.put("token", token);
        obj.put("offered_item", offeredItem);
        obj.put("n1", offeredItemAmmount);
        obj.put("demanded_item", demandedItem);
        obj.put("n2", demandedItemAmmunt);
        
        String jsonString = JSONValue.toJSONString(obj);
        
        return jsonString;
    }
    
}
