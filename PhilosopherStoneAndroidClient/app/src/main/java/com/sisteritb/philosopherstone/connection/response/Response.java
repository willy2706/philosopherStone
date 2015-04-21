/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.sisteritb.philosopherstone.connection.response;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/**
 *
 * @author winsxx
 */
public abstract class Response {
    protected JSONObject responseJson;
    
    protected Response(String jsonString) throws ParseException, ResponseFailException, ResponseErrorException{
        JSONParser jsonParser = new JSONParser();
        responseJson = (JSONObject) jsonParser.parse(jsonString);
        
        String status = (String) responseJson.get("status");
        if(!status.equals("ok")){
            if (status.equals("fail")){
                String description = (String) responseJson.get("description");
                throw new ResponseFailException(description);
            }else{
                throw new ResponseErrorException();
            }
        }
    }
    
}
