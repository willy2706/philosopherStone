/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package philosopherstoneclient;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.simple.parser.ParseException;
import philosopherstoneclient.connection.JsonSocket;
import philosopherstoneclient.connection.request.LoginRequest;
import philosopherstoneclient.connection.request.MixItemRequest;
import philosopherstoneclient.connection.request.SignUpRequest;
import philosopherstoneclient.connection.response.LoginResponse;
import philosopherstoneclient.connection.response.ResponseErrorException;
import philosopherstoneclient.connection.response.ResponseFailException;

/**
 *
 * @author winsxx
 */
public class PhilosopherStoneClient {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        String password = "1434325";
        String username = "kelvahn";
        
        JsonSocket js = new JsonSocket("167.205.32.46", 8025, 5000);
        for(int i=0; i<1; i++){
            try {
                System.out.println("Start write");
                js.connect();
                System.out.println("Done connect");
            } catch (IOException ex) {
                System.out.println("fail connect");
                Logger.getLogger(PhilosopherStoneClient.class.getName()).log(Level.SEVERE, null, ex);
            }
            try {
                System.out.println("Start write");
                LoginRequest lr = new LoginRequest();
                lr.password = password;
                lr.username = username;
                js.write(lr.toString());
                System.out.println("Done write");
            } catch (IOException ex) {
                System.out.println("fail write");
                Logger.getLogger(PhilosopherStoneClient.class.getName()).log(Level.SEVERE, null, ex);
            }
            String output;
            try {
                System.out.println("Start read");
                output = js.read();
                System.out.println("Done read");
                System.out.println(output);
                System.out.println("Start parsing");
                try {
                    LoginResponse response = new LoginResponse(output);
                    System.out.println(response.getToken());
                    System.out.println(response.getTime());
                    System.out.println(response.getX());
                    System.out.println(response.getY());
                } catch (ParseException | ResponseFailException | ResponseErrorException ex) {
                    Logger.getLogger(PhilosopherStoneClient.class.getName()).log(Level.SEVERE, null, ex);
                }
            } catch (IOException ex) {
                System.out.println("fail read");
                Logger.getLogger(PhilosopherStoneClient.class.getName()).log(Level.SEVERE, null, ex);
            }
            try {
                js.close();
            } catch (IOException ex) {
                Logger.getLogger(PhilosopherStoneClient.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        System.out.println("Done");
        
        
    }
    
}
