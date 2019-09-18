package com.example.yyz.nswbnb_android;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.example.yyz.nswbnb_android.Adapter.MyOrderAdapter;
import com.example.yyz.nswbnb_android.BaseBean.MsgBean;
import com.example.yyz.nswbnb_android.BaseBean.OrderBean;
import com.google.gson.Gson;
import com.wang.avi.AVLoadingIndicatorView;

import org.xutils.common.Callback;
import org.xutils.http.RequestParams;
import org.xutils.x;

import java.io.IOException;
import java.util.PriorityQueue;

import es.dmoral.toasty.Toasty;
import okhttp3.Call;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class Fragment4 extends Fragment {
    private TextView order_message;
    private RecyclerView order_result;
    private SharedPreferences sharedPreferences;
    private MyOrderAdapter myOrderAdapter;
    private LinearLayoutManager linearLayoutManager;
    private AVLoadingIndicatorView avi;
    private Button refresh;
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment4, container, false);

        order_message = view.findViewById(R.id.order_message);
        order_result = view.findViewById(R.id.order_result);
        refresh = view.findViewById(R.id.refresh);
        linearLayoutManager = new LinearLayoutManager(getContext());
        avi = view.findViewById(R.id.order_avi);
        avi.setVisibility(View.VISIBLE);
        avi.show();

        order_result.setLayoutManager(linearLayoutManager);
        getReservation();
        refresh.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                getReservation();
            }
        });
        return view;
    }

    private void getReservation() {
        sharedPreferences = getActivity().getSharedPreferences("USERINFO", Activity.MODE_PRIVATE);
        String token =sharedPreferences.getString("token","");

        String url="http://nswbnb.herokuapp.com/api/reservation";
        RequestParams params = new RequestParams(url);
        params.addQueryStringParameter("filter", "future");
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
                avi.hide();
                avi.setVisibility(View.GONE);
                if (!hasError && result != null)  {

                    final OrderBean orderBean = new Gson().fromJson(result, OrderBean.class);
                    Log.e("successmsg",orderBean.getMsg().get(0).getAccommodation_name());
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {

                            myOrderAdapter = new MyOrderAdapter(getActivity(), orderBean.getMsg());
                            order_result.setAdapter(myOrderAdapter);

                        }
                    });
                    myOrderAdapter.notifyDataSetChanged();

                } else {
                    order_message.setVisibility(View.VISIBLE);
                    final MsgBean msgBean = new Gson().fromJson(result,MsgBean.class);
                    Log.e("fail",msgBean.getMsg());
                    SharedPreferences sharedPreferences = getActivity().getSharedPreferences("USERINFO", Activity.MODE_PRIVATE);
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


}
