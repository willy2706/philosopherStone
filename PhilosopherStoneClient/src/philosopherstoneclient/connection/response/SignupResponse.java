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
public class SignupResponse extends Response{

    public SignupResponse(String jsonString) throws ParseException, ResponseFailException, ResponseErrorException {
        super(jsonString);
    }
    
}
