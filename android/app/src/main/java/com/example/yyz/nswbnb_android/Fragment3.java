package com.example.yyz.nswbnb_android;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.yyz.nswbnb_android.BaseBean.ErrorBean;
import com.example.yyz.nswbnb_android.BaseBean.UserBean;
import com.google.gson.Gson;

import java.io.IOException;

import es.dmoral.toasty.Toasty;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


public class Fragment3 extends Fragment {
    private Button innerlogin, innerregister;

    private ScrollView registerpage, loginpage;
    private EditText loginemail, loginpwd, registerusername, registeremail, registerpwd;
    private boolean isLogin;
    private TextView link_signup, link_login;
    private boolean regflag = false;
    private String errormsg, errormsg1;
    private int statuscode;


    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment3, container, false);
        isLogin = ((MainActivity) getActivity()).isLogin();

        loginpage = view.findViewById(R.id.loginpage);
        registerpage = view.findViewById(R.id.registerpage);

        link_signup = view.findViewById(R.id.link_signup);
        link_login = view.findViewById(R.id.link_login);

        loginpage.setVisibility(View.VISIBLE);
        registerpage.setVisibility(View.GONE);

        loginemail = view.findViewById(R.id.loginEmail);
        loginpwd = view.findViewById(R.id.loginpassword);
        innerlogin = view.findViewById(R.id.innerlogin);

        innerlogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                login();
            }
        });
        link_signup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                registerpage.setVisibility(View.VISIBLE);
                loginpage.setVisibility(View.GONE);
            }
        });
        link_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                registerpage.setVisibility(View.GONE);
                loginpage.setVisibility(View.VISIBLE);

            }
        });

        registeremail = view.findViewById(R.id.registeremail);
        registerusername = view.findViewById(R.id.registerusername);
        registerpwd = view.findViewById(R.id.registerpwd);
        innerregister = view.findViewById(R.id.innerregister);

        innerregister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                registerfunc();

            }
        });


        return view;
    }

    private void login() {
        if (!validate()) {
            onLoginFailed();
            return;
        }
        final ProgressDialog progressDialog = new ProgressDialog(getActivity(), R.style.AppTheme_Dark_Dialog);

        progressDialog.setIndeterminate(true);
        progressDialog.setMessage("Authenticating...");
        progressDialog.show();

        final String email = loginemail.getText().toString();
        String password = loginpwd.getText().toString();

        OkHttpClient okHttpClient = new OkHttpClient();
        FormBody.Builder formbody = new FormBody.Builder();
        formbody.add("email", email);
        formbody.add("password", password);
        Request request = new Request.Builder()
                .url("http://nswbnb.herokuapp.com/api/login")
                .post(formbody.build())
                .build();
        okHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e("onfail:", e.toString());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                statuscode = response.code();
                progressDialog.dismiss();
                if (statuscode == 200) {
                    ((MainActivity) getActivity()).setLogin(true);
                    SharedPreferences sharedPreferences = getActivity().getSharedPreferences("USERINFO", Context.MODE_PRIVATE);
                    SharedPreferences.Editor editor = sharedPreferences.edit();
                    editor.putString("useremail",email);
                    String res = response.body().string();
                    Log.e("suce",res);
                    UserBean userBean = new Gson().fromJson(res, UserBean.class);
                    editor.putInt("userid",userBean.getMsg().getUser_id());
                    editor.putString("username",userBean.getMsg().getUsername());
                    editor.putString("token",userBean.getMsg().getToken());
                    System.out.println(userBean.getMsg().getToken());
                    editor.commit();
                    //System.out.println("测试" + ((MainActivity) getActivity()).isLogin());
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {

                            Intent intent = new Intent(getContext(),MainActivity.class);
                            startActivity(intent);
                        }
                    });

                } else {
                    String res = response.body().string();
                    ErrorBean err0 = new Gson().fromJson(res, ErrorBean.class);
                    errormsg = err0.getError();
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            loginemail.setText("");
                            loginpwd.setText("");
                            //Log.e("失败", String.valueOf(((MainActivity) getActivity()).isLogin()));
                        }
                    });
                }

            }
        });
    }


    private void onLoginFailed() {
        Toasty.error(getContext(), "Log in failed.", Toast.LENGTH_SHORT, true).show();
        innerlogin.setEnabled(true);
    }

    private boolean validate() {
        boolean valid = true;
        String email = loginemail.getText().toString();
        String password = loginpwd.getText().toString();
        if (email.isEmpty() || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            loginemail.setError("enter a valid email address");
            valid = false;
        } else {
            loginemail.setError(null);
        }
        if (password.isEmpty() || password.length() < 8 || password.length() > 20) {
            loginpwd.setError("between 8 and 20 alphanumeric characters");
            valid = false;
        } else {
            loginpwd.setError(null);
        }
        return valid;
    }

    private void registerfunc() {
        if (!regvalidate()) {
            Toast.makeText(getContext(), "Register failed", Toast.LENGTH_LONG).show();
            innerregister.setEnabled(true);
            return;
        }


        final ProgressDialog progressDialog = new ProgressDialog(getActivity(), R.style.AppTheme_Dark_Dialog);
        progressDialog.setIndeterminate(true);
        progressDialog.setMessage("Creating Account...");
        progressDialog.show();

        String name = registerusername.getText().toString();
        String email = registeremail.getText().toString();
        String password = registerpwd.getText().toString();


        OkHttpClient okHttpClient = new OkHttpClient();
        FormBody.Builder formbody = new FormBody.Builder();
        formbody.add("username", name);
        formbody.add("email", email);
        formbody.add("password", password);
        Request request = new Request.Builder()
                .url("http://nswbnb.herokuapp.com/api/user")
                .post(formbody.build())
                .build();
        okHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                progressDialog.dismiss();
                if (response.code() == 201) {
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            registerpage.setVisibility(View.GONE);
                            loginpage.setVisibility(View.VISIBLE);
                        }
                    });
                } else {
                    String res = response.body().string();
                    Log.e("fail", res);
                    ErrorBean err1 = new Gson().fromJson(res, ErrorBean.class);
                    errormsg1 = err1.getError();
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            registeremail.setText("");
                            registerpwd.setText("");
                            registerusername.setText("");
                            Toast.makeText(getContext(), errormsg1, Toast.LENGTH_LONG).show();
                        }
                    });
                }
            }
        });
    }

    private boolean regvalidate() {
        boolean valid = true;

        String name = registerusername.getText().toString();
        String email = registeremail.getText().toString();
        String password = registerpwd.getText().toString();

        if (name.isEmpty() || name.length() < 3) {
            registerusername.setError("at least 3 characters");
            valid = false;
        } else {
            registerusername.setError(null);
        }

        if (email.isEmpty() || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            registeremail.setError("enter a valid email address");
            valid = false;
        } else {
            registeremail.setError(null);
        }

        if (password.isEmpty() || password.length() < 8 || password.length() > 20) {
            registerpwd.setError("between 8 and 20 alphanumeric characters");
            valid = false;
        } else {
            registerpwd.setError(null);
        }

        return valid;
    }

}
