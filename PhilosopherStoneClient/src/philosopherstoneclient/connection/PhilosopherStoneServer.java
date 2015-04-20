/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package philosopherstoneclient.connection;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.simple.parser.ParseException;
import philosopherstoneclient.connection.request.CancelOfferRequest;
import philosopherstoneclient.connection.request.FetchItemRequest;
import philosopherstoneclient.connection.request.FieldRequest;
import philosopherstoneclient.connection.request.InventoryRequest;
import philosopherstoneclient.connection.request.LoginRequest;
import philosopherstoneclient.connection.request.MapRequest;
import philosopherstoneclient.connection.request.MixItemRequest;
import philosopherstoneclient.connection.request.MoveRequest;
import philosopherstoneclient.connection.request.OfferRequest;
import philosopherstoneclient.connection.request.Request;
import philosopherstoneclient.connection.request.SendAcceptRequest;
import philosopherstoneclient.connection.request.SendFindRequest;
import philosopherstoneclient.connection.request.SignupRequest;
import philosopherstoneclient.connection.request.TradeboxRequest;
import philosopherstoneclient.connection.response.CancelOfferResponse;
import philosopherstoneclient.connection.response.FetchItemResponse;
import philosopherstoneclient.connection.response.FieldResponse;
import philosopherstoneclient.connection.response.InventoryResponse;
import philosopherstoneclient.connection.response.LoginResponse;
import philosopherstoneclient.connection.response.MapResponse;
import philosopherstoneclient.connection.response.MixItemResponse;
import philosopherstoneclient.connection.response.MoveResponse;
import philosopherstoneclient.connection.response.OfferResponse;
import philosopherstoneclient.connection.response.Response;
import philosopherstoneclient.connection.response.ResponseErrorException;
import philosopherstoneclient.connection.response.ResponseFailException;
import philosopherstoneclient.connection.response.SendAcceptResponse;
import philosopherstoneclient.connection.response.SendFindResponse;
import philosopherstoneclient.connection.response.SignupResponse;
import philosopherstoneclient.connection.response.TradeboxResponse;

/**
 *
 * @author winsxx
 */
public class PhilosopherStoneServer {
    JsonSocket socket;
    
    public PhilosopherStoneServer(JsonSocket socket) {
        this.socket = socket;
    }
    
    public SignupResponse send(SignupRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new SignupResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public LoginResponse send(LoginRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new LoginResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public InventoryResponse send(InventoryRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new InventoryResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public MixItemResponse send(MixItemRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new MixItemResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
        
    public MapResponse send(MapRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new MapResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public MoveResponse send(MoveRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new MoveResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public FieldResponse send(FieldRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new FieldResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public OfferResponse send(OfferRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new OfferResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public TradeboxResponse send(TradeboxRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new TradeboxResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public SendFindResponse send(SendFindRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new SendFindResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public SendAcceptResponse send(SendAcceptRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new SendAcceptResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public FetchItemResponse send(FetchItemRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new FetchItemResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    public CancelOfferResponse send(CancelOfferRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new CancelOfferResponse(responseString);
        } catch (IOException | ParseException ex) {
            Logger.getLogger(PhilosopherStoneServer.class.getName()).log(Level.SEVERE, null, ex);
            throw new ResponseErrorException();
        } 
    }
    
    private String sendRequest(String requestString) throws IOException{
        socket.connect();
        socket.write(requestString);
        String responseString = socket.read();
        socket.close();
        return responseString;
        
    }
}
