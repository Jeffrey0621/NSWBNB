package com.example.yyz.nswbnb_android;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.Button;

public class MyProperty extends AppCompatActivity {
    private Button add_property;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_property);
        add_property = findViewById(R.id.add_property);
        add_property.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MyProperty.this, AddPropertyActivity.class);
                startActivity(intent);
            }
        });
        initToolBar();
    }
    private void initToolBar() {
        Toolbar toolbar = findViewById(R.id.my_property_toolbar);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }

}
