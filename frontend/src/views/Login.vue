<template>
  <div class="bg">
    <header-component></header-component>
    <a-spin :spinning="spinning" tip="Login...">
      <div style="margin-top:20px">
        <div class="login-box">
          <div class="login-inner-box">
            <div class="span-login">
              <span>Log in with your email</span>
            </div>
            <br/>
            <div class="login-label">
              <label>Email address</label>
              <a-input id="email-add" size="large" placeholder="Email address" v-model="email" name="email"
                       v-validate="'email'"/>
              <span style="color: red">{{ errors.first('email') }}</span>
            </div>
            <span v-show="warningPwd" style="color: red">Password is empty.</span>
            <span v-show="warningPwd1" style="color: red">Password is incorrect.</span>
            <div class="login-label">
              <label>Password</label>

              <a-input size="large" type="text" v-if="pwdtype" v-model="eyetxt" name="password"
                       v-validate="{'required':'true'}"></a-input>
              <a-input size="large" placeholder="Password" type="password" v-model="eyetxt" name="password"
                       v-validate="{'required':'true'}" v-else/>
              <span style="color: red">{{ errors.first('password') }}</span>
            </div>
            <div>
              <div style="text-align: left;">
                <a-checkbox @change="onChange">Show password</a-checkbox>
              </div>
            </div>
            <div>
              <a-button type="primary" icon="login" class="login-btn" v-on:click="onLogin">Login</a-button>
            </div>
            <div style="text-align: left">
              Don't have an account? <a v-on:click="signup">Sign up</a>
            </div>
          </div>
        </div>
      </div>
    </a-spin>
  </div>
</template>

<script>
  import HeaderComponent from '../components/headercomponents'
  import Cookies from 'js-cookie'

  export default {
    components: {
      HeaderComponent: HeaderComponent
    },
    methods: {
      onChange(e) {
        this.pwdtype = !this.pwdtype
        console.log(`checked = ${e.target.checked}`)
      },
      /*login*/
      onLogin() {
        let redirect = decodeURIComponent(this.$route.query.redirect || '/')
        if (this.email === '' || this.eyetxt === '') {
          alert("email/password cannot be empty!")
        } else {
          var _this = this
          this.spinning = true
          _this.axios.post("/api/login", {
            email: this.email,
            password: this.eyetxt
          }).then((response) => {
            let res = response.data.msg;
            if (response.status == 200) {
              Cookies.set('user_id', res.user_id, {expires: this.expires / 24})
              Cookies.set('username', res.username, {expires: this.expires / 24})
              Cookies.set('email', this.email, {expires: this.expires / 24})
              Cookies.set('token', res.token, {expires: this.expires / 24})
              const userinfo = {
                'username': res.username,
                'user_id': res.user_id,
                'email': this.email,
                'token': res.token
              }
              sessionStorage.setItem('userinfo', JSON.stringify(userinfo))
              this.spinning = false
              this.$router.push({path: redirect})
            }
          }).catch((e) => {
            _this.spinning = false
            _this.warningPwd1 = true
            if (e.response.data["msg"]) {
              console.log(e.response.data['msg'])
            } else if (e.response.data['errors']) {
              console.log(e.response.data['errors'])
            } else {
              console.log("Bad request")
            }
          })
        }
      },
      signup() {
        this.$router.push('/signup')
      }
    },
    data() {
      return {
        eyetxt: "",
        pwdtype: false,
        warningPwd: false,
        warningPwd1: false,
        email: '',
        spinning: false
      }
    }
  }
</script>

