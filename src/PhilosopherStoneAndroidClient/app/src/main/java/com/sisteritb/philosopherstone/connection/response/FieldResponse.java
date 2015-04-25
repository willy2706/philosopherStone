/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.sisteritb.philosopherstone.connection.response;

import org.json.simple.parser.ParseException;

/**
 *
 * @author winsxx
 */
public class FieldResponse extends Response{
    private final long item;

    public FieldResponse(String jsonString) throws ParseException, ResponseFailException, ResponseErrorException {
        super(jsonString);
        
        item = (long) responseJson.get("item");
    }

    /**
     * @return the item
     */
    public long getItem() {
        return item;
    }
    
}
