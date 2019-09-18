package com.example.yyz.nswbnb_android.BaseBean;

import java.util.ArrayList;
import java.util.List;

public class SearchSesultBean {
    public ArrayList<MSG> msg;

    public ArrayList<MSG> getMsg() {
        return msg;
    }

    public void setMsg(ArrayList<MSG> msg) {
        this.msg = msg;
    }


    public static class MSG{
        public int id ;
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

        public int getId() {
            return id;
        }

        public void setId(int id) {
            this.id = id;
        }

        public int getHost_id() {
            return host_id;
        }

        public void setHost_id(int host_id) {
            this.host_id = host_id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public int getNum_guests() {
            return num_guests;
        }

        public void setNum_guests(int num_guests) {
            this.num_guests = num_guests;
        }

        public int getNum_bedrooms() {
            return num_bedrooms;
        }

        public void setNum_bedrooms(int num_bedrooms) {
            this.num_bedrooms = num_bedrooms;
        }

        public int getNum_beds() {
            return num_beds;
        }

        public void setNum_beds(int num_beds) {
            this.num_beds = num_beds;
        }

        public float getNum_bathrooms() {
            return num_bathrooms;
        }

        public void setNum_bathrooms(float num_bathrooms) {
            this.num_bathrooms = num_bathrooms;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }

        public String getSuburb() {
            return suburb;
        }

        public void setSuburb(String suburb) {
            this.suburb = suburb;
        }

        public String getCity() {
            return city;
        }

        public void setCity(String city) {
            this.city = city;
        }

        public String getState() {
            return state;
        }

        public void setState(String state) {
            this.state = state;
        }

        public String getCountry() {
            return country;
        }

        public void setCountry(String country) {
            this.country = country;
        }

        public int getPrice() {
            return price;
        }

        public void setPrice(int price) {
            this.price = price;
        }

        public String getProperty_type() {
            return property_type;
        }

        public void setProperty_type(String property_type) {
            this.property_type = property_type;
        }


        public ArrayList<String> getAmenities() {
            return amenities;
        }

        public void setAmenities(ArrayList<String> amenities) {
            this.amenities = amenities;
        }

        public ArrayList<String> getImage_urls() {
            return image_urls;
        }

        public void setImage_urls(ArrayList<String> image_urls) {
            this.image_urls = image_urls;
        }

        public float getRating() {
            return rating;
        }

        public void setRating(float rating) {
            this.rating = rating;
        }

        public int getNum_reviews() {
            return num_reviews;
        }

        public void setNum_reviews(int num_reviews) {
            this.num_reviews = num_reviews;
        }
    }
}
