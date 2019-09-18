package com.example.yyz.nswbnb_android;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;


import com.example.yyz.nswbnb_android.BaseBean.MsgBean;
import com.google.gson.Gson;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class BookDetailActivity extends AppCompatActivity {
    private int acc_id;
    public String name,startdate,enddate;
    public int  num_guests;
    public String suburb;
    public int price;
    private TextView book_name,book_location,book_guests,book_checkin,book_checkout,book_price,book_day,book_total,book_total_price;
    private Button pay;
    private SharedPreferences sharedPreferences;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_book_detail);
        initView();
        initdata();
        initToolBar();
        sharedPreferences = this.getSharedPreferences("USERINFO", Activity.MODE_PRIVATE);
        pay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String token =sharedPreferences.getString("token","");
                final int userid = sharedPreferences.getInt("userid",0);
                OkHttpClient okHttpClient = new OkHttpClient();
                FormBody.Builder formbody = new FormBody.Builder();
                formbody.add("token", token);
                formbody.add("guest_id", String.valueOf(userid));
                formbody.add("accommodation_id", String.valueOf(acc_id));
                formbody.add("num_guests", String.valueOf(num_guests));
                formbody.add("check_in", startdate);
                formbody.add("check_out", enddate);
                final Request request = new Request.Builder()
                        .url("http://nswbnb.herokuapp.com/api/reservation")
                        .post(formbody.build())
                        .build();
                okHttpClient.newCall(request).enqueue(new Callback() {
                    @Override
                    public void onFailure(Call call, IOException e) {
                        Log.e("onfail:", e.toString());
                    }

                    @Override
                    public void onResponse(Call call, Response response) throws IOException {
                        if(response.code() == 201){
                            Intent intent = new Intent(BookDetailActivity.this,BookSuccess.class);
                            startActivity(intent);
                        }else {
                            String res = response.body().string();
                            final MsgBean msgBean = new Gson().fromJson(res, MsgBean.class);
                            BookDetailActivity.this.runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    Log.e("fail",msgBean.getMsg());
                                    Toast.makeText(BookDetailActivity.this,msgBean.getMsg(),Toast.LENGTH_SHORT).show();
                                }
                            });

                        }
                    }
                });

            }
        });
    }

    private void initToolBar() {
        Toolbar toolbar = findViewById(R.id.book_detail_toolbar);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }

    private void initView() {
        book_name = findViewById(R.id.book_name);

        book_location = findViewById(R.id.book_location);

        book_guests =findViewById(R.id.book_guests);

        book_checkin = findViewById(R.id.book_checkin);
        book_checkout = findViewById(R.id.book_checkout);
        book_price = findViewById(R.id.book_price);
        book_day = findViewById(R.id.book_day);
        book_total = findViewById(R.id.book_total);
        book_total_price = findViewById(R.id.book_total_price);
        pay = findViewById(R.id.pay);
    }

    private void initdata() {
        Intent intent = getIntent();
        Bundle b = intent.getExtras();
        acc_id = b.getInt("accid");
        name = b.getString("name");
        num_guests = b.getInt("num_guests");
        suburb = b.getString("suburb");
        price = b.getInt("price")/100;
        startdate = b.getString("startdate");
        enddate = b.getString("enddate");

        book_name.setText(name);
        book_location.setText(suburb);
        book_guests.setText("At most "+String.valueOf(num_guests)+"guest(s)");
        book_checkin.setText(startdate);
        book_checkout.setText(enddate);
        book_price.setText("$"+String.valueOf(price)+"/night");
        SimpleDateFormat f = new SimpleDateFormat("yyyy-mm-dd");
        Date start = null;
        Date end = null;
        try{
            start = f.parse(startdate);
            end = f.parse(enddate);
        }catch (ParseException e){
            e.printStackTrace();
        }
        int day = (int) ((end.getTime()-start.getTime())/(24*60*60*1000));
        book_day.setText(String.valueOf(day)+"day(s)");
        book_total.setText("$"+String.valueOf(price*day));
        book_total_price.setText("$"+String.valueOf(price*day));

    }
}
