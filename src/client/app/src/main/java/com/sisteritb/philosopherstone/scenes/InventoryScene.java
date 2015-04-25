package com.sisteritb.philosopherstone.scenes;

import android.graphics.Color;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.sisteritb.philosopherstone.GameState;
import com.sisteritb.philosopherstone.R;
import com.sisteritb.philosopherstone.connection.PhilosopherStoneServer;
import com.sisteritb.philosopherstone.connection.request.FieldRequest;
import com.sisteritb.philosopherstone.connection.request.InventoryRequest;
import com.sisteritb.philosopherstone.connection.request.MixItemRequest;
import com.sisteritb.philosopherstone.connection.request.OfferRequest;
import com.sisteritb.philosopherstone.connection.response.FieldResponse;
import com.sisteritb.philosopherstone.connection.response.InventoryResponse;
import com.sisteritb.philosopherstone.connection.response.MixItemResponse;
import com.sisteritb.philosopherstone.connection.response.OfferResponse;
import com.sisteritb.philosopherstone.connection.response.ResponseErrorException;
import com.sisteritb.philosopherstone.connection.response.ResponseFailException;

public class InventoryScene extends ActionBarActivity {
    private static final int SELECTION_PADDING = 5;
    private static final int SELECTION_1_COLOR = 0xff83392b;
    private static final int SELECTION_2_COLOR = 0xffb6b032;
    private static final long UNSELECTED_ID = -1;

    private PhilosopherStoneServer psServer;
    private long selectItem1, selectItem2;

