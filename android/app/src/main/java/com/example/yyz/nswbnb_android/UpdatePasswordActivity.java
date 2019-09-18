package com.example.yyz.nswbnb_android;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.IOException;

import es.dmoral.toasty.Toasty;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class UpdatePasswordActivity extends AppCompatActivity {
    private EditText user_old_password,user_new_password,user_confirm_password;
    private Button user_password_update;
    private SharedPreferences sharedPreferences;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_update_password);
        user_old_password = findViewById(R.id.user_old_password);
        user_new_password = findViewById(R.id.user_new_password);
        user_confirm_password = findViewById(R.id.user_confirm_password);
        user_password_update = findViewById(R.id.user_password_update);
        sharedPreferences = this.getSharedPreferences("USERINFO", Activity.MODE_PRIVATE);
        initToolBar();
        user_password_update.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(user_old_password.getText().toString() == "" || user_new_password.getText().toString() == "" || user_confirm_password.getText().toString() == ""){
                    Toasty.info(UpdatePasswordActivity.this,"Nothing can be empty",Toasty.LENGTH_SHORT).show();
                }else if(!user_new_password.getText().toString().equals(user_confirm_password.getText().toString())){
                    Toasty.info(UpdatePasswordActivity.this,"New password and confirm password are different.",Toasty.LENGTH_SHORT).show();
                }else{
                    String token =sharedPreferences.getString("token","");
                    OkHttpClient okHttpClient = new OkHttpClient();
                    FormBody.Builder formbody = new FormBody.Builder();
                    formbody.add("old_password", user_old_password.getText().toString());
                    formbody.add("new_password", user_new_password.getText().toString());
                    formbody.add("token", token);
                    Request request = new Request.Builder()
                            .url("http://nswbnb.herokuapp.com/api/user/password")
                            .put(formbody.build())
                            .build();
                    okHttpClient.newCall(request).enqueue(new Callback() {
                        @Override
                        public void onFailure(Call call, IOException e) {
                            Log.e("onfail:", e.toString());
                        }

                        @Override
                        public void onResponse(Call call, Response response) throws IOException {
                            int statuscode = response.code();
                            if(statuscode == 200){
                                UpdatePasswordActivity.this.runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        Toasty.info(UpdatePasswordActivity.this,"Update successfully", Toast.LENGTH_SHORT, true).show();
                                        Intent intent = new Intent(UpdatePasswordActivity.this,MainActivity.class);
                                        startActivity(intent);
                                    }
                                });

                            }else{
                                UpdatePasswordActivity.this.runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        Toasty.error(UpdatePasswordActivity.this,"Update failed", Toast.LENGTH_SHORT, true).show();
                                    }
                                });

                            }
                        }
                    });
                }
            }
        });
    }
    private void initToolBar() {
        Toolbar toolbar = findViewById(R.id.update_password_toolbar);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }

}
