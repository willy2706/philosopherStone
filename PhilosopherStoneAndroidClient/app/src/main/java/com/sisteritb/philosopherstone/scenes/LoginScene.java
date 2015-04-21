package com.sisteritb.philosopherstone.scenes;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.SpannableStringBuilder;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.sisteritb.philosopherstone.R;
import com.sisteritb.philosopherstone.connection.JsonSocket;
import com.sisteritb.philosopherstone.connection.PhilosopherStoneServer;
import com.sisteritb.philosopherstone.connection.request.LoginRequest;
import com.sisteritb.philosopherstone.connection.request.SignupRequest;
import com.sisteritb.philosopherstone.connection.response.LoginResponse;
import com.sisteritb.philosopherstone.connection.response.ResponseErrorException;
import com.sisteritb.philosopherstone.connection.response.ResponseFailException;
import com.sisteritb.philosopherstone.connection.response.SignupResponse;

public class LoginScene extends Activity {
    private static int CONNECTION_TIMEOUT = 5000;

    private EditText usernameText, passwordText, portText, hostText;
    private PhilosopherStoneServer psServer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_scene);

        usernameText = (EditText) findViewById(R.id.username);
        passwordText = (EditText) findViewById(R.id.password);
        hostText = (EditText) findViewById(R.id.host);
        portText = (EditText) findViewById(R.id.port);

    }

    public void loginPlayer(View view) {
        String hostString = hostText.getText().toString();
        int portInt = 0;
        if (portText.getText().toString().length() > 0){
            portInt = Integer.parseInt(portText.getText().toString());
        }
        JsonSocket jsonSocket = new JsonSocket(hostString, portInt, CONNECTION_TIMEOUT);
        Log.d("connection", "Created JsonSocket object");

        psServer = new PhilosopherStoneServer(jsonSocket);
        Log.d("connection", "Created PhilosopherStoneServer");

        LoginRequest request = new LoginRequest();
        request.password = passwordText.getText().toString();
        request.username = usernameText.getText().toString();
        Log.d("connection","Login request created: " + request.toString());

        new LoginTask().execute(request);

    }

    public void signupPlayer(View view) {
        String hostString = hostText.getText().toString();
        int portInt = 0;
        if (portText.getText().toString().length() > 0){
            portInt = Integer.parseInt(portText.getText().toString());
        }
        JsonSocket jsonSocket = new JsonSocket(hostString, portInt, CONNECTION_TIMEOUT);
        Log.d("connection", "Created JsonSocket object");

        psServer = new PhilosopherStoneServer(jsonSocket);
        Log.d("connection", "Created PhilosopherStoneServer");

        SignupRequest request = new SignupRequest();
        request.password = passwordText.getText().toString();
        request.username = usernameText.getText().toString();
        Log.d("connection","Signup request created: " + request.toString());

        new SignupTask().execute(request);
    }

    private class LoginTask extends AsyncTask<LoginRequest, Void, LoginResponse>{

        ResponseFailException failException = null;

        @Override
        protected LoginResponse doInBackground(LoginRequest... requests) {
            LoginResponse response = null;
            try {
                response = psServer.send(requests[0]);
                Log.d("connection","Login response created: " + response.toString());
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","Login fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","Login error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(LoginResponse response){

            if (response != null) {

            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }

    private class SignupTask extends AsyncTask<SignupRequest, Void, SignupResponse>{

        ResponseFailException failException = null;

        @Override
        protected SignupResponse doInBackground(SignupRequest... requests) {
            SignupResponse response = null;
            try {
                response = psServer.send(requests[0]);
                Log.d("connection","Signup response created: " + response.toString());
            } catch (ResponseFailException e) {
                failException = e;
                Log.d("connection","Signup fail: " + e.getMessage());
            } catch (ResponseErrorException e) {
                Log.e("connection","Signup error");
            }

            return response;
        }

        @Override
        protected void onPostExecute(SignupResponse response){

            if (response != null) {

            } else if (failException != null) {
                Toast.makeText(getApplicationContext(), failException.getMessage(), Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(getApplicationContext(), PhilosopherStoneServer.ERROR_MESSAGE, Toast.LENGTH_LONG).show();
            }

        }
    }

}
