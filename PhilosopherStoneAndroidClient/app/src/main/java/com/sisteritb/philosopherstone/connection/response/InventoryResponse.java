/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.sisteritb.philosopherstone.connection.response;

import org.json.simple.JSONArray;
import org.json.simple.parser.ParseException;

/**
 *
 * @author winsxx
 */
public class InventoryResponse extends Response{
    private final long[] inventory;

    public InventoryResponse(String jsonString) throws ParseException, ResponseFailException, ResponseErrorException {
        super(jsonString);
        
        JSONArray jsonInventory = (JSONArray) responseJson.get("inventory");
        int inventorySize = jsonInventory.size();
        inventory = new long[inventorySize];
        for(int i=0; i<inventorySize; i++){
            inventory[i] = (long) jsonInventory.get(i);
        }
    }

    /**
     * @return the inventory
     */
    public long[] getInventory() {
        return inventory;
    }
    
}
