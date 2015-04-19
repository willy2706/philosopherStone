/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package philosopherstoneclient.connection.request;

import java.util.LinkedHashMap;
import java.util.Map;
import org.json.simple.JSONValue;

/**
 *
 * @author winsxx
 */
public class LoginRequest extends Request{
    public String username;
    public String password;
    
    public LoginRequest(){
        method = "login";
    }
    
    @Override
    public String toJsonString() {
        Map obj = new LinkedHashMap();
        
        obj.put("method", method);
        obj.put("username", username);
        obj.put("password", password);
        
        String jsonString = JSONValue.toJSONString(obj);
        
        return jsonString;
    }
    
}
