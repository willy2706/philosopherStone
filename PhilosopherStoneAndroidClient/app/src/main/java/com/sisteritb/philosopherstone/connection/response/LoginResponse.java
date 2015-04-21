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
public class LoginResponse extends Response{
    private final String token;
    private final long x, y, time;

    public LoginResponse(String jsonString) throws ParseException, ResponseFailException, ResponseErrorException {
        super(jsonString);
        
        token = (String) responseJson.get("token");
        x = (long) responseJson.get("x");
        y = (long) responseJson.get("y");
        time = (long) responseJson.get("time");
    }

    /**
     * @return the token
     */
    public String getToken() {
        return token;
    }

    /**
     * @return the x
     */
    public long getX() {
        return x;
    }

    /**
     * @return the y
     */
    public long getY() {
        return y;
    }

    /**
     * @return the time
     */
    public long getTime() {
        return time;
    }
    
}
