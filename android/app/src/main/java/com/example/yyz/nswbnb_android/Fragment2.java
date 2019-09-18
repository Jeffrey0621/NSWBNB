package com.example.yyz.nswbnb_android;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

public class Fragment2 extends Fragment {
    private LinearLayout prepage;
    private boolean isLogin;
    private TextView textshow;
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        isLogin = ((MainActivity)getActivity()).isLogin();

        View view = inflater.inflate(R.layout.fragment2, container, false);
        prepage = view.findViewById(R.id.prepage);
        textshow = view.findViewById(R.id.textshow);

        return view;
    }


}
