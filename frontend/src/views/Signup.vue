<template>
  <div class="bg">
    <header-component></header-component>
    <a-spin :spinning="spinning" tip="Creating account...">
      <div style="margin-top:20px">
        <div class="login-box">
          <div class="login-inner-box">
            <div class="span-login">
              <span>Register with your email</span>
            </div>
            <br/>
            <div class="login-label">
              <label>Email address</label>
              <a-input id="email-add" size="large" placeholder="Email address" name="email" v-validate="'email'"
                       v-model="email"/>
              <span style="color: red">{{ errors.first('email') }}</span>
            </div>
            <div class="login-label">
              <label>Username</label>
              <a-input size="large" placeholder="Input username" v-model="rusername"></a-input>
            </div>
            <div class="login-label">
              <label>Password</label>
              <a-input size="large" type="text" v-if="pwdtype" v-model="eyetxt" name="password"
                       v-validate="{'required':'true'}"></a-input>
              <a-input size="large" placeholder="Password" type="password" v-model="eyetxt" name="password"
                       v-validate="{'required':'true'}" v-else/>
              <password v-model="eyetxt" :strength-meter-only="true"></password>
              <span style="color: red">{{ errors.first('password') }}</span>
            </div>
            <div style="text-align: left">
              <a-checkbox @change="onChange">Show password</a-checkbox>
            </div>
            <div>
              <a-button type="primary" icon="login" class="login-btn" v-on:click="onRegister">Register</a-button>
            </div>
            <div style="text-align: left">
              Already have an account? <a v-on:click="login">Login</a>
            </div>
          </div>
        </div>
      </div>
    </a-spin>
    <a-modal
      title="Message"
      v-model="visible"
      @ok="handleOk"
    >
      <p>{{wrong_msg}}</p>
    </a-modal>
  </div>
</template>

<script>
  import HeaderComponent from '../components/headercomponents'
  import Password from 'vue-password-strength-meter'

  export default {
    components: {
      HeaderComponent: HeaderComponent,
      Password: Password
    },
    methods: {
      handleOk() {
        this.visible = false
      },
      onChange(e) {
        this.pwdtype = !this.pwdtype
        console.log(`checked = ${e.target.checked}`)
      },
      /*register*/
      onRegister() {
        if (this.eyetxt === "") {
          /* this.visible = true
           this.wrong_msg = "Password should not be be empty or less than 8 characters!"*/
          this.$message.warning("Password should not be be empty!")
        } else if (this.username === "") {
          /*this.visible = true
          this.wrong_msg = "Username should not be be empty!"*/
          this.$message.warning("Username should not be be empty!")
        } else {
          this.spinning = true
          this.axios.post("/api/user", {
            username: this.rusername,
            password: this.eyetxt,
            email: this.email
          }).then((response) => {
            let res = response.data
            console.log(response)
            if (response.status === 201) {
              this.spinning = false
              this.$router.push('/login')
            }
          }).catch((e) => {
            this.spinning = false
            this.visible = true
            if (e.response.data["msg"]) {
              this.wrong_msg = e.response.data["msg"]
            } else if (e.response.data['errors']) {
              this.wrong_msg = e.response.data["errors"]
            } else {
              this.wrong_msg = "Bad request"
            }
          })
        }
      },
      login() {
        this.$router.push('/login')
      }
    },
    data() {
      return {
        eyetxt: "",
        rusername: "",
        pwdtype: false,
        email: '',
        spinning: false,
        visible: false,
        wrong_msg: ''
      }
    }
  }
</script>

