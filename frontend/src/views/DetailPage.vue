<template>
  <div>
    <a-spin :spinning="spinning" tip="Loading...">
    <div style="margin-left: 5%;margin-right: 5%">
      <login-header style="float: right;width: 50%;"></login-header>
      <!--to clear the float-->
      <div style="clear: both"></div>
    </div>
    <div class="view_photos" style="margin-left: 5%;margin-right: 5%;width: 90%">

      <div style="float:left;width: 50%">
        <img class="detailImage" :src="this.detail_info.image_urls[0]"
             style="width: 100%;height: 250px;background-size: cover;">
      </div>
      <div style="float:right;width: 50%">
        <div>
          <div style="float:left;width:50%">
            <img class="detailImage" :src="this.detail_info.image_urls[1]"
                 style="width:100%;height:125px;background-size: cover;">
          </div>
          <div style="float:right;width:50%">
            <img class="detailImage" :src="this.detail_info.image_urls[2]"
                 style="width:100%;height:125px;background-size: cover;">
          </div>
          <div style="clear: both"></div>
        </div>
        <div>
          <div style="float:left;width:50%">
            <img class="detailImage" :src="this.detail_info.image_urls[3]"
                 style="width:100%;height:125px;background-size: cover;">
          </div>
          <div style="float:right;width:50%">
            <img class="detailImage" :src="this.detail_info.image_urls[4]"
                 style="width:100%;height:125px;background-size: cover;">
          </div>
          <div style="clear: both"></div>
        </div>
      </div>
      <div style="clear: both"></div>
    </div>
    <!--on the left is information about the house,on the right is the booking option-->
    <div style="margin-top: 50px;margin-left: 15%;margin-right: 15%;text-align: left;float: right">
      <!--left-->
      <div style="width: 58%;float: left">
        <div>
          <h1>{{this.detail_info.name}}</h1>
          <h3>{{this.detail_info.suburb}}</h3>
        </div>

        <!--house information-->
        <div style="padding-top: 15px;width: 100%">
          <a-icon style="float: left;margin-right: 10px" type="home"/>
          <h4 style="margin-left: 30px">Entire house</h4>
          <div>
            <h4>
              <div class="houseinfo">{{this.detail_info.num_guests}} {{detail_info.num_guests > 1 ? 'guests' : 'guest'}}</div>
              <div class="houseinfo">{{this.detail_info.num_bedrooms}} {{detail_info.num_bedrooms > 1 ? 'bedrooms' : 'bedroom'}}</div>
              <div class="houseinfo">{{this.detail_info.num_beds}} {{detail_info.num_beds > 1 ? 'beds' : 'bed'}}</div>
              <div class="houseinfo">{{this.detail_info.num_bathrooms}} {{detail_info.num_bathrooms > 1 ? 'baths' : 'bath'}}</div>
            </h4>
          </div>
        </div>

        <!--line-->
        <div style="margin-top: 55px">
          <a-divider/>
        </div>

        <!--information part-->
        <div style="width: 100%">
          <h2 style="margin-top: 20px;">Description</h2>
          <p>{{this.detail_info.description}}</p>
          <!--<a-collapse :bordered="false">
            <a-collapse-panel header="More information">
              <p>text</p>
            </a-collapse-panel>
          </a-collapse>-->
          <!--line-->
          <a-divider style="margin-top: 15px"/>
        </div>

        <!--Amenities-->
        <div style="width: 100%">
          <h2 style="margin-top: 20px;">Amenities</h2>
          <div>
            <div style="float:left;width:50%;margin-top: 15px">
              <span>{{this.detail_info.amenities[0]}}</span>
            </div>
            <div style="float:right;width:50%;margin-top: 15px">
              <span>{{this.detail_info.amenities[1]}}</span>
            </div>
          </div>

          <div>
            <div style="float:left;width:50%;margin-top: 15px;">
              <span>{{this.detail_info.amenities[2]}}</span>
            </div>
            <div style="float:right;width:50%;margin-top: 15px;">
              <span>{{this.detail_info.amenities[3]}}</span>
            </div>
          </div>

          <div>
            <div style="float:left;width:50%;margin-top: 15px;margin-bottom: 20px">
              <span>{{this.detail_info.amenities[4]}}</span>
            </div>
            <div style="float:right;width:50%;margin-top: 15px;margin-bottom: 20px">
              <a-button @click="show_more"><a-icon type="plus-circle"/>More</a-button>
            </div>
          </div>
          <!--line-->
          <a-divider style="margin-top: 15px"/>
        </div>

      <!--  &lt;!&ndash;reviews&ndash;&gt;
        <div style="margin-top: 10px;">
          <h2>{{all_reviews.length}} review(s)</h2>
          <a-rate :defaultValue="this.detail_info.rating" allowHalf disabled/>
          <a-divider/>
        </div>-->
        <!--review rate-->
        <div style="width: 100%">
          <h2>Rating</h2>
          <div>
            <div style="float:left;width:50%;margin-top: 15px">
              <div style="float:left;width: 45%">
                <h3>Accuracy</h3>
              </div>
              <div style="float:right;width:55%;">
                <a-rate :defaultValue="2.5" allowHalf disabled v-model="this.detail_info.scores_accuracy"/>
              </div>
            </div>
            <div style="float:right;width:50%;margin-top: 15px">
              <div style="float:left;width: 45%">
                <h3>Location</h3>
              </div>
              <div style="float:right;width:55%;">
                <a-rate :defaultValue="2.5" allowHalf disabled v-model="this.detail_info.scores_location"/>
              </div>
            </div>
          </div>

          <div>
            <div style="float:left;width:50%;margin-top: 15px">
              <div style="float:left;width: 45%">
                <h3>Communication</h3>
              </div>
              <div style="float:right;width:55%;">
                <a-rate :defaultValue="2.5" allowHalf disabled v-model="this.detail_info.scores_communication"/>
              </div>
            </div>
            <div style="float:right;width:50%;margin-top: 15px">
              <div style="float:left;width: 45%">
                <h3>Check-in</h3>
              </div>
              <div style="float:right;width:55%;">
                <a-rate :defaultValue="2.5" allowHalf disabled v-model="this.detail_info.scores_check_in"/>
              </div>
            </div>
          </div>

          <div>
            <div style="float:left;width:50%;margin-top: 15px;margin-bottom: 20px">
              <div style="float:left;width: 45%">
                <h3>Cleanliness</h3>
              </div>
              <div style="float:right;width:55%;">
                <a-rate :defaultValue="2.5" allowHalf disabled v-model="this.detail_info.scores_cleanliness"/>
              </div>
            </div>
            <div style="float:right;width:50%;margin-top: 15px;margin-bottom: 20px">
              <div style="float:left;width: 45%">
                <h3>Value</h3>
              </div>
              <div style="float:right;width:55%;">
                <a-rate :defaultValue="2.5" allowHalf disabled v-model="this.detail_info.scores_value"/>
              </div>
            </div>
          </div>
          <!--line-->
          <a-divider style="margin-top: 15px"/>
        </div>
        <div style="width: 100%">
          <h2>Reviews</h2>
          <a-button @click="show_all">All reviews</a-button>
          <a-button @click="show_good">Good reviews</a-button>
          <a-button @click="show_bad">Bad reviews</a-button>
        </div>
        <!--review-->
        <div v-show="havenoresult" style="margin-top: 20px;width: 100%">
          <h2>No reviews!</h2>
        </div>
        <div v-show="haveresult" style="margin-top: 20px;width: 100%">
          <a-list
            style="margin-bottom: 50px"
            class="comment-list"
            :header="`${all_reviews.length} ${all_reviews.length > 1 ? 'reviews' : 'review'}`"
            itemLayout="horizontal"
            :dataSource="all_reviews"
            :pagination="pagination"
            v-show="show_all_flag"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a-comment
                :author="item.guest_name"
              >
                <template slot="actions">
                  <a-rate allowHalf disabled :value="item.rating"/>
                </template>
                <p slot="content">{{item.review}}</p>
              </a-comment>
            </a-list-item>
          </a-list>

          <a-list
            style="margin-bottom: 50px"
            class="comment-list"
            :header="`${good_reviews.length} ${good_reviews.length > 1 ? 'reviews' : 'review'}`"
            itemLayout="horizontal"
            :dataSource="good_reviews"
            :pagination="pagination"
            v-show="show_good_flag"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a-comment
                :author="item.guest_name"
              >
                <template slot="actions">
                  <a-rate allowHalf disabled :value="item.rating"/>
                </template>
                <p slot="content">{{item.review}}</p>
              </a-comment>
            </a-list-item>
          </a-list>

          <a-list
            style="margin-bottom: 50px"
            class="comment-list"
            :header="`${bad_reviews.length} ${bad_reviews.length > 1 ? 'reviews' : 'review'}`"
            itemLayout="horizontal"
            :dataSource="bad_reviews"
            :pagination="pagination"
            v-show="show_bad_flag"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a-comment
                :author="item.guest_name"
              >
                <template slot="actions">
                  <a-rate allowHalf disabled :value="item.rating"/>
                </template>
                <p slot="content">{{item.review}}</p>
              </a-comment>
            </a-list-item>
          </a-list>
        </div>
        <a-divider style="margin-top: 15px"/>

        <!--recommendations-->
        <a-spin :spinning="spinning1" tip="Loading...">
        <h2>Recommendation</h2>
        <div style="padding: 20px;margin-top:10px;">

          <a-list
            :grid="{ gutter: 16, column: 2 }"
            :dataSource="recom_data"

          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a-card hoverable :title="item.name" v-on:click="show_detail(item.id)">
                <img
                  alt="example"
                  :src="item.image_urls[0]"
                  slot="cover"
                  style="height:150px"
                />
                <div style="text-align: left">
                  <h3>{{item.suburb}}</h3>
                  <span>{{item.price}}$/night</span><br>
                  <a-rate :defaultValue="item.rating" allowHalf disabled/>
                </div>
              </a-card>
            </a-list-item>
          </a-list>
        </div>
        </a-spin>
      </div>
      <!--right-->
      <div class="choose_right" id="right_part" :class="{'is_Fixed':isFixed}" ref="choose_right_part">
        <div style="padding: 30px;text-align: left">
          <!--price title-->
          <div>
            <div style="float: left">
              <h2>${{this.detail_info.price}}</h2>
            </div>
            <div style="float: left">
              <p>/night</p>
            </div>
          </div>
          <a-divider style="width: 95%"></a-divider>
          <!--check-in-->
          <div>
            <p>Check-in</p>
            <a-date-picker
              :disabledDate="disabledStartDate"
              :defaultValue=this.check_in_date
              format="YYYY-MM-DD"
              v-model="startValue"
              placeholder="Check-in"
              @openChange="handleStartOpenChange"
              :size="size"
              style="width: 95%"
            ></a-date-picker>
          </div>
          <!--check out-->
          <div>
            <p>Check-out</p>
            <a-date-picker
              :disabledDate="disabledEndDate"
              :defaultValue=this.check_out_date
              format="YYYY-MM-DD"
              placeholder="Check-out"
              v-model="endValue"
              :open="endOpen"
              @openChange="handleEndOpenChange"
              :size="size"
              style="width: 95%"
            ></a-date-picker>
          </div>
          <!--guests-->
          <div>
            <p>Guests</p>
            <a-select
              :size="size"
              :defaultValue=this.guestnumber
              style="width: 150px;width: 95%"
              @change="handleChangeGuests"

            >
              <a-select-option v-for="i in this.detail_info.num_guests" :key="i">
                {{i}}
              </a-select-option>
            </a-select>
          </div>
          <!--submit-->
          <div style="margin-top: 20px">
            <a-button type="primary" icon="check" :size="size" v-on:click="book" style="width: 95%">Book</a-button>
          </div>

          <div style="margin-top: 20px;text-align: center">
            <p>You won’t be charged yet</p>
            <a-divider style="width: 95%"></a-divider>
          </div>

          <div style="margin-top: 20px">
            <p>Enter dates and number of guests to see the total trip price</p>
            <a-divider style="width: 95%"></a-divider>
          </div>

        </div>
      </div>

    </div>
    <!--back to top-->
    <a-back-top :visibilityHeight="200"/>
    <a-modal
      title="Amenities"
      v-model="visible"
      @ok="handleOk"
    >
      <a-list
        :grid="{ gutter: 16, column: 2 }"
        :dataSource="this.detail_info.amenities"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <a-card ><p style="text-overflow:ellipsis;white-space:nowrap;overflow: hidden;width: 100%">{{item}}</p></a-card>
        </a-list-item>
      </a-list>
    </a-modal>
    </a-spin>
  </div>
