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
public class SendAcceptRequest extends Request{
    
    public String token;
    public String offerToken;

    public SendAcceptRequest() {
        method = "sendaccept";
    }
    
    @Override
    public String toString() {
        Map obj = new LinkedHashMap();
        
        obj.put("method", method);
        obj.put("token", token);
        obj.put("offer_token", offerToken);
        
        String jsonString = JSONValue.toJSONString(obj);
        
        return jsonString;
    }
    
}
