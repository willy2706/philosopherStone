package com.sisteritb.philosopherstone.scenes;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.CountDownTimer;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.sisteritb.philosopherstone.GameState;
import com.sisteritb.philosopherstone.R;
import com.sisteritb.philosopherstone.connection.PhilosopherStoneServer;
import com.sisteritb.philosopherstone.connection.request.FieldRequest;
import com.sisteritb.philosopherstone.connection.request.MapRequest;
import com.sisteritb.philosopherstone.connection.request.MoveRequest;
import com.sisteritb.philosopherstone.connection.request.SignupRequest;
import com.sisteritb.philosopherstone.connection.response.FieldResponse;
import com.sisteritb.philosopherstone.connection.response.MapResponse;
import com.sisteritb.philosopherstone.connection.response.MoveResponse;
import com.sisteritb.philosopherstone.connection.response.ResponseErrorException;
import com.sisteritb.philosopherstone.connection.response.ResponseFailException;
import com.sisteritb.philosopherstone.connection.response.SignupResponse;

public class MapScene extends ActionBarActivity {

    PhilosopherStoneServer psServer;
    EditText rowEditText, columnEditText;
    TextView mapNameText, arrivedTimeText, maxSizeText;
    CountDownTimer timer;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_map_scene);

        rowEditText = (EditText) findViewById(R.id.rowEditText);
        columnEditText = (EditText) findViewById(R.id.columnEditText);
        mapNameText = (TextView) findViewById(R.id.mapNameText);
        arrivedTimeText = (TextView) findViewById(R.id.arrivedTimeText);
        maxSizeText = (TextView) findViewById(R.id.mapSizeText);

        psServer = GameState.philosopherStoneServer;

        initPlayerInfo();
        initMapInfo();
        initTimer();
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main_scene, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.inventory){
            Intent intent = new Intent(this, InventoryScene.class);
            startActivity(intent);
            return true;
        } else if (id == R.id.finditem){
            Intent intent = new Intent(this, FindOfferScene.class);
            startActivity(intent);
            return true;
        } else if (id == R.id.tradebox){
            Intent intent = new Intent(this, TradeboxScene.class);
            startActivity(intent);
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void initTimer(){

    }

    public void movePlayer(View view) {
        MoveRequest request = new MoveRequest();
        request.token = GameState.loginToken;

        String columnString = columnEditText.getText().toString();
        int col = 0;
        if(columnString.length() > 0){
            col = Integer.parseInt(columnString);
        }
        request.x = col;

        String rowString = rowEditText.getText().toString();
        int row = 0;
        if(rowString.length() > 0){
            row = Integer.parseInt(rowString);
        }
        request.y = row;

        new MoveTask().execute(request);
    }

    public void takeFieldItem(View view) {
        FieldRequest request = new FieldRequest();
        request.token = GameState.loginToken;

        new FieldTask().execute(request);
    }

    private void initPlayerInfo(){
        rowEditText.setText(""+GameState.location_y);
        columnEditText.setText(""+GameState.location_x);
        Log.d("ui", "Current time millis:" + System.currentTimeMillis()+" Arrived:"+GameState.arrivedTime);
        if(GameState.arrivedTime > System.currentTimeMillis()){
            setTimer(System.currentTimeMillis(),GameState.arrivedTime);
        } else {
            arrivedTimeText.setText("You are at row:" + GameState.location_y+" col:"+GameState.location_x);
        }
    }

    private void setTimer(long now, long arrived){
        if(timer != null){
            timer.cancel();
        }
        timer = new CountDownTimer(arrived - now,1000){

            @Override
            public void onTick(long millisUntilFinished) {
                long second = millisUntilFinished/1000;
                arrivedTimeText.setText("Walking, arrived in "+second/60+" minutes and "+second%60+" seconds.");
            }

            @Override
            public void onFinish() {
                arrivedTimeText.setText("You are at row:" + GameState.location_y+" col:"+GameState.location_x);
            }
        }.start();
    }

    private void initMapInfo(){
        MapRequest request = new MapRequest();
        request.token = GameState.loginToken;

        if(GameState.USE_STUB){
            mapNameText.setText("Map Name: Stub Map");
            maxSizeText.setText("Max row: 5, Max column: 5");
        } else {
            new MapTask().execute(request);
        }
    }

    private class MapTask extends AsyncTask<MapRequest, Void, MapResponse> {

        private ResponseFailException failException = null;

        @Override
        protected MapResponse doInBackground(MapRequest... requests) {
            MapResponse response = null;
            try {
                response = psServer.send(requests[0]);
                Log.d("connection", "Move response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","Move fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","Move error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(MapResponse response){

            if (response != null) {
                mapNameText.setText("Map Name: "+response.getName());
                maxSizeText.setText("Max Row: "+response.getHeight()+", Max Column: "+response.getWidth());
                Toast.makeText(getApplicationContext(), "Map success.", Toast.LENGTH_LONG).show();
            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }

    private class MoveTask extends AsyncTask<MoveRequest, Void, MoveResponse> {

        private ResponseFailException failException = null;
        private long x, y;

        @Override
        protected MoveResponse doInBackground(MoveRequest... requests) {
            MoveResponse response = null;
            try {
                response = psServer.send(requests[0]);
                x = requests[0].x;
                y = requests[0].y;
                Log.d("connection", "Move response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","Move fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","Move error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(MoveResponse response){

            if (response != null) {
                GameState.arrivedTime = response.getTime()*1000;
                if(GameState.arrivedTime > System.currentTimeMillis()){
                    setTimer(System.currentTimeMillis(),GameState.arrivedTime);
                } else {
                    arrivedTimeText.setText("You are at row:" + GameState.location_y+" col:"+GameState.location_x);
                }
                Toast.makeText(getApplicationContext(), "Move success.", Toast.LENGTH_LONG).show();
            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }

    private class FieldTask extends AsyncTask<FieldRequest, Void, FieldResponse> {

        private ResponseFailException failException = null;

        @Override
        protected FieldResponse doInBackground(FieldRequest... requests) {
            FieldResponse response = null;
            try {
                response = psServer.send(requests[0]);
                Log.d("connection", "Field response created.");
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","Field fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","Field error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(FieldResponse response){

            if (response != null) {
                long item = response.getItem();
                Toast.makeText(getApplicationContext(), "You get item: "+item, Toast.LENGTH_LONG).show();
            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }
}
