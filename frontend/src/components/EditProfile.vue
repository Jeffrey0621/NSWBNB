<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--title-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Personal Information</h2>
    </div>
    <a-spin :spinning="spinning" tip="Updating...">
      <!--user name-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">Username</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right" v-model='username' disabled></input>
        </div>
        <div style="clear: left"></div>
      </div>
      <!--email address-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">Email address</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right" v-model='email' @change="onChange"></input>
        </div>
        <div style="clear: left"></div>
      </div>
      <!-- Phone number-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">Phone number</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right" v-model="phone_number" @change="onChange"></input>
        </div>
        <div style="clear: left"></div>
      </div>
      <!--gender-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">I am</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <a-select class="text-right1" style="width: 50%" v-model="gender_selected" @change="onChange">
            <a-select-option v-for="i in gender" :key="i">{{i}}</a-select-option>
          </a-select>
        </div>
        <div style="clear: left"></div>
      </div>
      <a-divider></a-divider>
      <div style="text-align: right;margin-right: 20px;margin-bottom: 20px">
        <a-button type="danger" :size="size" v-on:click="update_info">Update personal information</a-button>
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
  import Cookies from 'js-cookie'

  const gender = ["male", "female"]
  export default {
    data() {
      return {
        size: 'large',
        gender,
        gender_selected: "",
        username: '',
        email: '',
        phone_number: "",
        spinning: false,
        change_flag: false,
        visible: false,
        wrong_msg: '',
      }
    },
    methods: {
      handleOk(e) {
        this.visible = false
      },
      /*update user information*/
      update_info() {
        if (this.change_flag === true) {
          this.spinning = true
          this.axios.put('/api/user', {
            token: Cookies.get('token'),
            email: this.email,
            phone: this.phone_number,
            gender: this.gender_selected
          }).then((response) => {
            let res = response.data
            if (response.status === 200) {
              this.visible = true
              this.wrong_msg = "User info updated."
            }
            /*if (response.status === 200 && !res['is_phone_dup'] ) {
              this.visible = true
              this.wrong_msg = "User info updated."
            }else if(response.status === 200 && res['is_phone_dup'] ){
              this.visible = true
              this.wrong_msg = "Phone number has been used."
            }*/
            else {
              alert(response.data.error)
            }
            this.spinning = false
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
        } else {
          this.visible = true
          this.wrong_msg = 'Nothing changed'
        }
      },
      onChange() {
        this.change_flag = true
      }
    },
    mounted() {
      this.username = Cookies.get("username")
      this.email = Cookies.get("email")
      let _this = this
      _this.axios.get('/api/user', {
        params: {
          token: Cookies.get('token')
        }
      }).then((response) => {
        let res = response.data.msg
        console.log(res)
        _this.email = res.email
        _this.username = res.username
        _this.phone_number = res.phone
        _this.gender_selected = res.gender
      }).catch((e) => {
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
  }
</script>

<style scoped>
  .text-left {
    padding: 0 20px;
    font-size: 16px
  }

  .text-right {
    width: 100%;
    margin-top: 30px;
    height: 40px;
    padding: 8px 10px;
    border: 1px solid #aaa;
    font-size: 16px;
    border-radius: 4px;
  }

  .text-right1 {
    width: 50%;
    margin-top: 30px;
    height: 40px;
    font-size: 16px;
  }
</style>
