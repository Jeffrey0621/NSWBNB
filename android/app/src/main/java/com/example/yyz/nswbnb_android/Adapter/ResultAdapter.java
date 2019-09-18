package com.example.yyz.nswbnb_android.Adapter;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import com.bumptech.glide.Glide;

import com.bumptech.glide.request.target.SimpleTarget;
import com.bumptech.glide.request.transition.Transition;
import com.example.yyz.nswbnb_android.BaseBean.SearchSesultBean;
import com.example.yyz.nswbnb_android.R;
import com.iarcuschin.simpleratingbar.SimpleRatingBar;

import java.util.ArrayList;

public class ResultAdapter extends RecyclerView.Adapter<ResultAdapter.ViewHolder> {

    private ArrayList<SearchSesultBean.MSG> mData;
    private LayoutInflater mInflater;
    private OnItemClickListener mClickListener;
    private Context context;


    // data is passed into the constructor
    public ResultAdapter(Context context, ArrayList<SearchSesultBean.MSG> data) {
        this.context = context;
        this.mInflater = LayoutInflater.from(context);
        this.mData = data;
    }


    // inflates the row layout from xml when needed
    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = mInflater.inflate(R.layout.result_adapter, parent, false);
        ViewHolder myViewHolder = new ViewHolder(view);
        return myViewHolder;
    }

    // binds the data to the TextView in each row
    @Override
    public void onBindViewHolder(final ViewHolder holder, int position) {
        ArrayList<SearchSesultBean.MSG> animal = mData;
        holder.itemView.setTag(position);
        holder.search_result_name.setText(mData.get(position).getName());
        //Log.e("imageurl",mData.get(position).getName());
        Glide.with(context).load(mData.get(position).getImage_urls().get(0)).into(new SimpleTarget<Drawable>() {
            @Override
            public void onResourceReady(@NonNull Drawable resource, @Nullable Transition<? super Drawable> transition) {
                holder.search_result_image.setImageDrawable(resource);
            }
        });
        holder.numberofresult.setText(mData.get(position).getNum_reviews()+"reviews");
        holder.search_property_type.setText(mData.get(position).getProperty_type());

        holder.ratingBar.setRating(Float.valueOf(mData.get(position).getRating()/2));
        holder.search_price.setText("$"+String.valueOf(mData.get(position).getPrice()/100)+"/night");
    }

    // total number of rows
    @Override
    public int getItemCount() {
        return mData.size();

    }


    // stores and recycles views as they are scrolled off screen
    public class ViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
        CardView result_img;
        ImageView search_result_image;
        TextView search_result_name,numberofresult,search_property_type,search_price;
        SimpleRatingBar ratingBar;
        ViewHolder(View itemView) {
            super(itemView);
            result_img = itemView.findViewById(R.id.result_img);
            search_result_image = itemView.findViewById(R.id.search_result_image);
            search_result_name = itemView.findViewById(R.id.search_result_name);
            numberofresult = itemView.findViewById(R.id.numberofresult);
            search_property_type = itemView.findViewById(R.id.search_property_type);
            ratingBar = itemView.findViewById(R.id.ratingBar);
            search_price = itemView.findViewById(R.id.search_price);
            /*SimpleRatingBar.AnimationBuilder builder = ratingBar.getAnimationBuilder()
                    .setRatingTarget(3)
                    .setDuration(2000)
                    .setInterpolator(new BounceInterpolator());
            builder.start();*/
            itemView.setOnClickListener(this);
        }

        @Override
        public void onClick(View view) {
            if (mClickListener != null){
                mClickListener.onItemClick(view, (Integer) view.getTag(),mData);//(int)view.getTag()
            }
        }
    }

    // convenience method for getting data at click position
    public SearchSesultBean.MSG getItem(int id) {
        return mData.get(id);
    }

    // allows clicks events to be caught
    public void setOnClickListener(OnItemClickListener itemClickListener) {
        this.mClickListener = itemClickListener;
    }

    // parent activity will implement this method to respond to click events
    public interface OnItemClickListener {
        void onItemClick(View view, int position, ArrayList<SearchSesultBean.MSG> mData);
    }

}
