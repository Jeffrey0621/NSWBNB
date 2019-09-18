<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--The reservations in progress-->
    <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Current Reservations</h2>
    </div>
    <a-spin :spinning="spinning1" tip="Loading...">
      <div v-show="havenoresult1">
        <h2>No Current Reservations</h2>
      </div>
      <div style="text-align: left;margin-bottom: 20px" v-show="haveresult1">
        <a-list
          class="comment-list"
          itemLayout="vertical"
          :grid="{ gutter: 16, column: 2 }"
          :dataSource="in_process"
          :pagination="pagination"
        >
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-card
              style="width: 300px;margin: 16px"
            >
              <template class="ant-card-actions" slot="actions">
                <a-icon type="logout" @click="check_out(index,item.id)"/>
                <p @click="detailed(item.accommodation_id)">Details</p>
              </template>
              <a-icon type="user" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.guest_name}}</p>
              <div style="clear: left"></div>
              <a-icon type="contacts" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.guest_contact}}</p>
              <div style="clear: left"></div>
              <a-icon type="home" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px;text-overflow:ellipsis;white-space:nowrap;overflow: hidden;width: 70%">{{item.accommodation_name}}</p>
              <div style="clear: left"></div>
              <a-icon type="environment" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.suburb}}</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-right" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_in_date}}</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-left" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_out_date}}</p>
              <div style="clear: left"></div>
            </a-card>
            <!--<a slot="actions" @click="check_out(index,item.id)">check out</a>
            {{item.guest_name}}<br>
            <span>Contact email:{{item.guest_contact}}</span><br>
            <span>Property name:{{item.accommodation_name}}</span><br>
            <span>Property location:{{item.suburb}}</span><br>
            <span>Check in date:{{item.check_in_date}}</span><br>
            <span>Check out date:{{item.check_out_date}}</span><br>-->
          </a-list-item>
        </a-list>
      </div>
    </a-spin>

    <!--The reservations finished-->
    <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Completed Reservations</h2>
    </div>
    <a-spin :spinning="spinning2" tip="Loading...">
      <div v-show="havenoresult2">
        <h2>No Completed Reservations</h2>
      </div>
      <div style="text-align: left;margin-bottom: 20px" v-show="haveresult2">
        <a-list
          class="comment-list"
          itemLayout="vertical"
          :grid="{ gutter: 16, column: 2 }"
          :dataSource="in_check_out"
          :pagination="pagination"
        >
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-card
              style="width: 300px;margin: 16px"
            >
              <template class="ant-card-actions" slot="actions">
                <p @click="detailed(item.accommodation_id)">Details</p>
              </template>
              <a-icon type="user" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.guest_name}}</p>
              <div style="clear: left"></div>
              <a-icon type="contacts" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.guest_contact}}</p>
              <div style="clear: left"></div>
              <a-icon type="home" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px;text-overflow:ellipsis;white-space:nowrap;overflow: hidden;width: 70%">{{item.accommodation_name}}</p>
              <div style="clear: left"></div>
              <a-icon type="environment" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.suburb}}</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-right" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_in_date}}</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-left" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_out_date}}</p>
              <div style="clear: left"></div>
              <div style="clear: left"></div>
            </a-card>
          </a-list-item>
        </a-list>
      </div>
    </a-spin>

    <!--The reservations be canceled-->
    <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Cancelled Reservations</h2>
    </div>
    <a-spin :spinning="spinning3" tip="Loading...">
      <div v-show="havenoresult3">
        <h2>No Cancelled Reservations</h2>
      </div>
      <div style="text-align: left;margin-bottom: 20px" v-show="haveresult3">
        <a-list
          class="comment-list"
          itemLayout="vertical"
          :grid="{ gutter: 16, column: 2 }"
          :dataSource="in_cancelled"
          :pagination="pagination"
        >
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-card
              style="width: 300px;margin: 16px"
            >
              <template class="ant-card-actions" slot="actions">
                <p @click="detailed(item.accommodation_id)">Details</p>
              </template>
              <a-icon type="user" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.guest_name}}</p>
              <div style="clear: left"></div>
              <a-icon type="contacts" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.guest_contact}}</p>
              <div style="clear: left"></div>
              <a-icon type="home" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px;text-overflow:ellipsis;white-space:nowrap;overflow: hidden;width: 70%">{{item.accommodation_name}}</p>
              <div style="clear: left"></div>
              <a-icon type="environment" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.suburb}}</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-right" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_in_date}}</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-left" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_out_date}}</p>
              <div style="clear: left"></div>
              <div style="clear: left"></div>
            </a-card>
          </a-list-item>
        </a-list>
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
  import moment from 'moment'
  import Cookies from 'js-cookie'

  export default {
    data() {
      return {
        moment,
        pagination: {
          pageSize: 2,
          showTotal: total => total > 1 ? total + ' reservations' : total + ' reservation'
        },
        in_process: '',
        in_check_out: '',
        in_cancelled: '',
        spinning1: true,
        spinning2: true,
        spinning3: true,
        visible: false,
        wrong_msg: '',
        havenoresult1: false,
        haveresult1: false,
        havenoresult2: false,
        haveresult2: false,
        havenoresult3: false,
        haveresult3: false,
      }
    },
    methods: {
      handleOk() {
        this.visible = false
      },
      check_out(index, id) {
        this.axios.put('/api/reservation/' + id, {
          token: Cookies.get('token'),
          status: "checked_out"
        }).then((response) => {
          this.spinning1 = false
          if (response.status === 200) {
            alert(response.data.msg)
            this.in_process.splice(index, 1)
            if (this.in_process.length === 0) {
              this.havenoresult1 = true
              this.haveresult1 = false
            } else {
              this.havenoresult1 = false
              this.haveresult1 = true
            }
          } else {
            console.log(response.data.msg)
          }
        }).catch((e) => {
          this.spinning1 = false
          if (e.response.data["msg"]) {
            console.log(e.response.data['msg'])
          } else if (e.response.data['errors']) {
            console.log(e.response.data['errors'])
          } else {
            console.log("Bad request")
          }
        })
      },
      detailed(id) {
        this.$router.push({
          name: 'DetailPage',
          params: {accomodation_id:id}
        })
      },
    },
    mounted() {
      /*when load the page, get reservation information*/
      this.axios.get('/api/user/reservations', {
        params: {
          token: Cookies.get('token'),
          filter: 'In_Process'
        }
      }).then((response) => {
        if (response.data.msg !== 'No reservation found' && response.status === 200) {
          this.in_process = response.data.msg
          if (this.in_process.length === 0) {
            this.havenoresult1 = true
            this.haveresult1 = false
          } else {
            this.havenoresult1 = false
            this.haveresult1 = true
          }
        } else {
          /*this.visible = true
          this.wrong_msg = response.data.msg*/
          this.havenoresult1 = true
          this.haveresult1 = false
        }
        this.spinning1 = false
      }).catch((e) => {
        this.spinning1 = false
        this.havenoresult1 = true
        this.haveresult1 = false
        //this.visible = true
        //this.wrong_msg = e.response.data['msg']
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }

      })

      //get check_out
      this.axios.get('/api/user/reservations', {
        params: {
          token: Cookies.get('token'),
          filter: 'Checked_Out'
        }
      }).then((response) => {
        if (response.data.msg !== 'No reservation found' && response.status === 200) {
          this.in_check_out = response.data.msg
          if (this.in_check_out.length === 0) {
            this.havenoresult2 = true
            this.haveresult2 = false
          } else {
            this.havenoresult2 = false
            this.haveresult2 = true
          }
        } else {
          this.havenoresult2 = true
          this.haveresult2 = false
          /*this.visible = true
          this.wrong_msg = response.data.msg*/
        }
        this.spinning2 = false
      }).catch((e) => {
        this.spinning2 = false
        this.havenoresult2 = true
        this.haveresult2 = false
        /*this.visible = true
        this.wrong_msg = e.response.data['msg']*/
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }
      })
      //get cancelled
      this.axios.get('/api/user/reservations', {
        params: {
          token: Cookies.get('token'),
          filter: 'Cancelled'
        }
      }).then((response) => {
        if (response.data.msg !== 'No reservation found' && response.status === 200) {
          this.in_cancelled = response.data.msg
          if (this.in_cancelled.length === 0) {
            this.havenoresult3 = true
            this.haveresult3 = false
          } else {
            this.havenoresult3 = false
            this.haveresult3 = true
          }
        } else {
          /* this.visible = true
           this.wrong_msg = response.data.msg*/
          this.havenoresult3 = true
          this.haveresult3 = false
        }
        this.spinning3 = false
      }).catch((e) => {
        this.spinning3 = false
        this.havenoresult3 = true
        this.haveresult3 = false
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }
        /*this.visible = true
        this.wrong_msg = e.response.data['msg']*/
      })
    }
  }
</script>

<style scoped>

</style>
