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
public class MoveRequest extends Request{
    
    public String token;
    public int x, y;

    public MoveRequest() {
        method = "move";
    }
    
    @Override
    public String toString() {
        Map obj = new LinkedHashMap();
        
        obj.put("method", method);
        obj.put("token", token);
        obj.put("x", x);
        obj.put("y", y);
        
        String jsonString = JSONValue.toJSONString(obj);
        
        return jsonString;
    }
    
}
