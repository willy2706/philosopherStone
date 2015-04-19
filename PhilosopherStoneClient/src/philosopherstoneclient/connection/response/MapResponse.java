/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package philosopherstoneclient.connection.response;

import org.json.simple.parser.ParseException;

/**
 *
 * @author winsxx
 */
public class MapResponse extends Response{
    private final String name;
    private final long width, height;

    public MapResponse(String jsonString) throws ParseException, ResponseFailException, ResponseErrorException {
        super(jsonString);
        
        name = (String) responseJson.get("name");
        width = (long) responseJson.get("width");
        height = (long) responseJson.get("height");
    }

    /**
     * @return the name
     */
    public String getName() {
        return name;
    }

    /**
     * @return the width
     */
    public long getWidth() {
        return width;
    }

    /**
     * @return the height
     */
    public long getHeight() {
        return height;
    }
    
}
