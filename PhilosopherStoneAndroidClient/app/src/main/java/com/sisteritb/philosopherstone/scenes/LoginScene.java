package com.sisteritb.philosopherstone.scenes;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

import com.sisteritb.philosopherstone.R;

public class LoginScene extends Activity {
    private EditText usernameText, passwordText, portText, hostText;

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

    }

    public void signupPlayer(View view) {

    }

}