</template>

<script>
  import LoginHeader from "./../components/LoginHeader"
  import moment from 'moment'
  import Cookies from 'js-cookie'

  export default {
    components: {LoginHeader},
    data() {
      return {
        moment,
        pagination: {
          pageSize: 3,
          showTotal: total => total > 1 ? 'Total '+total+' reviews' : 'Total '+total+' review'
        },
        isFixed: false,
        startValue: null,
        endValue: null,
        endOpen: false,
        size: 'large',
        detail_info: '',
        guestValue: '',
        offsetTop: '',
        comments: [],
        //show_image_urls:''
        good_reviews: '',
        bad_reviews: '',
        all_reviews: [],
        show_all_flag: true,
        show_good_flag: false,
        show_bad_flag: false,
        recom_data: '',
        havenoresult: false,
        haveresult: false,
        visible:false,
        spinning:false,
        spinning1:false,
      }
    },
    methods: {
      show_more(){
        this.visible = true
      },
      handleOk(){
        this.visible = false
      },
      handleScroll() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
        if (scrollTop-300 > this.offsetTop) {
          this.isFixed = true
        } else {
          this.isFixed = false
        }
      },
      /*set the date disabled*/
      disabledStartDate(startValue) {
        if (this.detail_info.unavailable_dates.includes(startValue.format('YYYY-MM-DD'))) {
          return true;
        }

        return startValue && startValue < moment().startOf('day');
      },
      /*set the date disabled*/
      disabledEndDate(endValue) {
        const startValue = this.startValue;
        if (!endValue || !startValue) {
          return endValue.valueOf() <= moment().toDate().valueOf();
        }
        if(endValue.valueOf() <= moment().toDate().valueOf()){
          return true
        }
        if(endValue.format('YYYY-MM-DD') === startValue.format('YYYY-MM-DD')){
          return true
        }
        if (this.detail_info.unavailable_dates.includes(endValue.format('YYYY-MM-DD'))) {
          return true;
        }
        return  startValue.valueOf() >= endValue.valueOf();
      },
      handleStartOpenChange(open) {
        if (!open) {
          this.endOpen = true;
        }
      },
      handleEndOpenChange(open) {
        this.endOpen = open;
      },
      handleChangeGuests(value) {
        console.log(`Selected: ${value}`);
      },
      /*book the accommodation*/
      book() {
        Cookies.set('book_accommodation_id', this.detail_info.id)
        Cookies.set('book_accommodation_name', this.detail_info.name)
        Cookies.set('book_guest_num', this.guestnumber)
        Cookies.set('location', this.detail_info.suburb)
        Cookies.set('book_price', this.detail_info.price)
        Cookies.set('book_check_in', this.check_in_date.format("YYYY-MM-DD"))
        Cookies.set('book_check_out', this.check_out_date.format("YYYY-MM-DD"))
        Cookies.set('book_day', parseInt(Math.ceil((new Date(this.check_out_date).getTime() / 1000 - parseInt(new Date(this.check_in_date).getTime() / 1000)) / 60 / 60 / 24)))
        this.$router.push('/booking')
      },
      show_all() {
        if (this.all_reviews.length === 0) {
          this.havenoresult = true
          this.haveresult = false
          this.show_all_flag = false
          this.show_good_flag = false
          this.show_bad_flag = false
        } else {
          this.havenoresult = false
          this.haveresult = true
          this.show_all_flag = true
          this.show_good_flag = false
          this.show_bad_flag = false
        }
      },
      show_good() {
        if (this.good_reviews.length === 0) {
          this.havenoresult = true
          this.haveresult = false
          this.show_all_flag = false
          this.show_good_flag = false
          this.show_bad_flag = false
        } else {
          this.havenoresult = false
          this.haveresult = true
          this.show_all_flag = false
          this.show_good_flag = true
          this.show_bad_flag = false
        }
      },
      show_bad() {
        if (this.bad_reviews.length === 0) {
          this.havenoresult = true
          this.haveresult = false
          this.show_all_flag = false
          this.show_good_flag = false
          this.show_bad_flag = false
        } else {
          this.havenoresult = false
          this.haveresult = true
          this.show_all_flag = false
          this.show_good_flag = false
          this.show_bad_flag = true
        }
      },
      //go to new accommodation
      show_detail(id){
        this.$router.replace(
          {
            name: 'Empty',
            params: {temp_id: id}
          })

      }
    },
    computed: {
      guestnumber() {
        return this.$store.state.guest_number
      },
      check_in_date() {
        if (typeof (this.$store.state.check_in_date) === 'string') {
          this.$store.state.check_in_date = moment(this.$store.state.check_in_date)
        }
        return this.$store.state.check_in_date
      },
      check_out_date() {
        if (typeof (this.$store.state.check_out_date) === 'string') {
          this.$store.state.check_out_date = moment(this.$store.state.check_out_date)
        }
        return this.$store.state.check_out_date
      },
    },
    mounted() {
      let _this = this
      _this.spinning = true
      //get the accommodation detail
      _this.axios.get('/api/accommodation/' + _this.$route.params.accomodation_id).then((response) => {
        if (response.status === 200) {
          let res = response.data
          _this.detail_info = res.msg
          _this.detail_info.price = _this.detail_info.price / 100
          _this.detail_info.rating = Math.round(_this.detail_info.rating / 2)
          _this.detail_info.scores_accuracy = Math.round(_this.detail_info.scores_accuracy / 2)
          _this.detail_info.scores_check_in = Math.round(_this.detail_info.scores_check_in / 2)
          _this.detail_info.scores_cleanliness = Math.round(_this.detail_info.scores_cleanliness / 2)
          _this.detail_info.scores_communication = Math.round(_this.detail_info.scores_communication / 2)
          _this.detail_info.scores_location = Math.round(_this.detail_info.scores_location / 2)
          _this.detail_info.scores_value = Math.round(_this.detail_info.scores_value / 2)
        }
        _this.spinning = false
      }).catch((e)=> {
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
          alert(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }
        this.$router.push('/')
        _this.spinning = false
      })
      //get the good reviews of accommodation
      _this.axios.get('/api/reviews/' + _this.$route.params.accomodation_id + '/good').then((response) => {
        _this.good_reviews = response.data.msg
        _this.good_reviews.forEach(function (c) {
          c.rating = c.rating / 2
          _this.all_reviews.push(c)
        })
        if (_this.all_reviews.length === 0) {
          _this.havenoresult = true
          _this.haveresult = false
        } else {
          _this.havenoresult = false
          _this.haveresult = true
        }
      }).catch(function (e) {
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }
        _this.havenoresult = true
        _this.haveresult = false
      })
      //get the bad reviews of accommodation
      _this.axios.get('/api/reviews/' + _this.$route.params.accomodation_id + '/bad').then((response) => {
        _this.bad_reviews = response.data.msg
        _this.bad_reviews.forEach(function (c) {
          c.rating = c.rating / 2
          _this.all_reviews.push(c)
        })
        console.log(_this.all_reviews)
        if (_this.all_reviews.length === 0) {
          _this.havenoresult = true
          _this.haveresult = false
        } else {
          _this.havenoresult = false
          _this.haveresult = true
        }
      }).catch(function (e) {
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }ri
        _this.havenoresult = true
        _this.haveresult = false
      })
      //get recommendations
      this.spinning1 = true
      this.axios.get('/api/recommendation/' + _this.$route.params.accomodation_id).then((response) => {
        console.log(response.data.msg)
        if (response.status === 200) {
          _this.recom_data = response.data.msg
          _this.recom_data.forEach(function (c) {
            c.price = c.price/100
            c.rating = c.rating/2
            console.log(c.image_urls[0])
          })
          this.spinning1 =false
        }
      }).catch((e) => {
        if (e.response.data["msg"]) {
          console.log(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          console.log(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }
        _this.spinning = false
        this.spinning1 =false
      })
      window.addEventListener('scroll', this.handleScroll)
      window.addEventListener('DOMContentLoaded', (event) => {
        //to make sure the html has been created.
        this.$nextTick(() => {
          this.offsetTop = document.querySelector("#right_part").offsetTop
          //this.getoffSetTop(document.querySelector("#right_part").offsetTop)
        })
      })
    },
    destroyed() {
      window.removeEventListener('scroll', this.handleScroll)
    },
    watch: {
      startValue(val) {
        console.log('startValue', val)
        this.$store.commit("updateCheckIn", val)
      },
      endValue(val) {
        console.log('endValue', val)
        this.$store.commit("updateCheckOut", val)
      }
    },
  }

</script>

<style scoped>
  .view_photos {
    height: 250px;
    width: 100%;
    margin-top: 20px;
    float: left;
  }

  .detailImage {
    cursor: pointer;
    transition: all 0.6s;
  }

  .detailImage:hover {
    transform: scale(1.5);
  }

  .houseinfo {
    float: left;
    margin-left: 30px;
  }

  .choose_right {
    width: 38%;
    float: right;
    border: solid 1px #e4e4e4;
  }

  .is_Fixed {
    top: 10px;
    display: inline-block; /*use display to make sure other css can be applied(to deal with position);*/
    position: fixed;
    width: 28%;
    margin-left: 30px;
    float: right
  }
</style>
