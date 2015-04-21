package com.sisteritb.philosopherstone.connection;

import com.sisteritb.philosopherstone.connection.request.CancelOfferRequest;
import com.sisteritb.philosopherstone.connection.request.FetchItemRequest;
import com.sisteritb.philosopherstone.connection.request.FieldRequest;
import com.sisteritb.philosopherstone.connection.request.InventoryRequest;
import com.sisteritb.philosopherstone.connection.request.LoginRequest;
import com.sisteritb.philosopherstone.connection.request.MapRequest;
import com.sisteritb.philosopherstone.connection.request.MixItemRequest;
import com.sisteritb.philosopherstone.connection.request.MoveRequest;
import com.sisteritb.philosopherstone.connection.request.OfferRequest;
import com.sisteritb.philosopherstone.connection.request.SendAcceptRequest;
import com.sisteritb.philosopherstone.connection.request.SendFindRequest;
import com.sisteritb.philosopherstone.connection.request.SignupRequest;
import com.sisteritb.philosopherstone.connection.request.TradeboxRequest;
import com.sisteritb.philosopherstone.connection.response.CancelOfferResponse;
import com.sisteritb.philosopherstone.connection.response.FetchItemResponse;
import com.sisteritb.philosopherstone.connection.response.FieldResponse;
import com.sisteritb.philosopherstone.connection.response.InventoryResponse;
import com.sisteritb.philosopherstone.connection.response.LoginResponse;
import com.sisteritb.philosopherstone.connection.response.MapResponse;
import com.sisteritb.philosopherstone.connection.response.MixItemResponse;
import com.sisteritb.philosopherstone.connection.response.MoveResponse;
import com.sisteritb.philosopherstone.connection.response.OfferResponse;
import com.sisteritb.philosopherstone.connection.response.ResponseErrorException;
import com.sisteritb.philosopherstone.connection.response.ResponseFailException;
import com.sisteritb.philosopherstone.connection.response.SendAcceptResponse;
import com.sisteritb.philosopherstone.connection.response.SendFindResponse;
import com.sisteritb.philosopherstone.connection.response.SignupResponse;
import com.sisteritb.philosopherstone.connection.response.TradeboxResponse;

import org.json.simple.parser.ParseException;

import java.io.IOException;

public class PhilosopherStoneServer {
    public static final String ERROR_MESSAGE = "Sorry, problem with server.";
    private JsonSocket socket;

    public PhilosopherStoneServer(JsonSocket socket) {
        this.socket = socket;
    }

    public SignupResponse send(SignupRequest req) throws ResponseFailException, ResponseErrorException {
        try {
            String responseString = sendRequest(req.toString());
            return new SignupResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public LoginResponse send(LoginRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new LoginResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public InventoryResponse send(InventoryRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new InventoryResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public MixItemResponse send(MixItemRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new MixItemResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public MapResponse send(MapRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new MapResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public MoveResponse send(MoveRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new MoveResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public FieldResponse send(FieldRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new FieldResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public OfferResponse send(OfferRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new OfferResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public TradeboxResponse send(TradeboxRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new TradeboxResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public SendFindResponse send(SendFindRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new SendFindResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public SendAcceptResponse send(SendAcceptRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new SendAcceptResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public FetchItemResponse send(FetchItemRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new FetchItemResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
            throw new ResponseErrorException();
        }
    }

    public CancelOfferResponse send(CancelOfferRequest req) throws ResponseFailException, ResponseErrorException{
        try {
            String responseString = sendRequest(req.toString());
            return new CancelOfferResponse(responseString);
        } catch (IOException | ParseException ex) {
            ex.printStackTrace();
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
