package com.sisteritb.philosopherstone.entity;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.sisteritb.philosopherstone.GameState;
import com.sisteritb.philosopherstone.R;
import com.sisteritb.philosopherstone.connection.PhilosopherStoneServer;
import com.sisteritb.philosopherstone.connection.request.CancelOfferRequest;
import com.sisteritb.philosopherstone.connection.request.FetchItemRequest;
import com.sisteritb.philosopherstone.connection.request.FieldRequest;
import com.sisteritb.philosopherstone.connection.request.Request;
import com.sisteritb.philosopherstone.connection.request.SendAcceptRequest;
import com.sisteritb.philosopherstone.connection.response.CancelOfferResponse;
import com.sisteritb.philosopherstone.connection.response.FetchItemResponse;
import com.sisteritb.philosopherstone.connection.response.FieldResponse;
import com.sisteritb.philosopherstone.connection.response.ResponseErrorException;
import com.sisteritb.philosopherstone.connection.response.ResponseFailException;
import com.sisteritb.philosopherstone.connection.response.SendAcceptResponse;

import java.util.ArrayList;

/**
 * Created by winsxx on 4/23/2015.
 */
public class TradeOfferAdapter extends ArrayAdapter<TradeOffer> {
    private ArrayList<TradeOffer> objects;
    private Context activityContext;
    private TradeOfferAdapter thisAdapter;

    public TradeOfferAdapter(Context context, int textViewResouceId, ArrayList<TradeOffer> objects) {
        super(context, textViewResouceId, objects);
        activityContext = context;
        this.objects = objects;
        thisAdapter = this;
    }

    public View getView(int position, View convertView, ViewGroup parent) {
        View v = convertView;
        final TradeOffer offer = objects.get(position);
        if (offer != null){

            if (v == null) {
                LayoutInflater inflater = (LayoutInflater) getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                v = inflater.inflate(R.layout.list_tradebox_item, null);
            }

            TextView offerItemAmountText = (TextView) v.findViewById(R.id.tradeBoxOfferItemAmountText);
            TextView demandAmountItemText = (TextView) v.findViewById(R.id.tradeBoxDemandItemAmountText);
            ImageView offerItemImage = (ImageView) v.findViewById(R.id.tradeBoxOfferImageView);
            ImageView demandItemImage = (ImageView) v.findViewById(R.id.tradeBoxDemandImageView);
            Button tradeBoxButton = (Button) v.findViewById(R.id.tradeBoxButton);

            if (offerItemImage != null) {
                offerItemImage.setImageResource(itemIdToResourceId(offer.offeredItem));
            }
            if (offerItemAmountText != null) {
                offerItemAmountText.setText("" + offer.offeredAmmount);
            }
            if (demandItemImage != null) {
                demandItemImage.setImageResource(itemIdToResourceId(offer.demandedItem));
            }
            if (demandAmountItemText != null) {
                demandAmountItemText.setText("" + offer.demandedAmmount);
            }

            if (parent.getId() == R.id.tradeBoxOfferListView) {
                Log.d("connection", "Create TradeBox List Item");

                if (offer.availability == false) {
                    tradeBoxButton.setText("Fetch");
                    tradeBoxButton.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            fetchItem(offer);
                        }
                    });
                } else {
                    tradeBoxButton.setText("Cancel");
                    tradeBoxButton.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            cancelOffer(offer);
                        }
                    });
                }

            } else if (parent.getId() == R.id.findOfferListView){
                Log.d("connection", "Create FindOffer List Item");

                if (offer.availability == true){
                    tradeBoxButton.setText("Buy");
                    tradeBoxButton.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            buyItem(offer);
                        }
                    });
                } else{
                    v = null;
                }
            }
        }
        return v;
    }

    private int itemIdToResourceId(long id){
        int itemId = (int) id;
        switch (itemId){
            case 0: return R.drawable.honey;
            case 1: return R.drawable.herbs;
            case 2: return R.drawable.clay;
            case 3: return R.drawable.mineral;
            case 4: return R.drawable.potion;
            case 5: return R.drawable.incense;
            case 6: return R.drawable.gems;
            case 7: return R.drawable.life_elixir;
            case 8: return R.drawable.mana_crystal;
            case 9: return R.drawable.philosopher_stone;
            default: return R.drawable.honey;
        }
    }

    private void buyItem(TradeOffer offer){
        SendAcceptRequest request = new SendAcceptRequest();
        request.token = GameState.loginToken;
        request.offerToken = offer.offerToken;

        new SendAcceptTask(offer).execute(request);
    }

    private void fetchItem(TradeOffer offer) {
        FetchItemRequest request = new FetchItemRequest();
        request.offerToken = offer.offerToken;
        request.token = GameState.loginToken;

        new FetchItemTask(offer).execute(request);
    }

    private void cancelOffer(TradeOffer offer) {
        CancelOfferRequest request = new CancelOfferRequest();
        request.offerToken = offer.offerToken;
        request.token = GameState.loginToken;

        new CancelOfferTask(offer).execute(request);
    }

    private class CancelOfferTask extends AsyncTask<CancelOfferRequest, Void, CancelOfferResponse> {

        private ResponseFailException failException = null;
        private TradeOffer offer;

        public CancelOfferTask(TradeOffer offer){
                this.offer = offer;
        }

        @Override
        protected CancelOfferResponse doInBackground(CancelOfferRequest... requests) {
            CancelOfferResponse response = null;
            try {
                response = GameState.philosopherStoneServer.send(requests[0]);
                Log.d("connection", "CancelOffer response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection", "CancelOffer fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection", "CancelOffer error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(CancelOfferResponse response) {

            if (response != null) {
                thisAdapter.remove(offer);
                Toast.makeText(activityContext, "Success CancelOffer", Toast.LENGTH_LONG).show();
            } else if (failException != null) {
                Toast.makeText(activityContext, failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(activityContext, PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }

    private class FetchItemTask extends AsyncTask<FetchItemRequest, Void, FetchItemResponse> {

        private ResponseFailException failException = null;
        private TradeOffer offer;

        public FetchItemTask(TradeOffer offer){
            this.offer = offer;
        }

        @Override
        protected FetchItemResponse doInBackground(FetchItemRequest... requests) {
            FetchItemResponse response = null;
            try {
                response = GameState.philosopherStoneServer.send(requests[0]);
                Log.d("connection", "FetchItem response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection", "FetchItem fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection", "FetchItem error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(FetchItemResponse response) {

            if (response != null) {
                thisAdapter.remove(offer);
                Toast.makeText(activityContext, "Success FetchItem", Toast.LENGTH_LONG).show();
            } else if (failException != null) {
                Toast.makeText(activityContext, failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(activityContext, PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }

    private class SendAcceptTask extends AsyncTask<SendAcceptRequest, Void, SendAcceptResponse> {

        private ResponseFailException failException = null;
        private TradeOffer offer;

        public SendAcceptTask(TradeOffer offer){
            this.offer = offer;
        }

        @Override
        protected SendAcceptResponse doInBackground(SendAcceptRequest... requests) {
            SendAcceptResponse response = null;
            try {
                response = GameState.philosopherStoneServer.send(requests[0]);
                Log.d("connection", "SendAccept response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection", "SendAccept fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection", "SendAccept error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(SendAcceptResponse response) {

            if (response != null) {
                thisAdapter.remove(offer);
                Toast.makeText(activityContext, "Success SendAccept", Toast.LENGTH_LONG).show();
            } else if (failException != null) {
                Toast.makeText(activityContext, failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(activityContext, PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }
}
