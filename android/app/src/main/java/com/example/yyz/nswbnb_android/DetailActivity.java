package com.example.yyz.nswbnb_android;

import android.app.Activity;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Display;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;


import com.archit.calendardaterangepicker.customviews.DateRangeCalendarView;
import com.bumptech.glide.Glide;
import com.example.yyz.nswbnb_android.BaseBean.ErrorBean;
import com.example.yyz.nswbnb_android.BaseBean.UserBean;
import com.example.yyz.nswbnb_android.utils.SelfDialog;
import com.google.gson.Gson;
import com.youth.banner.Banner;
import com.youth.banner.BannerConfig;
import com.youth.banner.Transformer;
import com.youth.banner.listener.OnBannerListener;
import com.youth.banner.loader.ImageLoader;

import org.xutils.common.util.DensityUtil;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;

import es.dmoral.toasty.Toasty;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


public class DetailActivity extends AppCompatActivity implements OnBannerListener {
    private Banner banner;
    private ArrayList<String> list_path;
    private ArrayList<String> list_title;
    private int acc_id;
    public int host_id;
    public String name;
    public int  num_guests;
    public int num_bedrooms;
    public int num_beds;
    public float num_bathrooms;
    public String description;
    public String suburb;
    public String city;
    public String state;
    public String country;
    public int price;
    public String property_type;
    public ArrayList<String> amenities;
    public ArrayList<String> image_urls;
    public float rating;
    public int num_reviews;

