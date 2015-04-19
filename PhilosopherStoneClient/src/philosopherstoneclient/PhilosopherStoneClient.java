/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package philosopherstoneclient;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import philosopherstoneclient.connection.JsonSocket;
import philosopherstoneclient.connection.request.MixItemRequest;
import philosopherstoneclient.connection.request.SignUpRequest;

/**
 *
 * @author winsxx
 */
public class PhilosopherStoneClient {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        SignUpRequest sur = new SignUpRequest();
        sur.password = "1434325";
        sur.username = "kelvahn";
        
        String json = sur.toString();
        System.out.println(json);
        
        JsonSocket js = new JsonSocket("167.205.32.46", 8025, 5000);
        for(int i=0; i<3; i++){
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
                js.write(json);
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
        
        MixItemRequest mir = new MixItemRequest();
        mir.item1 = 0;
        mir.item2 = 1;
        mir.token = "agagargarha";
        System.out.println(mir);
    }
    
}
