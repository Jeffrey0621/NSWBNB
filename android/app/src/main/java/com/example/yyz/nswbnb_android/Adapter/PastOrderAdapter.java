package com.example.yyz.nswbnb_android.Adapter;

import android.content.Context;
import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.example.yyz.nswbnb_android.BaseBean.OrderBean;
import com.example.yyz.nswbnb_android.R;

import java.util.ArrayList;

public class PastOrderAdapter extends RecyclerView.Adapter<PastOrderAdapter.ViewHolder> {

    private ArrayList<OrderBean.MSG> mData;
    private LayoutInflater mInflater;
    private PastOrderAdapter.OnItemClickListener mClickListener;
    private Context context;


    // data is passed into the constructor
    public PastOrderAdapter(Context context, ArrayList<OrderBean.MSG> data) {
        this.context = context;
        this.mInflater = LayoutInflater.from(context);
        this.mData = data;
    }


    // inflates the row layout from xml when needed
    @Override
    public PastOrderAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = mInflater.inflate(R.layout.past_order_adapter,parent, false);
        PastOrderAdapter.ViewHolder myViewHolder = new PastOrderAdapter.ViewHolder(view);
        return myViewHolder;
    }


    // binds the data to the TextView in each row
    @Override
    public void onBindViewHolder(final PastOrderAdapter.ViewHolder holder, int position) {
        ArrayList<OrderBean.MSG> animal = mData;
        holder.itemView.setTag(position);

        holder.order_name.setText(mData.get(position).getAccommodation_name());
        holder.order_location.setText(mData.get(position).getSuburb());
        holder.order_price.setText("$"+String.valueOf(mData.get(position).getPrice()/100)+"/night");
        holder.order_date.setText(mData.get(position).getCheck_in()+"-"+mData.get(position).getCheck_out());

    }

    // total number of rows
    @Override
    public int getItemCount() {
        return mData.size();

    }


    // stores and recycles views as they are scrolled off screen
    public class ViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
        TextView order_name,order_location,order_price,order_date;
        CardView order_Card;
        ViewHolder(View itemView) {
            super(itemView);
            order_date = itemView.findViewById(R.id.past_order_date);
            order_name = itemView.findViewById(R.id.past_order_name);
            order_location = itemView.findViewById(R.id.past_order_location);
            order_price = itemView.findViewById(R.id.past_order_price);
            order_Card = itemView.findViewById(R.id.past_order_Card);

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
    public OrderBean.MSG getItem(int id) {
        return mData.get(id);
    }

    // allows clicks events to be caught
    public void setOnClickListener(PastOrderAdapter.OnItemClickListener itemClickListener) {
        this.mClickListener = itemClickListener;
    }

    // parent activity will implement this method to respond to click events
    public interface OnItemClickListener {
        void onItemClick(View view, int position, ArrayList<OrderBean.MSG> mData);
    }
}
