/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.sisteritb.philosopherstone.connection.request;

/**
 *
 * @author winsxx
 */
public abstract class Request {
    
    protected String method;
    
    public String getMethod(){
        return method;
    }
    
    public abstract String toString();
    
}
