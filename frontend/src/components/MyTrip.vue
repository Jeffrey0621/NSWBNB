<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--Coming trip-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Upcoming Trips</h2>
    </div>
    <a-spin :spinning="spinning1" tip="Loading...">
      <div v-show="havenoresult1">
        <h2>No upcoming trips. Please make a booking and start your new trip!</h2>
      </div>
      <div style="margin-bottom: 20px;text-align: left" v-show="haveresult1">
        <a-list
          class="demo-loadmore-list"
          itemLayout="horizontal"
          :dataSource="datafuture"
          :pagination="pagination"
        >
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a slot="actions" @click="cancel(index,item.reservation_id)">Cancel</a>
            <a slot="actions" @click="detailed(item)">Details</a>
            <a-list-item-meta
              :description="item.suburb"
            >
              <a slot="title">{{item.accommodation_name}}</a>

            </a-list-item-meta>
            ${{item.price}}/night <br> {{item.check_in}}-{{item.check_out}}
          </a-list-item>
        </a-list>
      </div>
    </a-spin>


    <!--Current Trips-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Current Trips</h2>
    </div>
    <a-spin :spinning="spinning3" tip="Loading...">
      <div v-show="havenoresult3">
        <h2>No current trips.</h2>
      </div>
      <div style="margin-bottom: 20px;text-align: left" v-show="haveresult3">
        <a-list
          class="demo-loadmore-list"
          itemLayout="horizontal"
          :grid="{ gutter: 16, column: 2 }"
          :dataSource="datacurrent"
          :pagination="pagination"
        >
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-card
              style="width: 300px;margin: 16px"
            >
              <template class="ant-card-actions" slot="actions">
                <p @click="detailed(item)">Details</p>
              </template>
              <a-icon type="home" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px;text-overflow:ellipsis;white-space:nowrap;overflow: hidden;width: 70%">{{item.accommodation_name}}</p>
              <div style="clear: left"></div>
              <a-icon type="environment" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.suburb}}</p>
              <div style="clear: left"></div>
              <a-icon type="dollar" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.price}}$/night</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-right" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_in}}</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-left" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_out}}</p>
              <div style="clear: left"></div>
            </a-card>

          </a-list-item>
        </a-list>

      </div>
    </a-spin>


    <!--Past Trips-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Past Trips</h2>
    </div>
    <a-spin :spinning="spinning2" tip="Loading...">
      <div v-show="havenoresult2">
        <h2>No past trips.Please make a booking and start your new trip!</h2>
      </div>
      <div style="margin-bottom: 20px;text-align: left" v-show="haveresult2">
        <a-list
          class="demo-loadmore-list"
          itemLayout="horizontal"
          :grid="{ gutter: 16, column: 2 }"
          :dataSource="datapast"
          :pagination="pagination"
        >
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-card
              style="width: 300px;margin: 16px"
            >
              <template class="ant-card-actions" slot="actions">
                <a-icon type="edit" @click="write_review(item.reservation_id)"/>
                <p @click="detailed(item)">Details</p>
              </template>
              <a-icon type="home" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px;text-overflow:ellipsis;white-space:nowrap;overflow: hidden;width: 70%">{{item.accommodation_name}}</p>
              <div style="clear: left"></div>
              <a-icon type="environment" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.suburb}}</p>
              <div style="clear: left"></div>
              <a-icon type="dollar" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.price}}$/night</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-right" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_in}}</p>
              <div style="clear: left"></div>
              <a-icon type="arrow-left" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.check_out}}</p>
              <div style="clear: left"></div>
            </a-card>

          </a-list-item>
        </a-list>

      </div>
    </a-spin>

    <!--write review window-->
    <a-modal
      title="Write review"
      v-model="visible"
      @ok="handleOk"
    >
      <div style="margin-top: 15px">
        <div style="float:left;width: 45%;text-align: right;margin-right: 5%">
          <h3>Accuracy</h3>
        </div>
        <div style="float:right;width:50%;">
          <a-rate :defaultValue="5" allowHalf @change="onAccuracy" :value="accuracy"/>
        </div>
        <div style="clear: both"></div>
      </div>

      <div style="margin-top: 15px">
        <div style="float:left;width: 45%;text-align: right;margin-right: 5%">
          <h3>Location</h3>
        </div>
        <div style="float:right;width:50%;">
          <a-rate :defaultValue="5" allowHalf @change="onLocation" :value="location"/>
        </div>
        <div style="clear: both"></div>
      </div>

      <div style="margin-top: 15px">
        <div style="float:left;width: 45%;text-align: right;margin-right: 5%">
          <h3>Communication</h3>
        </div>
        <div style="float:right;width:50%;">
          <a-rate :defaultValue="5" allowHalf @change="onCommunication" :value="communication"/>
        </div>
        <div style="clear: both"></div>
      </div>

      <div style="margin-top: 15px">
        <div style="float:left;width: 45%;text-align: right;margin-right: 5%">
          <h3>Check-in</h3>
        </div>
        <div style="float:right;width:50%;">
          <a-rate :defaultValue="5" allowHalf @change="onCheckin" :value="checkin"/>
        </div>
        <div style="clear: both"></div>
      </div>

      <div style="margin-top: 15px">
        <div style="float:left;width: 45%;text-align: right;margin-right: 5%">
          <h3>Cleanliness</h3>
        </div>
        <div style="float:right;width:50%;">
          <a-rate :defaultValue="5" allowHalf @change="onCleanliness" :value="cleanliness"/>
        </div>
        <div style="clear: both"></div>
      </div>

      <div style="margin-top: 15px">
        <div style="float:left;width: 45%;text-align: right;margin-right: 5%">
          <h3>Value</h3>
        </div>
        <div style="float:right;width:50%;">
          <a-rate :defaultValue="5" allowHalf @change="onValue" :value="onvalue"/>
        </div>
        <div style="clear: both"></div>
      </div>


      <div style="margin-top: 15px">
        <a-comment>
          <div slot="content" style="width: 100%">
            <a-form-item>
              <a-textarea :rows="4" @change="handleChange" :value="review_content"></a-textarea>
            </a-form-item>
          </div>
        </a-comment>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import Cookies from 'js-cookie'

  const datapast = []
  const datafuture = []
  const datacurrent = []
  export default {
    data() {
      return {
        datapast,
        datafuture,
        datacurrent,
        visible: false,
        pagination: {
          pageSize: 4,
          showTotal: total => total > 1 ? total + ' trips' : total + ' trip'
        },
        review_content: '',
        review_reservation_id: '',
        accuracy: 5,
        location: 5,
        communication: 5,
        checkin: 5,
        cleanliness: 5,
        onvalue: 5,
        spinning1: true,
        spinning2: true,
        spinning3: true,
        havenoresult1: false,
        haveresult1: false,
        havenoresult2: false,
        haveresult2: false,
        havenoresult3: false,
        haveresult3: false
      }
    },
    methods: {
      //for more details
      detailed(item) {
        this.$router.push({
          name: 'DetailPage',
          params: {accomodation_id: item.accommodation_id}
        })
      },
      /*cancel the booking*/
      cancel: function (index, id) {
        this.spinning1 = true
        const userinfo1 = JSON.parse(sessionStorage.getItem('userinfo'))
        this.axios.put('/api/reservation/' + id, {
          token: Cookies.get('token'),
          status: "cancelled"
        }).then((response) => {
          this.spinning1 = false
          if (response.status === 200) {
            alert(response.data.msg)
            this.datafuture.splice(index, 1)
            if (this.datafuture.length === 0) {
              this.havenoresult1 = true
              this.haveresult1 = false
            } else {
              this.havenoresult1 = false
              this.haveresult1 = true
            }
          } else {
            alert(response.data.msg)
          }
        }).catch((e) => {
          this.spinning1 = false
          if (e.response.data["msg"]) {
            alert(e.response.data['msg'])
          } else if (e.response.data['errors']) {
            alert(e.response.data['errors'])
          } else {
            console.log("Bad request")
          }
        })
      },
      /*write the review*/
      write_review: function (id) {
        this.review_reservation_id = id
        this.visible = true
      },
      /*use api to create review*/
      handleOk(e) {
        console.log(this.review_reservation_id)
        console.log(this.cleanliness)
        this.axios.post('/api/reviews', {
          token: Cookies.get('token'),
          reservation_id: this.review_reservation_id,
          scores_accuracy: this.accuracy * 2 / 1,
          scores_location: this.location * 2 / 1,
          scores_communication: this.communication * 2 / 1,
          scores_check_in: this.checkin * 2 / 1,
          scores_cleanliness: this.cleanliness * 2 / 1,
          scores_value: this.onvalue * 2 / 1,
          review: this.review_content
        }).then((response) => {
          if (response.status === 201) {
            alert(response.data.msg)
          } else {
            alert(response.data.msg)
          }
          this.visible = false
        }).catch((e) => {
          this.visible = false
          console.log(e.response.data)
          if (e.response.data["msg"]) {
            alert(e.response.data['msg'])
          } else if (e.response.data['errors']) {
            alert(e.response.data['errors'])
          } else {
            console.log("Bad request")
          }
        })
      },
      handleChange(e) {
        this.review_content = e.target.value
        console.log(e.target.value)
      },
      onAccuracy(e) {
        this.accuracy = e
      },
      onLocation(e) {
        this.location = e
      },
      onCommunication(e) {
        this.communication = e
      },
      onCheckin(e) {
        this.checkin = e
      },
      onCleanliness(e) {
        this.cleanliness = e
      },
      onValue(e) {
        this.onvalue = e
      }

    },
    mounted() {
      /*get past reservation by token*/
      const userinfo1 = JSON.parse(sessionStorage.getItem('userinfo'))
      let _this = this
      _this.axios.get('/api/reservation', {
        params: {
          filter: 'past',
          token: Cookies.get('token'),
        }
      }).then((response) => {
        _this.datapast = response.data.msg
        if (_this.datapast.length === 0) {
          _this.havenoresult2 = true
          _this.haveresult2 = false
        } else {
          _this.havenoresult2 = false
          _this.haveresult2 = true
        }
        console.log(_this.datapast)
        _this.datapast.forEach(function (c) {
          c.price = c.price / 100
        })
        _this.spinning2 = false
      }).catch((e) => {
        _this.spinning2 = false
        _this.havenoresult2 = true
        _this.haveresult2 = false
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }
      })
      /*get current reservation by token*/
      _this.axios.get('/api/reservation', {
        params: {
          filter: 'current',
          token: Cookies.get('token'),
        }
      }).then((response) => {
        _this.datacurrent = response.data.msg
        if (_this.datacurrent.length === 0) {
          _this.havenoresult3 = true
          _this.haveresult3 = false
        } else {
          _this.havenoresult3 = false
          _this.haveresult3 = true
        }
        _this.datacurrent.forEach(function (c) {
          c.price = c.price / 100
        })
        _this.spinning3 = false
      }).catch((e) => {
        _this.spinning3 = false
        _this.havenoresult3 = true
        _this.haveresult3 = false
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }
      })
      /*get future reservation by token*/
      _this.axios.get('/api/reservation', {
        params: {
          filter: 'future',
          token: Cookies.get('token'),
        }
      }).then((response) => {
        _this.datafuture = response.data.msg
        if (_this.datafuture.length === 0) {
          _this.havenoresult1 = true
          _this.haveresult1 = false
        } else {
          _this.havenoresult1 = false
          _this.haveresult1 = true
        }
        _this.datafuture.forEach(function (c) {
          c.price = c.price / 100
        })
        _this.spinning1 = false
      }).catch((e) => {
        _this.spinning1 = false
        _this.havenoresult1 = true
        _this.haveresult1 = false
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }
      })
    }
  }
</script>

<style scoped>

</style>
