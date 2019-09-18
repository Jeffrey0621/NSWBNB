package com.example.yyz.nswbnb_android.utils;


import android.app.Dialog;
import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;

import org.xutils.common.util.DensityUtil;

public class SelfDialog extends Dialog {
    private static int default_width = 300;

    private static int default_height = 300;



    public SelfDialog(Context context, View layout, int style) {

        this(context, default_width, default_height, layout, style);

    }



    public SelfDialog(Context context, int width, int height, View layout, int style) {

        super(context, style);

        setContentView(layout);

        Window window = getWindow();

        WindowManager.LayoutParams params = window.getAttributes();
        params.width = DensityUtil.dip2px(width);
        params.height = DensityUtil.dip2px( height);
        params.gravity = Gravity.CENTER;

        window.setAttributes(params);

    }


}
