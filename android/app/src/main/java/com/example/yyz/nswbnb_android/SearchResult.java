package com.example.yyz.nswbnb_android;

import android.app.Dialog;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;


import com.archit.calendardaterangepicker.customviews.DateRangeCalendarView;
import com.example.yyz.nswbnb_android.Adapter.ResultAdapter;
import com.example.yyz.nswbnb_android.BaseBean.SearchSesultBean;
import com.example.yyz.nswbnb_android.utils.SelfDialog;
import com.google.gson.Gson;
import com.jmf.addsubutils.AddSubUtils;
import com.wang.avi.AVLoadingIndicatorView;

import org.angmarch.views.NiceSpinner;
import org.xutils.common.Callback;
import org.xutils.ex.HttpException;
import org.xutils.http.RequestParams;
import org.xutils.x;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;

import java.util.LinkedList;
import java.util.List;

import es.dmoral.toasty.Toasty;


public class SearchResult extends AppCompatActivity {
    private EditText search_location;
    private Button search_checkdate;
    private NiceSpinner search_guestnumber;
    private String startdate, enddate;
    private Dialog dialog;
    private List<Integer> numguest;
    private Button filters;
    private RecyclerView detailresult;
    private LinearLayoutManager layoutManager;
    private ResultAdapter mAdapter;
    private SearchSesultBean searchSesultBean;
    private AVLoadingIndicatorView search_avi;
    private ImageButton search_less,search_more;
    private TextView list_message;
    private LinearLayout search_bedroom,search_bed,search_bathroom;
    private AddSubUtils add_sub_bed,add_sub_bedroom,add_sub_bathroom;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_result);


        Intent i = getIntent();
        Bundle b = i.getExtras();

        search_location = findViewById(R.id.search_location);
        search_checkdate = findViewById(R.id.search_checkdate);
        search_guestnumber = findViewById(R.id.search_guestnumber);
        detailresult = findViewById(R.id.detailresult);
        search_avi = findViewById(R.id.search_avi);
        search_more = findViewById(R.id.search_more);
        search_less = findViewById(R.id.search_less);
        filters = findViewById(R.id.filters);
        list_message = findViewById(R.id.list_message);
        add_sub_bed = findViewById(R.id.add_sub_bed);
        add_sub_bedroom = findViewById(R.id.add_sub_bedroom);
        add_sub_bathroom = findViewById(R.id.add_sub_bathroom);

        add_sub_bed.setBuyMax(3).setOnWarnListener(new AddSubUtils.OnWarnListener() {
            @Override
            public void onWarningForInventory(int inventory) {
            }
            @Override
            public void onWarningForBuyMax(int max) {
                Toasty.info(SearchResult.this,"The max number is 3",Toasty.LENGTH_SHORT,true).show();
            }
            @Override
            public void onWarningForBuyMin(int min) {
            }
        });
        add_sub_bedroom.setBuyMax(3).setOnWarnListener(new AddSubUtils.OnWarnListener() {
            @Override
            public void onWarningForInventory(int inventory) {
            }
            @Override
            public void onWarningForBuyMax(int max) {
                Toasty.info(SearchResult.this,"The max number is 3",Toasty.LENGTH_SHORT,true).show();
            }
            @Override
            public void onWarningForBuyMin(int min) {
            }
        });
        add_sub_bathroom.setBuyMax(3).setOnWarnListener(new AddSubUtils.OnWarnListener() {
            @Override
            public void onWarningForInventory(int inventory) {
            }
            @Override
            public void onWarningForBuyMax(int max) {
                Toasty.info(SearchResult.this,"The max number is 3",Toasty.LENGTH_SHORT,true).show();
            }
            @Override
            public void onWarningForBuyMin(int min) {
            }
        });

        search_bed = findViewById(R.id.search_bed);
        search_bedroom = findViewById(R.id.search_bedroom);
        search_bathroom = findViewById(R.id.search_bathroom);

        search_avi.show();
        search_avi.setVisibility(View.VISIBLE);

        search_checkdate.setVisibility(View.GONE);
        search_guestnumber.setVisibility(View.GONE);
        filters.setVisibility(View.GONE);
        search_bed.setVisibility(View.GONE);
        search_bedroom.setVisibility(View.GONE);
        search_bathroom.setVisibility(View.GONE);

        layoutManager = new LinearLayoutManager(this);


        search_location.setText(b.getString("location"));
        if (b.getString("startdate") != null && b.getString("enddate") != null) {
            search_checkdate.setText(b.getString("startdate") + "-" + b.getString("enddate"));
            startdate = b.getString("startdate");
            enddate = b.getString("enddate");
        }
        numguest = new LinkedList<>(Arrays.asList(1,2,3,4,5,6));
        search_guestnumber.attachDataSource(numguest);
        search_guestnumber.setSelectedIndex(b.getInt("guestnumber"));


        String url="http://nswbnb.herokuapp.com/api/search";
        RequestParams params = new RequestParams(url);
        params.addQueryStringParameter("location", b.getString("location"));
        params.addQueryStringParameter("check_in", b.getString("startdate"));
        params.addQueryStringParameter("num_guests", search_guestnumber.getItemAtPosition(b.getInt("guestnumber")).toString());
        params.addQueryStringParameter("check_out", b.getString("enddate"));

        search_result(url,params);

        /*OkHttpClient okHttpClient = new OkHttpClient();
        okHttpClient.newBuilder()
                .retryOnConnectionFailure(true)
                .build();

        Request request = new Request.Builder()
                .header("Connection","close")
                .url("http://nswbnb.herokuapp.com/api/search?location=" + b.getString("location")
                        + "&check_in=" + b.getString("startdate") + "&check_out=" + b.getString("enddate") +
                        "&num_guests=" + search_guestnumber.getItemAtPosition(b.getInt("guestnumber")).toString())
                .get()

                .build();
        okHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e("failure", e.toString());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                ResponseBody body = response.body();
                int code = response.code();
                //if use String res = response.body().string() will cause response close()

                if (response.isSuccessful()) {
                    try {
                        String res = body.string();
                        searchSesultBean = new Gson().fromJson(res, SearchSesultBean.class);
                        SearchResult.this.runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                detailresult.setLayoutManager(layoutManager);
                                mAdapter = new ResultAdapter(SearchResult.this, searchSesultBean.getMsg());
                                detailresult.setAdapter(mAdapter);
                                mAdapter.setOnClickListener(new ResultAdapter.OnItemClickListener() {
                                    @Override
                                    public void onItemClick(View view, int position, ArrayList<SearchSesultBean.MSG> mData) {

                                        Intent intent = new Intent(SearchResult.this, DetailActivity.class);
                                        Bundle bundle = new Bundle();
                                        bundle.putInt("accid",mData.get(position).id);
                                        bundle.putInt("host_id",mData.get(position).host_id);
                                        bundle.putString("name",mData.get(position).name);
                                        bundle.putInt("num_guests",mData.get(position).num_guests);
                                        bundle.putInt("num_bedrooms",mData.get(position).num_bedrooms);
                                        bundle.putInt("num_beds",mData.get(position).num_beds);
                                        bundle.putFloat("num_bathrooms",mData.get(position).num_bathrooms);
                                        bundle.putString("description",mData.get(position).description);
                                        bundle.putString("suburb",mData.get(position).suburb);
                                        bundle.putString("city",mData.get(position).city);
                                        bundle.putString("state",mData.get(position).state);
                                        bundle.putString("country",mData.get(position).country);
                                        bundle.putInt("price",mData.get(position).price);
                                        bundle.putString("property_type",mData.get(position).property_type);
                                        bundle.putStringArrayList("amenities",mData.get(position).amenities);
                                        bundle.putStringArrayList("image_urls",mData.get(position).image_urls);
                                        bundle.putFloat("rating",mData.get(position).rating);
                                        bundle.putInt("num_reviews",mData.get(position).num_reviews);
                                        bundle.putString("startdate",startdate);
                                        bundle.putString("enddate",enddate);

                                        intent.putExtras(bundle);
                                        startActivity(intent);
                                        //Toast.makeText(SearchResult.this,String.valueOf(position),Toast.LENGTH_LONG).show();
                                    }
                                });
                                mAdapter.notifyDataSetChanged();
                            }
                        });
                    }catch (ProtocolException e){
                        Log.e("失败",e.getMessage());
                    }
                    // Log.e("previous",res);


                    //Log.e("success", searchSesultBean.getMsg().get(0).getName());


                } else {
                    Log.e("failure", "failure");
                }
            }
        });
*/

        filters.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                /*Intent intent = new Intent(SearchResult.this, Filters.class);
                startActivity(intent);*/
                search_avi.setVisibility(View.VISIBLE);
                search_avi.show();

                String url="http://nswbnb.herokuapp.com/api/search";
                RequestParams params = new RequestParams(url);
                params.addQueryStringParameter("location", search_location.getText().toString());
                params.addQueryStringParameter("check_in", startdate);
                params.addQueryStringParameter("num_guests", search_guestnumber.getSelectedItem().toString());
                params.addQueryStringParameter("check_out", enddate);

                params.addQueryStringParameter("num_beds", String.valueOf(add_sub_bed.getNumber()));
                params.addQueryStringParameter("num_bedrooms", String.valueOf(add_sub_bedroom.getNumber()));
                params.addQueryStringParameter("num_bathrooms", String.valueOf(add_sub_bathroom.getNumber()));

                search_result(url,params);
                list_message.setVisibility(View.GONE);
                search_more.setVisibility(View.VISIBLE);
                search_less.setVisibility(View.GONE);
                search_checkdate.setVisibility(View.GONE);
                search_guestnumber.setVisibility(View.GONE);
                filters.setVisibility(View.GONE);
                search_bed.setVisibility(View.GONE);
                search_bedroom.setVisibility(View.GONE);
                search_bathroom.setVisibility(View.GONE);
            }
        });

        search_more.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                search_more.setVisibility(View.GONE);
                search_less.setVisibility(View.VISIBLE);
                search_checkdate.setVisibility(View.VISIBLE);
                search_guestnumber.setVisibility(View.VISIBLE);
                filters.setVisibility(View.VISIBLE);
                search_bed.setVisibility(View.VISIBLE);
                search_bedroom.setVisibility(View.VISIBLE);
                search_bathroom.setVisibility(View.VISIBLE);
            }
        });
        search_less.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                search_more.setVisibility(View.VISIBLE);
                search_less.setVisibility(View.GONE);
                search_checkdate.setVisibility(View.GONE);
                search_guestnumber.setVisibility(View.GONE);
                filters.setVisibility(View.GONE);
                search_bed.setVisibility(View.GONE);
                search_bedroom.setVisibility(View.GONE);
                search_bathroom.setVisibility(View.GONE);
            }
        });

        search_checkdate.setKeyListener(null);
        search_checkdate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showdialog();
            }
        });


        search_guestnumber.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
            }
        });
        initToolbar();

    }

    private void search_result(String url, RequestParams params) {
        x.http().get(params, new Callback.CacheCallback<String>() {
            private boolean hasError = false;
            private String result = null;
            @Override
            public void onSuccess(String result) {
                if (result != null) {
                    this.result = result;
                }
                Log.e("success","success");

            }

            @Override
            public void onError(Throwable ex, boolean isOnCallback) {
                Log.e("fail",ex.toString());
                hasError = true;
                Toast.makeText(x.app(), ex.getMessage(), Toast.LENGTH_LONG).show();
                if (ex instanceof HttpException) {
                    HttpException httpEx = (HttpException) ex;
                    int responseCode = httpEx.getCode();
                    String responseMsg = httpEx.getMessage();
                    String errorResult = httpEx.getResult();
                }
            }

            @Override
            public void onCancelled(CancelledException cex) {
                Log.e("fail1","fail");
            }

            @Override
            public void onFinished() {
                search_avi.hide();
                search_avi.setVisibility(View.GONE);

                if (!hasError && result != null) {
                    //Toast.makeText(x.app(), result, Toast.LENGTH_LONG).show();
                    Gson gson = new Gson();
                    searchSesultBean = gson.fromJson(result, SearchSesultBean.class);
                    if(searchSesultBean.getMsg().isEmpty()){
                        list_message.setVisibility(View.VISIBLE);
                    }else {
                        SearchResult.this.runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                detailresult.setLayoutManager(layoutManager);
                                mAdapter = new ResultAdapter(SearchResult.this, searchSesultBean.getMsg());
                                detailresult.setAdapter(mAdapter);
                                mAdapter.setOnClickListener(new ResultAdapter.OnItemClickListener() {
                                    @Override
                                    public void onItemClick(View view, int position, ArrayList<SearchSesultBean.MSG> mData) {

                                        Intent intent = new Intent(SearchResult.this, DetailActivity.class);
                                        Bundle bundle = new Bundle();
                                        bundle.putInt("accid", mData.get(position).id);
                                        bundle.putInt("host_id", mData.get(position).host_id);
                                        bundle.putString("name", mData.get(position).name);
                                        bundle.putInt("num_guests", mData.get(position).num_guests);
                                        bundle.putInt("num_bedrooms", mData.get(position).num_bedrooms);
                                        bundle.putInt("num_beds", mData.get(position).num_beds);
                                        bundle.putFloat("num_bathrooms", mData.get(position).num_bathrooms);
                                        bundle.putString("description", mData.get(position).description);
                                        bundle.putString("suburb", mData.get(position).suburb);
                                        bundle.putString("city", mData.get(position).city);
                                        bundle.putString("state", mData.get(position).state);
                                        bundle.putString("country", mData.get(position).country);
                                        bundle.putInt("price", mData.get(position).price);
                                        bundle.putString("property_type", mData.get(position).property_type);
                                        bundle.putStringArrayList("amenities", mData.get(position).amenities);
                                        bundle.putStringArrayList("image_urls", mData.get(position).image_urls);
                                        bundle.putFloat("rating", mData.get(position).rating);
                                        bundle.putInt("num_reviews", mData.get(position).num_reviews);
                                        bundle.putString("startdate", startdate);
                                        bundle.putString("enddate", enddate);

                                        intent.putExtras(bundle);
                                        startActivity(intent);
                                        //Toast.makeText(SearchResult.this,String.valueOf(position),Toast.LENGTH_LONG).show();
                                    }
                                });
                                mAdapter.notifyDataSetChanged();
                            }
                        });
                    }
                }
            }
            @Override
            public boolean onCache(String result) {
                //because the network result stream are too long,so I use cache to collect all stream,
                // otherwise will meet problem of unexpected end of stream
                this.result = result;
                return true;
            }
        });
    }

    private void initToolbar() {
        Toolbar toolbar = findViewById(R.id.search_toolbar);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }

    private void showdialog() {
        View view = View.inflate(SearchResult.this, R.layout.dialog_layout, null);
        dialog = new SelfDialog(SearchResult.this, 200, 200, view, R.style.dialog);
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
                search_checkdate.setText(startdate + '-' + enddate);
                dialog.dismiss();
            }
        });
    }



}
