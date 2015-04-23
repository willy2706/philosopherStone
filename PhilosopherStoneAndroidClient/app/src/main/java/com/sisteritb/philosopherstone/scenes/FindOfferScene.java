package com.sisteritb.philosopherstone.scenes;

import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import com.sisteritb.philosopherstone.GameState;
import com.sisteritb.philosopherstone.R;
import com.sisteritb.philosopherstone.connection.PhilosopherStoneServer;
import com.sisteritb.philosopherstone.connection.request.Request;
import com.sisteritb.philosopherstone.connection.request.SendFindRequest;
import com.sisteritb.philosopherstone.connection.request.TradeboxRequest;
import com.sisteritb.philosopherstone.connection.response.ResponseErrorException;
import com.sisteritb.philosopherstone.connection.response.ResponseFailException;
import com.sisteritb.philosopherstone.connection.response.SendFindResponse;
import com.sisteritb.philosopherstone.connection.response.TradeboxResponse;
import com.sisteritb.philosopherstone.entity.TradeOffer;
import com.sisteritb.philosopherstone.entity.TradeOfferAdapter;

import java.util.ArrayList;
import java.util.Arrays;

public class FindOfferScene extends ActionBarActivity {
    private PhilosopherStoneServer psServer;
    private TradeOfferAdapter offerAdapter;
    private ListView findOfferListView;
    private EditText findOfferEditText;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_find_offer_scene);

        psServer = GameState.philosopherStoneServer;

        findOfferEditText = (EditText) findViewById(R.id.findOfferItemIdEditText);
        findOfferListView = (ListView) findViewById(R.id.findOfferListView);
        offerAdapter = new TradeOfferAdapter(this, R.layout.list_tradebox_item, new ArrayList<TradeOffer>());
        findOfferListView.setAdapter(offerAdapter);

        findOfferInitial();
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_find_offer_scene, menu);
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

    private void findItem(long id){
        SendFindRequest request = new SendFindRequest();
        request.item = id;
        request.token = GameState.loginToken;

        new SendFindTask().execute(request);
    }

    public void findOfferClick(View view) {
        offerAdapter.clear();
        String findOfferIdString = findOfferEditText.getText().toString();
        long findOfferId = -1;
        if (findOfferIdString.length() > 0){
            findOfferId = Integer.parseInt(findOfferIdString);
        }
        if(findOfferId>=0 && findOfferId <10){
            findItem(findOfferId);
        } else {
            for(int i=0; i<10; i++){
                findItem(i);
            }
        }
    }

    private void findOfferInitial(){
        offerAdapter.clear();
        for(int i=0; i<10; i++){
            findItem(i);
        }
    }

    private class SendFindTask extends AsyncTask<SendFindRequest, Void, SendFindResponse> {

        private ResponseFailException failException = null;

        @Override
        protected SendFindResponse doInBackground(SendFindRequest... requests) {
            SendFindResponse response = null;
            try {
                response = psServer.send(requests[0]);
                Log.d("connection", "SendFind response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","SendFind fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","SendFind error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(SendFindResponse response){

            if (response != null) {
                offerAdapter.addAll(response.getOffers());
                offerAdapter.notifyDataSetChanged();

                Toast.makeText(getApplicationContext(), "Success SendFind", Toast.LENGTH_SHORT).show();
            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }

}
