<template>
  <div>
    <login-header></login-header>
    <div style="padding: 50px 200px;background-color: #ececec;">
      <div style="padding: 24px 0; background: #fff">
        <a-spin :spinning="spinning" tip="Booking...">
          <div style="background-color: #ececec;width: 95%;text-align: left;height: 45px;margin-left: 2.5%;">
            <h2 style="padding: 6px 12px 0 12px;color: #484848">Booking Information</h2>
          </div>
          <div style="margin: 10px 20%;">
            <div style="text-align: left;margin-top: 20px">
              <h2>{{this.accommodation_name}}</h2>
            </div>
            <div style="text-align: left;margin-top: 20px">
              <h3>{{this.location}}</h3>
            </div>
            <div style="text-align: left;margin-top: 20px">
              <h3>{{this.guest_num}} guests</h3>
            </div>
            <a-divider></a-divider>

            <!--price-->
            <div>
              <div style="width: 30%;float: left; margin-top: 20px;text-align: left;">
                <label class="text-left">price</label>
              </div>
              <div style="margin-top: 20px;float:left;text-align: right;width: 60%">
                <label class="text-right">{{this.price}}/night</label>
              </div>
              <div style="clear: left"></div>
            </div>

            <!--checkin-->
            <div>
              <div style="width: 30%;float: left; margin-top: 20px;text-align: left;">
                <label class="text-left">check-in</label>
              </div>
              <div style="margin-top: 20px;float:left;text-align: right;width: 60%">
                <label class="text-right">{{this.check_in}}</label>
              </div>
              <div style="clear: left"></div>
            </div>

            <!--checkout-->
            <div>
              <div style="width: 30%;float: left; margin-top: 20px;text-align: left;">
                <label class="text-left">check-out</label>
              </div>
              <div style="margin-top: 20px;float:left;text-align: right;width: 60%">
                <label class="text-right">{{this.check_out}}</label>
              </div>
              <div style="clear: left"></div>
            </div>

            <!--total-->
            <div>
              <div style="width: 30%;float: left; margin-top: 20px;text-align: left;">
                <label class="text-left">Total(AUD)</label>
              </div>
              <div style="margin-top: 20px;float:left;text-align: right;width: 60%">
                <label class="text-right">$ {{this.price*this.day}}</label>
              </div>
              <div style="clear: left"></div>
            </div>

            <a-divider style="margin-top: 30px"></a-divider>
            <div style="text-align: right">
              <a-button class="primary" :size="size" v-on:click="booking">Agree and continue</a-button>
            </div>

          </div>
        </a-spin>
      </div>

    </div>
  </div>
</template>

<script>
  import LoginHeader from "./../components/LoginHeader"
  import Cookies from 'js-cookie'

  export default {
    components: {LoginHeader},
    data() {
      return {
        size: 'large',
        spinning: false,
        accommodation_name: Cookies.get('book_accommodation_name'),
        location: Cookies.get('location'),
        guest_num: Cookies.get('book_guest_num'),
        price: Cookies.get('book_price'),
        check_in: Cookies.get('book_check_in'),
        check_out: Cookies.get('book_check_out'),
        day: Cookies.get('book_day'),
      }
    },
    methods: {
      /*create the booking*/
      booking() {
        this.spinning = true
        this.axios.post("/api/reservation", {
          token: Cookies.get('token'),
          guest_id: Cookies.get('user_id'),
          accommodation_id: Cookies.get('book_accommodation_id'),
          num_guests: this.guest_num,
          check_in: this.check_in,
          check_out: this.check_out
        }).then((response) => {
          if (response.status === 201) {
            this.$notification["success"]({
              message: 'Success',
              description: 'Congratulations, booking successfully!',
              duration: 2,
            });
            this.$router.push('/profile')
          } else {
            console.log(response.data.msg)
          }
          this.spinning = false
        }).catch((e) => {
          this.spinning = false
          if (e.response.data["msg"]) {
            console.log(e.response.data['msg'])
          } else if (e.response.data['errors']) {
            console.log(e.response.data['errors'])
          } else {
            console.log("Bad request")
          }
        })
      },
    },
    destroyed() {
      Cookies.remove('book_accommodation_id')
      Cookies.remove('book_accommodation_name')
      Cookies.remove('location')
      Cookies.remove('book_guest_num')
      Cookies.remove('book_price')
      Cookies.remove('book_check_in')
      Cookies.remove('book_check_out')
      Cookies.remove('book_day')
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
    font-size: 16px;
  }
</style>
