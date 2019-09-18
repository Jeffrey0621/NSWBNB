package com.example.yyz.nswbnb_android;

import android.app.Activity;
import android.content.Context;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Toast;


import com.donkingliang.imageselector.utils.ImageSelector;
import com.donkingliang.imageselector.utils.ImageSelectorUtils;
import com.example.yyz.nswbnb_android.BaseBean.UpLoadImageBean;
import com.google.gson.Gson;
import com.wang.avi.AVLoadingIndicatorView;

import org.angmarch.views.NiceSpinner;
import org.angmarch.views.OnSpinnerItemSelectedListener;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

import es.dmoral.toasty.Toasty;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class AddPropertyActivity extends AppCompatActivity {
    private EditText property_name, property_price, property_description, property_amenities;
    private Button property_save, property_upload;
    private NiceSpinner property_guest_number, property_bedroom_number, property_bed_number, property_bathroom_number,
            property_type, property_city, property_country, property_suburb;
    private List<String> numguest, numbed, numbedroom, numbathroom;
    private List<String> proptype;
    private static final int REQUEST_CODE = 0x00000011;
    private ArrayList<String> imagesurl = new ArrayList<>();
    private AVLoadingIndicatorView avi;
    private ArrayList<String> country = new ArrayList<>();

    private ArrayList<String> city = new ArrayList<>();

    private ArrayList<ArrayList<String>> suburb = new ArrayList<>();
    private ArrayList<String> suburb1 = new ArrayList<>();
    private ArrayList<String> suburb2 = new ArrayList<>();

    private LinearLayout checklist;
    private List<CheckBox> checkBoxList = new ArrayList<CheckBox>();
    private ArrayList<String> selected;
    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_property);
        initView();
        intiData();
        checkFunction();
        initToolBar();
        property_save.setEnabled(false);
        property_upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                ImageSelector.builder()
                        .useCamera(true)
                        .setSingle(false)
                        .setMaxSelectCount(5)
                        .setSelected(selected)
                        .setViewImage(true) //Click to enlarge the image
                        .start(AddPropertyActivity.this, REQUEST_CODE);
            }
        });

        property_save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String checkstr = "";
                for (CheckBox checkBox : checkBoxList) {
                    if (checkBox.isChecked()) {
                        checkstr += checkBox.getText().toString() + ",";
                    }
                }
                if(checkstr == ""||property_name.getText().toString() == "" || property_guest_number.getSelectedItem().toString() == "number of guests" ||
                        property_bed_number.getSelectedItem().toString() == "number of beds" || property_bedroom_number.getSelectedItem().toString() == "number of bedrooms"||
                        property_bathroom_number.getSelectedItem().toString() == "number of bathrooms" || property_type.getSelectedItem().toString() == "" ||
                        property_country.getSelectedIndex() == 0 || property_city.getSelectedIndex() == 0  ||
                        property_suburb.getSelectedIndex() == 0  ||
                        property_price.getText().toString() == "" || property_description.getText().toString() == "" || imagesurl.size() != 5){
                    Toasty.error(AddPropertyActivity.this, "All information are needed.", Toast.LENGTH_SHORT, true).show();
                }else {
                    String finalurls = imagesurl.get(0);
                    for (int i = 1; i < imagesurl.size(); i++) {
                        finalurls = finalurls + "," + imagesurl.get(i);
                    }
                    SharedPreferences sharedPreferences = AddPropertyActivity.this.getSharedPreferences("USERINFO", Activity.MODE_PRIVATE);
                    int userid = sharedPreferences.getInt("userid",0);

                    OkHttpClient okHttpClient = new OkHttpClient();
                    FormBody.Builder formbody = new FormBody.Builder();
                    String token =sharedPreferences.getString("token","");
                    formbody.add("host_id", String.valueOf(userid));
                    formbody.add("name", property_name.getText().toString());
                    formbody.add("num_guests", property_guest_number.getSelectedItem().toString());
                    formbody.add("num_bedrooms", property_bedroom_number.getSelectedItem().toString());
                    formbody.add("num_beds", property_bed_number.getSelectedItem().toString());
                    formbody.add("num_bathrooms", property_bathroom_number.getSelectedItem().toString());
                    formbody.add("property_type", property_type.getSelectedItem().toString());
                    formbody.add("country", property_country.getSelectedItem().toString());
                    formbody.add("city", property_city.getSelectedItem().toString());
                    formbody.add("suburb", property_suburb.getSelectedItem().toString());
                    formbody.add("price", String.valueOf((Integer.valueOf(property_price.getText().toString())*100)));
                    formbody.add("description", property_description.getText().toString());
                    formbody.add("amenities", checkstr.substring(0, checkstr.length() - 1));
                    formbody.add("image_urls", finalurls);
                    formbody.add("token", token);

                    Request request = new Request.Builder()
                            .url("http://nswbnb.herokuapp.com/api/accommodation")
                            .post(formbody.build())
                            .build();
                    okHttpClient.newCall(request).enqueue(new Callback() {
                        @Override
                        public void onFailure(Call call, IOException e) {
                            Toasty.error(AddPropertyActivity.this, e.toString(), Toast.LENGTH_SHORT, true).show();
                        }

                        @Override
                        public void onResponse(Call call, Response response) throws IOException {
                            if(response.code() == 201){
                                AddPropertyActivity.this.runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        Toasty.success(AddPropertyActivity.this, "Add successfully", Toast.LENGTH_SHORT, true).show();
                                        Intent intent = new Intent(AddPropertyActivity.this,MainActivity.class);
                                        startActivity(intent);
                                    }
                                });

                            }
                        }
                    });

                }
            }
        });
    }

    private void initToolBar() {
        Toolbar toolbar = findViewById(R.id.add_property_toolbar);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        selected = data.getStringArrayListExtra(ImageSelector.SELECT_RESULT);
        if (requestCode == REQUEST_CODE && data != null&&selected.size()==5) {
            ArrayList<String> images = data.getStringArrayListExtra(
                    ImageSelectorUtils.SELECT_RESULT);
            boolean isCameraImage = data.getBooleanExtra(ImageSelector.IS_CAMERA_IMAGE, false);
            property_upload.setVisibility(View.GONE);
            try {
                for (int i = 0; i < images.size(); i++) {
                    avi.show();
                    avi.setVisibility(View.VISIBLE);
                    uploadImage(images.get(i));
                }

            } catch (IOException e) {
                e.printStackTrace();
            }
        }else {
            AddPropertyActivity.this.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    Toasty.error(AddPropertyActivity.this, "At least 5 pictures.", Toast.LENGTH_SHORT, true).show();
                }
            });

        }
    }


    public String uploadImage(String imagePath) throws IOException {

        final OkHttpClient okHttpClient = new OkHttpClient();
        File file = new File(imagePath);
        final RequestBody image = RequestBody.create(MediaType.parse("image/jpg"), file);
        RequestBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", imagePath, image)
                .build();
        Request request = new Request.Builder()
                .url("https://imgurl.org/api/upload")
                .post(requestBody)
                .build();
        final UpLoadImageBean upLoadImageBean;
        okHttpClient.newCall(request).enqueue(new Callback() {

            @Override
            public void onFailure(Call call, IOException e) {
                Log.e("fail", e.toString());
                AddPropertyActivity.this.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        avi.hide();
                        avi.setVisibility(View.GONE);
                        property_upload.setText("Upload failed,upload again.");
                        imagesurl.clear();
                        property_upload.setVisibility(View.VISIBLE);
                    }
                });
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {

                String n = response.body().string();
                UpLoadImageBean upLoadImageBean = new Gson().fromJson(n, UpLoadImageBean.class);
                imagesurl.add(upLoadImageBean.getUrl());
                Log.e("success", String.valueOf(upLoadImageBean.getUrl()));

                if (imagesurl.size() == 5) {
                    AddPropertyActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            property_save.setEnabled(true);
                            avi.hide();
                            avi.setVisibility(View.GONE);

                        }
                    });

                }
            }
        });
        return "url";

    }


    private void initView() {
        property_name = findViewById(R.id.property_name);
        property_guest_number = findViewById(R.id.property_guest_number);
        property_bedroom_number = findViewById(R.id.property_bedroom_number);
        property_bed_number = findViewById(R.id.property_bed_number);
        property_bathroom_number = findViewById(R.id.property_bathroom_number);
        property_type = findViewById(R.id.property_type);
        property_price = findViewById(R.id.property_price);
        property_description = findViewById(R.id.property_description);

        property_save = findViewById(R.id.property_save);
        property_upload = findViewById(R.id.property_upload);
        avi = findViewById(R.id.avi);
        property_country = findViewById(R.id.property_country);
        property_city = findViewById(R.id.property_city);
        property_suburb = findViewById(R.id.property_suburb);

        checklist = findViewById(R.id.checklist);
    }

    private void intiData() {
        country.add("Australia");
        country.add("Australia");

        city.add("Sydney");
        city.add("Randwick");

        suburb1.add("city");
        suburb1.add("test");
        suburb2.add("Zetland");
        suburb2.add("Kingsford");
        suburb2.add("Surry Hills");
        suburb.add(suburb1);
        suburb.add(suburb2);

        numguest = new LinkedList<>(Arrays.asList("number of guests","1", "2", "3", "4", "5", "6"));
        property_guest_number.setTag("number of guests");
        property_guest_number.attachDataSource(numguest);
        numbed = new LinkedList<>(Arrays.asList("number of beds","1", "2", "3"));
        property_bed_number.attachDataSource(numbed);
        numbedroom = new LinkedList<>(Arrays.asList("number of bedrooms","1", "2", "3"));
        property_bedroom_number.attachDataSource(numbedroom);
        numbathroom = new LinkedList<>(Arrays.asList("number of bathrooms","1", "2", "3"));
        property_bathroom_number.attachDataSource(numbathroom);
        proptype = new LinkedList<>(Arrays.asList("Apartment", "unit", "house"));
        property_type.attachDataSource(proptype);

        property_country.attachDataSource(country);
        property_city.attachDataSource(city);
        property_suburb.attachDataSource(suburb.get(0));

        property_country.setOnSpinnerItemSelectedListener(new OnSpinnerItemSelectedListener() {
            @Override
            public void onItemSelected(NiceSpinner parent, View view, int position, long id) {
                String a = property_country.getItemAtPosition(position).toString();
                Log.e("country", a);
            }
        });


        property_city.setOnSpinnerItemSelectedListener(new OnSpinnerItemSelectedListener() {
            @Override
            public void onItemSelected(NiceSpinner parent, View view, int position, long id) {
                property_suburb.attachDataSource(suburb.get(position));
                String b = property_city.getItemAtPosition(position).toString();
                Log.e("city", b);
            }
        });
        property_suburb.setOnSpinnerItemSelectedListener(new OnSpinnerItemSelectedListener() {
            @Override
            public void onItemSelected(NiceSpinner parent, View view, int position, long id) {
                String c = property_suburb.getItemAtPosition(position).toString();
                Log.e("suburb", c);
            }
        });
    }


    private void checkFunction() {
        String[] strArr = {"TV", "Kitchen", "Elevator", "WIFI", "Balcony", "Washer"};
        for (String str : strArr) {
            CheckBox checkBox = (CheckBox) View.inflate(this, R.layout.checkbox, null);
            checkBox.setText(str);
            checklist.addView(checkBox);
            checkBoxList.add(checkBox);
        }
    }

}
