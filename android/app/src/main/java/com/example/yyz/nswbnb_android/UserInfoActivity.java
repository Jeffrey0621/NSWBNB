package com.example.yyz.nswbnb_android;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
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

import com.archit.calendardaterangepicker.customviews.DateRangeCalendarView;
import com.example.yyz.nswbnb_android.utils.SelfDialog;

import org.angmarch.views.NiceSpinner;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Calendar;
import java.util.LinkedList;
import java.util.List;

import es.dmoral.toasty.Toasty;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class UserInfoActivity extends AppCompatActivity {
    private EditText user_email,user_name,user_phone;
    private Button user_info_save;
    private NiceSpinner user_gender;
    private List<String> gender;
    private Dialog dialog;
    String birthday;
    private SharedPreferences sharedPreferences;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        final SharedPreferences sharedPreferences = UserInfoActivity.this.getSharedPreferences("USERINFO", Context.MODE_PRIVATE);

        setContentView(R.layout.activity_user_info);
        user_email = findViewById(R.id.user_email);
        user_email.setText(sharedPreferences.getString("useremail","no email"));
        user_email.setEnabled(false);
        user_name = findViewById(R.id.user_name);
        user_name.setText(sharedPreferences.getString("username","no name"));
        user_name.setEnabled(false);
        user_gender = findViewById(R.id.user_gender);
        gender = new LinkedList<>(Arrays.asList("gender","Male", "Female"));
        user_gender.attachDataSource(gender);
        user_phone = findViewById(R.id.user_phone);
        user_info_save = findViewById(R.id.user_info_save);
        initToolBar();

        user_info_save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                System.out.println(String.valueOf(user_gender.getSelectedIndex()));;
                System.out.println(user_phone.getText().toString());
                if(user_gender.getSelectedIndex() == 0 && birthday == null ){
                    Toasty.info(UserInfoActivity.this,"Nothing change",Toasty.LENGTH_SHORT).show();
                }else{
                    String token =sharedPreferences.getString("token","");
                    OkHttpClient okHttpClient = new OkHttpClient();
                    FormBody.Builder formbody = new FormBody.Builder();
                    formbody.add("gender", user_gender.getItemAtPosition(user_gender.getSelectedIndex()).toString());
                    formbody.add("phone", user_phone.getText().toString());
                    formbody.add("token", token);
                    Request request = new Request.Builder()
                            .url("http://nswbnb.herokuapp.com/api/user")
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
                                UserInfoActivity.this.runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        Toasty.info(UserInfoActivity.this,"Update successfully", Toast.LENGTH_SHORT, true).show();
                                        Intent intent = new Intent(UserInfoActivity.this,MainActivity.class);
                                        startActivity(intent);
                                    }
                                });
                            }else{
                                UserInfoActivity.this.runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        Toasty.error(UserInfoActivity.this,"Update failed", Toast.LENGTH_SHORT, true).show();
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
        Toolbar toolbar = findViewById(R.id.user_info_toolbar);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }
}
