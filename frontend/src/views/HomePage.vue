<template>
  <div style="margin-left: 5%;margin-right: 5%">
    <LoginHeader></LoginHeader>
    <a-carousel autoplay style="margin-top: 30px">
      <div
        slot="prevArrow" slot-scope="props"
        class="custom-slick-arrow"
        style="left: 10px;zIndex: 1"
      >
        <a-icon type="left-circle"/>
      </div>
      <div
        slot="nextArrow" slot-scope="props"
        class="custom-slick-arrow"
        style="right: 10px"
      >
        <a-icon type="right-circle"/>
      </div>
      <div><img src="https://voith.com/aus-en/1280x300_sydney-opera-house.png"></div>
      <div><img src="http://australiatravels.net/images/inner_banner11.jpg"></div>
      <div><img src="https://promolover.com/media/t/3VSGDZg-iVhF_1280x300_Xe3lowe7.jpg"></div>
      <div><img
        src="https://www.australia.com/content/australia/en/places/sydney-and-surrounds/guide-to-sydney-harbour/jcr:content/image.adapt.1200.HIGH.jpg">
      </div>
    </a-carousel>
    <h1 style="margin-top: 30px">NSW BNB</h1>
    <h3>Find your ideal vacation home in NSW</h3>
    <div id="search-line" style="margin-top: 50px">


      <a-input size="large" placeholder="e.g. bondi beach" style="width: 200px;margin: 0 8px 8px 0;"
               v-model="inputRegion"/>

      <a-date-picker
        :disabledDate="disabledStartDate"
        format="YYYY-MM-DD"
        v-model="startValue"
        placeholder="Check-in"
        @openChange="handleStartOpenChange"
        size="large"></a-date-picker>
      <a-date-picker
        :disabledDate="disabledEndDate"
        format="YYYY-MM-DD"
        placeholder="Check-out"
        v-model="endValue"
        :open="endOpen"
        @openChange="handleEndOpenChange"
        size="large"
      ></a-date-picker>
      <a-select
        :size="size"
        defaultValue="# of guests"
        style="width: 150px"
        @change="handleChange"
      >
        <a-select-option v-for="i in 15" :key="i">
          {{i}}
        </a-select-option>
      </a-select>
      <a-button type="primary" icon="search" :size="size" v-on:click="search">Search</a-button>

    </div>
    <!--line-->
    <div style="margin-top: 55px">
      <a-divider/>
    </div>
    <a-spin :spinning="spinning" tip="Loading...">
    <!--recommendations-->
    <div style="text-align: left;margin-top: 30px">
    <h2>You may like</h2>
    </div>
    <div style="padding: 20px;margin-top:10px;">

      <a-list
        :grid="{ gutter: 16, column: 4 }"
        :dataSource="recom_data"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <a-card :title="item.name" v-on:click="show_detail(item.id)">
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

    <!--back to top-->
    <a-back-top :visibilityHeight="200"/>

  </div>

</template>

<script>
  import LoginHeader from '../components/LoginHeader'
  import moment from 'moment'
  import Cookies from 'js-cookie'

  export default {
    components: {LoginHeader},
    data() {
      return {
        startValue: null,
        endValue: null,
        endOpen: false,
        size: 'large',
        inputRegion: '',
        visible: false,
        num_guest: '',
        recom_data:'',
        spinning:false
      }
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
    methods: {
      /*set the date disabled*/
      disabledStartDate(startValue) {
        return startValue && startValue < moment().startOf('day');
      },
      /*set the date disabled*/
      disabledEndDate(endValue) {
        const startValue = this.startValue;
        if (!endValue || !startValue) {
          return endValue <= moment().toDate().valueOf();
        }
        if (endValue <= moment().toDate().valueOf()) {
          return true
        }
        if (endValue.format('YYYY-MM-DD') === startValue.format('YYYY-MM-DD')) {
          return true
        }
        return startValue >= endValue;
      },
      handleStartOpenChange(open) {
        if (!open) {
          this.endOpen = true;
        }
      },
      handleEndOpenChange(open) {
        this.endOpen = open;
      },
      handleChange(value) {
        console.log(`Selected: ${value}`);
        this.num_guest = value
        this.$store.commit("updateGuestNumber", value)
      },
      handleOk() {
        this.visible = false
      },
      /*go to search page*/
      search() {
        this.$store.commit("updateLocation", this.inputRegion)

        if (this.inputRegion !== "" && this.startValue !== null && this.endValue !== null && this.$store.state.guest_number !== "number of guest") {
          this.$router.push('/searchresult')
        } else {
          this.$warning({
            title: 'Waring',
            content: 'Please enter the appropriate query conditions',
          });
        }
      },
      show_detail(id){
        this.$router.push({
          name: 'DetailPage',
          params: {accomodation_id: id}
        })
      },
    },
    computed: {
      guestnumber() {
        return this.$store.state.guest_number
      }
    },
    mounted(){
      let _this = this
      const params = {}
      _this.spinning = true
      if(Cookies.get('user_id')){
        _this.axios.get('/api/knn_recommendation',{
          params:{
            user_id:Cookies.get('user_id')
          }
        }).then((response)=> {
          if(response.status === 200){
            _this.recom_data = response.data.msg
            _this.recom_data.forEach(function (c) {
              c.price = c.price/100
              c.rating = c.rating/2
            })
          }
          _this.spinning = false
        }).catch((e)=>{
          if (e.response.data["msg"]) {
            console.log(e.response.data['msg'])
          } else if (e.response.data['errors']) {
            console.log(e.response.data['errors'])
          } else {
            console.log("Bad request")
          }
          _this.spinning = false
        })
      }else {
        _this.axios.get('/api/knn_recommendation').then((response)=> {
          if(response.status === 200){
            _this.recom_data = response.data.msg
            _this.recom_data.forEach(function (c) {
              c.price = c.price/100
              c.rating = c.rating/2
            })
          }
          _this.spinning = false
        }).catch((e)=>{
          if (e.response.data["msg"]) {
            console.log(e.response.data['msg'])
          } else if (e.response.data['errors']) {
            console.log(e.response.data['errors'])
          } else {
            console.log("Bad request")
          }
          _this.spinning = false
        })
      }

    }
  }
</script>

<style scoped>
 /* input::placeholder {
    color: black
  }
*/
  .ant-carousel >>> .slick-slide {
    text-align: center;
    height: 300px;
    line-height: 300px;
    background: #364d79;
    overflow: hidden;
  }

  .ant-carousel >>> .custom-slick-arrow {
    width: 25px;
    height: 25px;
    font-size: 25px;
    color: #fff;
    background-color: rgba(31, 45, 61, .11);
    opacity: 0.3;
  }

  .ant-carousel >>> .custom-slick-arrow:before {
    display: none;
  }

  .ant-carousel >>> .custom-slick-arrow:hover {
    opacity: 0.5;
  }

  .ant-carousel >>> .slick-slide h3 {
    color: #fff;
  }


</style>
