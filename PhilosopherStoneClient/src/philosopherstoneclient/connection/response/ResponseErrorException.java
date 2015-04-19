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
public class ResponseErrorException extends Exception{
    
    public ResponseErrorException(){
        super();
    }
    
    public ResponseErrorException(String message){
        super(message);
    }
    
    public ResponseErrorException(String message, Throwable cause){
        super(message, cause);
    }
    
    public ResponseErrorException(Throwable cause){
        super(cause);
    }
    
}
