package com.example.yyz.nswbnb_android;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class Fragment5 extends Fragment {
    private LinearLayout personalinfopage, userinfo_line, password_line, order_line, add_property_line, logout_line;
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment5, container, false);

        personalinfopage = view.findViewById(R.id.personalinfopage);
        userinfo_line = view.findViewById(R.id.userinfo_line);
        password_line = view.findViewById(R.id.password_line);
        order_line = view.findViewById(R.id.order_line);
        add_property_line = view.findViewById(R.id.add_property_line);
        logout_line = view.findViewById(R.id.logout_line);

        clickfunction();
        return view;
    }

    private void clickfunction() {
        logout_line.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final ProgressDialog progressDialog = new ProgressDialog(getActivity(), R.style.AppTheme_Dark_Dialog);
                progressDialog.setIndeterminate(true);
                progressDialog.setMessage("Log out...");

                SharedPreferences sharedPreferences = getActivity().getSharedPreferences("USERINFO", Context.MODE_PRIVATE);
                final SharedPreferences.Editor editor = sharedPreferences.edit();

                OkHttpClient okHttpClient = new OkHttpClient();
                FormBody.Builder formbody = new FormBody.Builder();
                formbody.add("token", sharedPreferences.getString("token","").toString());
                editor.clear().commit();
                Request request = new Request.Builder()
                        .url("http://nswbnb.herokuapp.com/api/logout")
                        .post(formbody.build())
                        .build();
                okHttpClient.newCall(request).enqueue(new Callback() {
                    @Override
                    public void onFailure(Call call, IOException e) {
                        Log.e("fail",e.toString());
                    }

                    @Override
                    public void onResponse(Call call, Response response) throws IOException {

                            getActivity().runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    progressDialog.show();
                                    new android.os.Handler().postDelayed(
                                            new Runnable() {
                                                public void run() {
                                /*FragmentManager manger = getFragmentManager();
                                FragmentTransaction fragmentTransaction = manger.beginTransaction();
                                Fragment fragment2 = new Fragment2();
                                fragmentTransaction.replace(R.id.fragment2, fragment2);
                                fragmentTransaction.commit();*/
                                                    progressDialog.dismiss();
                                                    Intent intent = new Intent(getContext(),MainActivity.class);
                                                    startActivity(intent);
                                                }
                                            }, 2000);
                                }
                            });

                    }
                });

            }
        });

        userinfo_line.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getActivity(), UserInfoActivity.class);
                startActivity(intent);
            }
        });

        password_line.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getActivity(), UpdatePasswordActivity.class);
                startActivity(intent);
            }
        });

        order_line.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getActivity(), ViewOrderActivity.class);
                startActivity(intent);
            }
        });

        add_property_line.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getActivity(), MyProperty.class);
                startActivity(intent);
            }
        });
    }


}
