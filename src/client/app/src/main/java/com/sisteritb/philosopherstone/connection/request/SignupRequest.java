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
public class SignupRequest extends Request{
    public String username;
    public String password;
    
    public SignupRequest() {
        method = "signup";
    }
    
    @Override
    public String toString() {
        Map obj = new LinkedHashMap();
        
        obj.put("method", method);
        obj.put("username", username);
        obj.put("password", password);
        
        String jsonString = JSONValue.toJSONString(obj);
        
        return jsonString;
    }
    
}
