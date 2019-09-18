package com.example.yyz.nswbnb_android;

import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.design.button.MaterialButton;
import android.support.v4.app.Fragment;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import android.widget.TextView;
import android.widget.Toast;


import com.archit.calendardaterangepicker.customviews.DateRangeCalendarView;
import com.bumptech.glide.Glide;
import com.example.yyz.nswbnb_android.utils.SelfDialog;
import com.youth.banner.Banner;
import com.youth.banner.BannerConfig;
import com.youth.banner.Transformer;
import com.youth.banner.listener.OnBannerListener;
import com.youth.banner.loader.ImageLoader;

import org.angmarch.views.NiceSpinner;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.LinkedList;
import java.util.List;

import es.dmoral.toasty.Toasty;


public class Fragment1 extends Fragment implements OnBannerListener {

    private Banner banner;
    private ArrayList<String> list_path;
    private ArrayList<String> list_title;
    private EditText editText;
    private NiceSpinner guestspinner;
    Dialog dialog;
    private Button checkdate,show;
    private String startdate,enddate;
    private RecyclerView recyclerView;
    private ArrayList<String> mDatas = new ArrayList<>();

    private List<Integer> numguest;
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment1, container, false);
        banner = (Banner) view.findViewById(R.id.banner);
        editText = (EditText) view.findViewById(R.id.location);
        guestspinner = view.findViewById(R.id.guestnumber);
        numguest = new LinkedList<>(Arrays.asList(1,2,3,4,5,6));
        guestspinner.attachDataSource(numguest);


        checkdate = view.findViewById(R.id.checkdate);
        //collection of pictures
        list_path = new ArrayList<>();
        //collection of titles
        list_title = new ArrayList<>();

        list_path.add("https://voith.com/aus-en/1280x300_sydney-opera-house.png");
        list_path.add("http://australiatravels.net/images/inner_banner11.jpg");
        list_path.add("https://promolover.com/media/t/3VSGDZg-iVhF_1280x300_Xe3lowe7.jpg");
        list_path.add("http://dingyue.nosdn.127.net/2yibhtfaEh0H7L8qIkVpYxTghx3vQT7pvgGv6TR3djUJh1524792141605.jpg");
        list_title.add("1");
        list_title.add("2");
        list_title.add("3");
        list_title.add("4");
        //Setting built-in styles
        banner.setBannerStyle(BannerConfig.CIRCLE_INDICATOR_TITLE_INSIDE);
        //Set up the image loader
        banner.setImageLoader(new MyLoader());
        //image url
        banner.setImages(list_path);
        //Set the animation effect of the rotation
        banner.setBannerAnimation(Transformer.Default);
        //title
        banner.setBannerTitles(list_title);
        //delay time
        banner.setDelayTime(3000);

        banner.isAutoPlay(true);
        //Set the position of the indicator
        banner.setIndicatorGravity(BannerConfig.CENTER)
                .setOnBannerListener(this)
                //start
                .start();
        checkdate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showdialog();
            }
        });
        show= view.findViewById(R.id.searchresult);
        show.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Log.e("aaa",startdate+enddate);
                Log.e("bbb",checkdate.getText().toString());
                if(editText.getText().toString()=="" ||startdate==null||enddate==null){
                    Toasty.info(getContext(),"Something missing",Toasty.LENGTH_SHORT,true).show();
                }else {
                    Intent intent = new Intent(getActivity(), SearchResult.class);
                    Bundle bundle = new Bundle();
                    bundle.putString("location", editText.getText().toString());
                    bundle.putString("startdate", startdate);
                    bundle.putString("enddate", enddate);
                    bundle.putInt("guestnumber", guestspinner.getSelectedIndex());
                    intent.putExtras(bundle);
                    startActivity(intent);
                }
            }
        });
        return view;
    }

    private void showdialog() {
        View view=View.inflate(getActivity(),R.layout.dialog_layout,null);
        dialog = new SelfDialog(getActivity(), 300, 400, view, R.style.dialog);
        dialog.show();
        final Button save = (Button) view.findViewById(R.id.save);
        final DateRangeCalendarView dateView = view.findViewById(R.id.calendar);
        dateView.setCalendarListener(new DateRangeCalendarView.CalendarListener() {
            @Override
            public void onFirstDateSelected(Calendar startDate) {
            }
            @Override
            public void onDateRangeSelected(Calendar startDate, Calendar endDate) {
                SimpleDateFormat formater = new SimpleDateFormat("yyyy-MM-dd");
                startdate = formater.format(startDate.getTime());
                enddate = formater.format(endDate.getTime());
            }
        });
        save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(startdate != null&&enddate!=null) {
                    checkdate.setText(startdate + '-' + enddate);
                }
                dialog.dismiss();
            }
        });
    }

    //The monitoring method of rotation chart
    @Override
    public void OnBannerClick(int position) {
      //  Log.i("tag", "this is "+position+"viewpager");
    }
    //ImageLoader
    private class MyLoader extends ImageLoader {
        @Override
        public void displayImage(Context context, Object path, ImageView imageView) {
            Glide.with(context).load((String) path).into(imageView);
        }
    }
}