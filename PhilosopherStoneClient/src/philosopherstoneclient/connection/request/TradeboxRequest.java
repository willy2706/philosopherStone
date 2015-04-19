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
public class TradeboxRequest extends Request{
    
    public String token;

    public TradeboxRequest() {
        method = "tradebox";
    }
    
    @Override
    public String toJsonString() {
        Map obj = new LinkedHashMap();
        
        obj.put("method", method);
        obj.put("token", token);
        
        String jsonString = JSONValue.toJSONString(obj);
        
        return jsonString;
    }
    
}
