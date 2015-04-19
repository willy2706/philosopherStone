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
public class MixItemRequest extends Request{
    
    public String token;
    public int item1;
    public int item2;

    public MixItemRequest() {
        method = "mixitem";
    }
    
    @Override
    public String toString() {
        Map obj = new LinkedHashMap();
        
        obj.put("method", method);
        obj.put("token", token);
        obj.put("item1", item1);
        obj.put("item2", item2);
        
        String jsonString = JSONValue.toJSONString(obj);
        
        return jsonString;
    }
    
}
