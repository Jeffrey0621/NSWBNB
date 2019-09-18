package com.example.yyz.nswbnb_android.BaseBean;


public class UserBean {
    public MSG msg;

    public MSG getMsg() {
        return msg;
    }

    public void setMsg(MSG msg) {
        this.msg = msg;
    }

    public static class MSG {
        private String username, token;
        private int user_id;

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getToken() {
            return token;
        }

        public void setToken(String token) {
            this.token = token;
        }

        public int getUser_id() {
            return user_id;
        }

        public void setUser_id(int user_id) {
            this.user_id = user_id;
        }
    }

}
