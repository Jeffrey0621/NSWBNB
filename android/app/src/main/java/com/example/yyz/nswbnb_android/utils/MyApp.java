package com.example.yyz.nswbnb_android.utils;


import android.app.Application;

import org.xutils.x;

public class MyApp extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        x.Ext.init(this);
        x.Ext.setDebug(false);
    }
}