    private EditText offerAmountEditText, demandAmountEditText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_inventory_scene);

        psServer = GameState.philosopherStoneServer;

        offerAmountEditText = (EditText) findViewById(R.id.offerAmountEditText);
        demandAmountEditText = (EditText) findViewById(R.id.demandAmountEditText);

        requestInventory();
        selectItem1 = UNSELECTED_ID;
        selectItem2 = UNSELECTED_ID;
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_inventory_scene, menu);
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

    private void requestInventory(){
        InventoryRequest request = new InventoryRequest();
        request.token = GameState.loginToken;

        new InventoryTask().execute(request);
    }

    private void requestMixItem(){
        MixItemRequest request = new MixItemRequest();
        request.token = GameState.loginToken;
        request.item1 = selectItem1;
        request.item2 = selectItem2;
        new MixItemTask().execute(request);

    }

    public void imageClick(View view) {
        ImageView itemImage = (ImageView) view;
        long itemImageId = convertImageIdToItemNumber(view.getId());
        if(selectItem1 == itemImageId){
            deselect(itemImage);
            selectItem1 = UNSELECTED_ID;
        } else if (selectItem2 == itemImageId){
            deselect(itemImage);
            selectItem2 = UNSELECTED_ID;
        } else if (selectItem1 == UNSELECTED_ID){
            select1(itemImage);
            selectItem1 = itemImageId;
        } else if (selectItem2 == UNSELECTED_ID){
            select2(itemImage);
            selectItem2 = itemImageId;
        }
    }

    private void select1(ImageView view){
        view.setPadding(SELECTION_PADDING,SELECTION_PADDING,SELECTION_PADDING,SELECTION_PADDING);
        view.setBackgroundColor(SELECTION_1_COLOR);
        view.invalidate();
    }

    private void select2(ImageView view){
        view.setPadding(SELECTION_PADDING,SELECTION_PADDING,SELECTION_PADDING,SELECTION_PADDING);
        view.setBackgroundColor(SELECTION_2_COLOR);
        view.invalidate();
    }

    private void deselect(ImageView view){
        view.setPadding(0,0,0,0);
        view.setBackgroundColor(Color.TRANSPARENT);
        view.invalidate();
    }

    private long convertImageIdToItemNumber(int id){
        if (id == R.id.item0Image){
            return 0;
        } else if (id == R.id.item1Image){
            return 1;
        } else if (id == R.id.item2Image){
            return 2;
        } else if (id == R.id.item3Image){
            return 3;
        } else if (id == R.id.item4Image){
            return 4;
        } else if (id == R.id.item5Image){
            return 5;
        } else if (id == R.id.item6Image){
            return 6;
        } else if (id == R.id.item7Image){
            return 7;
        } else if (id == R.id.item8Image){
            return 8;
        } else if (id == R.id.item9Image){
            return 9;
        }
        return -1;
    }

    private void setInventoryToView(long[] items) {
        TextView amountText;

        amountText = (TextView) findViewById(R.id.item0TextView);
        amountText.setText(""+items[0]);

        amountText = (TextView) findViewById(R.id.item1TextView);
        amountText.setText(""+items[1]);

        amountText = (TextView) findViewById(R.id.item2TextView);
        amountText.setText(""+items[2]);

        amountText = (TextView) findViewById(R.id.item3TextView);
        amountText.setText(""+items[3]);

        amountText = (TextView) findViewById(R.id.item4TextView);
        amountText.setText(""+items[4]);

        amountText = (TextView) findViewById(R.id.item5TextView);
        amountText.setText(""+items[5]);

        amountText = (TextView) findViewById(R.id.item6TextView);
        amountText.setText(""+items[6]);

        amountText = (TextView) findViewById(R.id.item7TextView);
        amountText.setText(""+items[7]);

        amountText = (TextView) findViewById(R.id.item8TextView);
        amountText.setText(""+items[8]);

        amountText = (TextView) findViewById(R.id.item9TextView);
        amountText.setText(""+items[9]);
    }

    public void mixItem(View view) {
        if (selectItem1 != UNSELECTED_ID && selectItem2 != UNSELECTED_ID) {
            requestMixItem();
        }
    }

    public void offerItem(View view) {
        long offerAmount = 0;
        String offerAmountString = offerAmountEditText.getText().toString();
        if(offerAmountString.length()>0){
            offerAmount = Integer.parseInt(offerAmountString);
        }

        long demandAmount = 0;
        String demandAmountString = demandAmountEditText.getText().toString();
        if(offerAmountString.length()>0){
            demandAmount = Integer.parseInt(demandAmountString);
        }

        if(offerAmount >0 && demandAmount >0 && selectItem1!=UNSELECTED_ID && selectItem2!=UNSELECTED_ID){
            requestOfferItem(selectItem1, offerAmount, selectItem2, demandAmount);
        }
    }

    private void requestOfferItem(long offer, long offerAmount, long demand, long demandAmount){
        OfferRequest request = new OfferRequest();
        request.token = GameState.loginToken;
        request.demandedItem = demand;
        request.demandedItemAmmunt = demandAmount;
        request.offeredItem = offer;
        request.offeredItemAmmount = offerAmount;

        new OfferTask().execute(request);
    }

    private class InventoryTask extends AsyncTask<InventoryRequest, Void, InventoryResponse> {

        private ResponseFailException failException = null;

        @Override
        protected InventoryResponse doInBackground(InventoryRequest... requests) {
            InventoryResponse response = null;
            try {
                response = psServer.send(requests[0]);
                Log.d("connection", "Inventory response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","Inventory fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","Inventory error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(InventoryResponse response){

            if (response != null) {
                long[] items = response.getInventory();
                setInventoryToView(items);
                Toast.makeText(getApplicationContext(), "Retrive Inventory Done", Toast.LENGTH_LONG).show();
            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }

    private class MixItemTask extends AsyncTask<MixItemRequest, Void, MixItemResponse> {

        private ResponseFailException failException = null;

        @Override
        protected MixItemResponse doInBackground(MixItemRequest... requests) {
            MixItemResponse response = null;
            try {
                response = psServer.send(requests[0]);
                Log.d("connection", "MixItem response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","MixItem fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","MixItem error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(MixItemResponse response){

            if (response != null) {
                Toast.makeText(getApplicationContext(), "MixItem Done", Toast.LENGTH_LONG).show();
                requestInventory();
            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }

    private class OfferTask extends AsyncTask<OfferRequest, Void, OfferResponse> {

        private ResponseFailException failException = null;

        @Override
        protected OfferResponse doInBackground(OfferRequest... requests) {
            OfferResponse response = null;
            try {
                response = psServer.send(requests[0]);
                Log.d("connection", "Offer response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","Offer fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","Offer error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(OfferResponse response){

            if (response != null) {
                Toast.makeText(getApplicationContext(), "Offer Done", Toast.LENGTH_LONG).show();
                requestInventory();
            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }
}
