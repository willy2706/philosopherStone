package com.sisteritb.philosopherstone.scenes;

import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ListView;
import android.widget.Toast;

import com.sisteritb.philosopherstone.GameState;
import com.sisteritb.philosopherstone.R;
import com.sisteritb.philosopherstone.connection.PhilosopherStoneServer;
import com.sisteritb.philosopherstone.connection.request.TradeboxRequest;
import com.sisteritb.philosopherstone.connection.response.ResponseErrorException;
import com.sisteritb.philosopherstone.connection.response.ResponseFailException;
import com.sisteritb.philosopherstone.connection.response.TradeboxResponse;
import com.sisteritb.philosopherstone.entity.TradeOffer;
import com.sisteritb.philosopherstone.entity.TradeOfferAdapter;

import java.util.ArrayList;
import java.util.Arrays;

public class TradeboxScene extends ActionBarActivity {
    private TradeOfferAdapter offerAdapter;
    private ListView offerListView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tradebox_scene);

        ArrayList<TradeOffer> tradeOffer;
        if (GameState.USE_STUB) {
            tradeOffer = genereteTradeOfferStub();
            setTradeBoxToAdapter(tradeOffer);
        } else {
            requestTradeBox();
        }

        offerListView = (ListView) findViewById(R.id.tradeBoxOfferListView);

    }

    private ArrayList<TradeOffer> genereteTradeOfferStub(){
        ArrayList<TradeOffer> offers = new ArrayList<>();
        offers.add(new TradeOffer("12344",1,2,3,4,true));
        offers.add(new TradeOffer("12344",1,2,3,4,true));
        offers.add(new TradeOffer("12344",1,2,3,4,false));
        offers.add(new TradeOffer("12344",1,2,3,4,true));
        offers.add(new TradeOffer("12344",1,2,3,4,false));
        offers.add(new TradeOffer("12344",1,2,3,4,true));
        offers.add(new TradeOffer("12344",1,2,3,4,true));
        offers.add(new TradeOffer("12344",1,2,3,4,false));
        offers.add(new TradeOffer("12344",1,2,3,4,true));
        offers.add(new TradeOffer("12344",1,2,3,4,false));
        offers.add(new TradeOffer("12344",1,2,3,4,true));
        offers.add(new TradeOffer("12344",1,2,3,4,true));
        offers.add(new TradeOffer("12344",1,2,3,4,false));
        offers.add(new TradeOffer("12344",1,2,3,4,true));
        offers.add(new TradeOffer("12344",1,2,3,4,false));
        return offers;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_tradebox_scene, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    private void requestTradeBox(){
        TradeboxRequest request = new TradeboxRequest();
        request.token = GameState.loginToken;

        new TradeboxTask().execute(request);
    }

    private void setTradeBoxToAdapter(ArrayList<TradeOffer> tradeOffers){
        offerAdapter = new TradeOfferAdapter(this, R.layout.list_tradebox_item, tradeOffers);
        offerListView.setAdapter(offerAdapter);
    }

    private class TradeboxTask extends AsyncTask<TradeboxRequest, Void, TradeboxResponse> {

        private ResponseFailException failException = null;

        @Override
        protected TradeboxResponse doInBackground(TradeboxRequest... requests) {
            TradeboxResponse response = null;
            try {
                response = GameState.philosopherStoneServer.send(requests[0]);
                Log.d("connection", "Tradebox response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","Tradebox fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","Tradebox error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(TradeboxResponse response){

            if (response != null) {
                ArrayList<TradeOffer> offers = new ArrayList<TradeOffer>(Arrays.asList(response.getOffers()));
                setTradeBoxToAdapter(offers);

                Toast.makeText(getApplicationContext(), "Success Tradebox", Toast.LENGTH_LONG).show();
            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }
}
