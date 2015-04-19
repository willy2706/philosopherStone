/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package philosopherstoneclient.connection.response;

/**
 *
 * @author winsxx
 */
public class ResponseFailException extends Exception{
    public ResponseFailException(){
        super();
    }
    
    public ResponseFailException(String message){
        super(message);
    }
    
    public ResponseFailException(String message, Throwable cause){
        super(message, cause);
    }
    
    public ResponseFailException(Throwable cause){
        super(cause);
    }
}
