package com.example.yyz.nswbnb_android;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import java.util.Timer;
import java.util.TimerTask;

public class BookSuccess extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_book_success);
        Timer timer = new Timer();
        TimerTask timerTask = new TimerTask() {
            @Override
            public void run() {
                Intent intent = new Intent(BookSuccess.this,MainActivity.class);
                startActivity(intent);
                BookSuccess.this.finish();
            }
        };
        timer.schedule(timerTask,1000*3);
    }
}
