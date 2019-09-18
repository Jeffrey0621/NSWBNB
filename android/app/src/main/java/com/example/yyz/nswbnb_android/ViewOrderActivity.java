package com.example.yyz.nswbnb_android;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.example.yyz.nswbnb_android.Adapter.PastOrderAdapter;
import com.example.yyz.nswbnb_android.BaseBean.MsgBean;
import com.example.yyz.nswbnb_android.BaseBean.OrderBean;
import com.google.gson.Gson;
import com.wang.avi.AVLoadingIndicatorView;

import org.xutils.common.Callback;
import org.xutils.http.RequestParams;
import org.xutils.x;

public class ViewOrderActivity extends AppCompatActivity {
    private TextView order_message;
    private RecyclerView order_result;
    private SharedPreferences sharedPreferences;
    private PastOrderAdapter myOrderAdapter;
    private LinearLayoutManager linearLayoutManager;
    private AVLoadingIndicatorView avi;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_order);

        order_message = findViewById(R.id.past_order_message);
        order_result = findViewById(R.id.past_order_result);
        linearLayoutManager = new LinearLayoutManager(ViewOrderActivity.this);
        avi = findViewById(R.id.past_order_avi);
        avi.setVisibility(View.VISIBLE);
        avi.show();
        initToolBar();
        order_result.setLayoutManager(linearLayoutManager);
        sharedPreferences = ViewOrderActivity.this.getSharedPreferences("USERINFO", Activity.MODE_PRIVATE);
        String token =sharedPreferences.getString("token","");

        String url="http://nswbnb.herokuapp.com/api/reservation";
        RequestParams params = new RequestParams(url);
        params.addQueryStringParameter("filter", "past");
        params.addQueryStringParameter("token", token);

        x.http().get(params, new Callback.CacheCallback<String>() {
            private boolean hasError = false;
            private String result = null;
            @Override
            public void onSuccess(String result) {
                if (result != null) {
                    this.result = result;
                }
            }

            @Override
            public void onError(Throwable ex, boolean isOnCallback) {
                order_message.setVisibility(View.VISIBLE);
            }

            @Override
            public void onCancelled(CancelledException cex) {

            }

            @Override
            public void onFinished() {
                if (!hasError && result != null)  {
                    if(result.length() == 0){
                        order_message.setVisibility(View.VISIBLE);
                    }
                    final OrderBean orderBean = new Gson().fromJson(result, OrderBean.class);
                    ViewOrderActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {

                            myOrderAdapter = new PastOrderAdapter(ViewOrderActivity.this, orderBean.getMsg());
                            order_result.setAdapter(myOrderAdapter);
                            avi.hide();
                            avi.setVisibility(View.GONE);
                        }
                    });
                    myOrderAdapter.notifyDataSetChanged();

                } else {
                    order_message.setVisibility(View.VISIBLE);
                    final MsgBean msgBean = new Gson().fromJson(result,MsgBean.class);
                    Log.e("fail",msgBean.getMsg());
                    SharedPreferences sharedPreferences = ViewOrderActivity.this.getSharedPreferences("USERINFO", Activity.MODE_PRIVATE);
                    sharedPreferences.edit().clear();
                }
            }

            @Override
            public boolean onCache(String result) {
                this.result = result;
                return true;
            }
        });
    }
    private void initToolBar() {
        Toolbar toolbar = findViewById(R.id.view_order_toolbar);
        toolbar.setTitle("Past trips");
        toolbar.setTitleTextColor(Color.BLACK);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }

}
