package com.example.yyz.nswbnb_android.BaseBean;

import java.util.ArrayList;

public class OrderBean {
    public ArrayList<MSG> msg;

    public ArrayList<MSG> getMsg() {
        return msg;
    }

    public void setMsg(ArrayList<MSG> msg) {
        this.msg = msg;
    }

    public static class MSG {
        private int reservation_id, accommodation_id, price;
        private String check_in, check_out, accommodation_name, suburb;

        public int getReservation_id() {
            return reservation_id;
        }

        public void setReservation_id(int reservation_id) {
            this.reservation_id = reservation_id;
        }

        public int getAccommodation_id() {
            return accommodation_id;
        }

        public void setAccommodation_id(int accommodation_id) {
            this.accommodation_id = accommodation_id;
        }

        public int getPrice() {
            return price;
        }

        public void setPrice(int price) {
            this.price = price;
        }

        public String getCheck_in() {
            return check_in;
        }

        public void setCheck_in(String check_in) {
            this.check_in = check_in;
        }

        public String getCheck_out() {
            return check_out;
        }

        public void setCheck_out(String check_out) {
            this.check_out = check_out;
        }

        public String getAccommodation_name() {
            return accommodation_name;
        }

        public void setAccommodation_name(String accommodation_name) {
            this.accommodation_name = accommodation_name;
        }

        public String getSuburb() {
            return suburb;
        }

        public void setSuburb(String suburb) {
            this.suburb = suburb;
        }
    }
}