    private TextView detail_name,detail_location,detail_guests,detail_bedroom,detail_bed,detail_bathroom,detail_description,detail_price,detail_check;
    private TextView amenties1,amenties2,amenties3,amenties4,amenties5,amenties6,more_detail;
    private Button detail_book_btn;
    private  String startdate,enddate;
    private Dialog dialog,dialog_login;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);
        initView();
        initdata();
        initBanner();
        adaptdata();
        initToolBar();
        detail_book_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                SharedPreferences sharedPreferences = DetailActivity.this.getSharedPreferences("USERINFO", Activity.MODE_PRIVATE);
                if (sharedPreferences.getString("token", "") == "") {
                    showLogin();
                } else {
                    Intent intent = new Intent(DetailActivity.this, BookDetailActivity.class);
                    Bundle bundle = new Bundle();
                    bundle.putInt("accid", acc_id);
                    bundle.putString("name", name);
                    bundle.putInt("num_guests", num_guests);
                    bundle.putString("suburb", suburb);
                    bundle.putInt("price", price);
                    bundle.putString("startdate", startdate);
                    bundle.putString("enddate", enddate);

                    intent.putExtras(bundle);
                    startActivity(intent);
                }
            }
        });



    }



    private void initToolBar() {
        Toolbar toolbar = findViewById(R.id.detail_toolbar);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }


    private void adaptdata() {
        detail_name.setText(name);
        detail_location.setText(suburb);
        detail_guests.setText(String.valueOf(num_guests)+"guests");
        detail_bedroom.setText(String.valueOf(num_bedrooms)+"bedrooms");
        detail_bed.setText(String.valueOf(num_beds)+"beds");
        detail_bathroom.setText(String.valueOf(num_bathrooms)+"bathrooms");
        detail_description.setText(description);
        detail_price.setText("$"+String.valueOf(price/100)+"/night");
        detail_check.setText(startdate+"-"+enddate);

        amenties1.setText(amenities.get(0));
        amenties2.setText(amenities.get(1));
        amenties3.setText(amenities.get(2));
        amenties4.setText(amenities.get(3));
        amenties5.setText(amenities.get(4));
        amenties6.setText(amenities.get(5));

    }

    private void initView() {
        banner = findViewById(R.id.detailbanner);
        detail_name = findViewById(R.id.detail_name);
        detail_location = findViewById(R.id.detail_location);
        detail_guests = findViewById(R.id.detail_guests);
        detail_bedroom = findViewById(R.id.detail_bedroom);
        detail_bed = findViewById(R.id.detail_bed);
        detail_bathroom = findViewById(R.id.detail_bathroom);
        detail_description = findViewById(R.id.detail_description);
        detail_price = findViewById(R.id.detail_price);
        detail_book_btn = findViewById(R.id.detail_book_btn);
        detail_check = findViewById(R.id.detail_check);

        amenties1 = findViewById(R.id.amenties1);
        amenties2 = findViewById(R.id.amenties2);
        amenties3 = findViewById(R.id.amenties3);
        amenties4 = findViewById(R.id.amenties4);
        amenties5 = findViewById(R.id.amenties5);
        amenties6 = findViewById(R.id.amenties6);

        more_detail = findViewById(R.id.more_detail);

    }

    private void initdata() {
        Intent intent = getIntent();
        Bundle b = intent.getExtras();
        acc_id = b.getInt("accid");
        host_id = b.getInt("host_id");
        name = b.getString("name");
        num_guests = b.getInt("num_guests");
        num_bedrooms = b.getInt("num_bedrooms");
        num_beds = b.getInt("num_beds");
        num_bathrooms = b.getFloat("num_bathrooms");
        description = b.getString("description");
        suburb = b.getString("suburb");
        city = b.getString("city");
        state = b.getString("state");
        country = b.getString("country");
        price = b.getInt("price");
        property_type = b.getString("property_type");
        amenities = b.getStringArrayList("amenities");
        image_urls = b.getStringArrayList("image_urls");
        rating = b.getFloat("rating");
        num_reviews = b.getInt("num_reviews");
        startdate = b.getString("startdate");
        enddate = b.getString("enddate");

        more_detail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                moredetail();
            }
        });
    }



    private void initBanner() {
        //collection of pictures
        list_path = new ArrayList<>();
        list_title= new ArrayList<>();
        for(int i = 1;i<=image_urls.size();i++){
            list_path.add(image_urls.get(i - 1));
            list_title.add(String.valueOf(i));
        }
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
                .setOnBannerListener(DetailActivity.this)
                //start
                .start();
    }

    @Override
    public void OnBannerClick(int position) {

    }

    //ImageLoader
    private class MyLoader extends ImageLoader {
        @Override
        public void displayImage(Context context, Object path, ImageView imageView) {
            Glide.with(context).load((String) path).into(imageView);
        }
    }

    private void showdialog() {
        View view=View.inflate(DetailActivity.this,R.layout.dialog_layout,null);
        dialog = new SelfDialog(DetailActivity.this, 200, 200, view, R.style.dialog);
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
                dialog.dismiss();
            }
        });
    }

    private void moredetail() {
        View view=View.inflate(DetailActivity.this,R.layout.detail_dialog,null);
        dialog = new SelfDialog(DetailActivity.this, 300, 400, view, R.style.dialog);
        dialog.show();
        final Toolbar toolbar = view.findViewById(R.id.more_detail_dialog_toolbar);
        final TextView show_more = view.findViewById(R.id.show_more);

        show_more.setText(description);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                dialog.dismiss();
            }
        });
    }

    private void showLogin() {
        View view=View.inflate(DetailActivity.this,R.layout.dialog_login_layout,null);
        dialog_login = new SelfDialog(DetailActivity.this, 300, 300, view, R.style.dialog);
        dialog_login.show();

        final EditText detail_loginEmail = view.findViewById(R.id.detail_loginEmail);
        final EditText detail_loginpassword = view.findViewById(R.id.detail_loginpassword);
        final Button detail_login = view.findViewById(R.id.detail_login);
        final Toolbar detail_login_dialog_toolbar = view.findViewById(R.id.detail_login_dialog_toolbar);
        detail_login_dialog_toolbar.setTitle("Login");
        detail_login_dialog_toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                dialog_login.dismiss();
            }
        });
        detail_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                login(detail_loginEmail.getText().toString(),detail_loginpassword.getText().toString());
            }
        });
    }
    private void login(String email, String password) {
        if (!validate(email,password)) {
            Toasty.error(DetailActivity.this, "Log in failed.", Toast.LENGTH_SHORT, true).show();
            return;
        }
        final ProgressDialog progressDialog = new ProgressDialog(DetailActivity.this, R.style.AppTheme_Dark_Dialog);

        progressDialog.setIndeterminate(true);
        progressDialog.setMessage("Authenticating...");
        progressDialog.show();

        OkHttpClient okHttpClient = new OkHttpClient();
        FormBody.Builder formbody = new FormBody.Builder();
        formbody.add("email", email);
        formbody.add("password", password);
        Request request = new Request.Builder()
                .url("http://nswbnb.herokuapp.com/api/login")
                .post(formbody.build())
                .build();
        final String email1 = email;
        okHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e("onfail:", e.toString());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                progressDialog.dismiss();
                if (response.code() == 200) {

                    SharedPreferences sharedPreferences = DetailActivity.this.getSharedPreferences("USERINFO", Context.MODE_PRIVATE);
                    SharedPreferences.Editor editor = sharedPreferences.edit();
                    editor.putString("useremail",email1);
                    String res = response.body().string();
                    UserBean userBean = new Gson().fromJson(res, UserBean.class);
                    editor.putInt("userid",userBean.getMsg().getUser_id());
                    editor.putString("username",userBean.getMsg().getUsername());
                    editor.putString("token",userBean.getMsg().getToken());
                    System.out.println(userBean.getMsg().getToken());
                    editor.commit();
                    //System.out.println("测试" + ((MainActivity) getActivity()).isLogin());
                    DetailActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            dialog_login.dismiss();
                        }
                    });

                }

            }
        });
    }


    private boolean validate(String email,String password) {
        boolean valid = true;
        if (email.isEmpty() || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            valid = false;
        }
        if (password.isEmpty() || password.length() < 8 || password.length() > 20) {
            valid = false;
        } else {
        }
        return valid;
    }
}
