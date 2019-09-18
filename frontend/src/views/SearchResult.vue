<template>
  <div style="margin-left: 5%;margin-right: 5%">
    <login-header></login-header>
    <div style="margin-top: 10px;text-align: left">
      <form id="test">
        <a-input size="large" style="width: 200px;margin: 0 8px 8px 0;" v-model="location"/>
      </form>
      <a-date-picker
        :disabledDate="disabledStartDate"
        :defaultValue=this.check_in_date
        format="YYYY-MM-DD"
        v-model="startValue"
        placeholder="Check-in"
        @openChange="handleStartOpenChange"
        size="large"></a-date-picker>
      <a-date-picker
        :disabledDate="disabledEndDate"
        :defaultValue=this.check_out_date
        format="YYYY-MM-DD"
        placeholder="Check-out"
        v-model="endValue"
        :open="endOpen"
        @openChange="handleEndOpenChange"
        size="large"></a-date-picker>
      <a-select
        :size="size"
        :defaultValue=this.guestnumber
        style="width: 150px"
        @change="handleChange"
      >
        <a-select-option v-for="i in 5" :key="i">
          {{i}}
        </a-select-option>
      </a-select>

      <a-button type="primary" :size="size" @click="showDrawer">
        More filters
      </a-button>
      <a-button type="primary" :size="size" @click="searchagain">
        Search
      </a-button>
      <!--more filters-->
      <a-drawer
        title="More filters"
        placement="right"
        :closable="false"
        @close="onClose"
        :visible="visible"
      >
        <!--<p>sort</p>
        <a-radio-group :options="sortOptions" @change="onsortChange" :defaultValue="value1"/>
        <a-divider/>-->

        <p>price</p>
        <a-slider range :step="50" :max="1500" @change="onrangeChange" @afterChange="onAfterChange"/>
        <a-divider/>

        <p>bedrooms</p>
        <a-row>
          <a-col :span="12">
            <a-slider :min="0" :max="4" v-model="bedroomnumber"/>
          </a-col>
          <a-col :span="4">
            <a-input-number
              :min="0"
              :max="4"
              style="marginLeft: 8px"
              v-model="bedroomnumber"
            />
          </a-col>
        </a-row>
        <a-divider/>

        <p>bed</p>
        <a-row>
          <a-col :span="12">
            <a-slider :min="0" :max="8" v-model="bednumber"/>
          </a-col>
          <a-col :span="4">
            <a-input-number
              :min="0"
              :max="8"
              style="marginLeft: 8px"
              v-model="bednumber"
            />
          </a-col>
        </a-row>
        <a-divider/>

        <p>bath</p>
        <a-row>
          <a-col :span="12">
            <a-slider :step="0.5" :min="0" :max="3" v-model="bathnumber"/>
          </a-col>
          <a-col :span="4">
            <a-input-number
              :step="0.5"
              :min="0"
              :max="3"
              style="marginLeft: 8px"
              v-model="bathnumber"
            />
          </a-col>
        </a-row>
        <a-divider/>

        <p>Amenities</p>
        <a-checkbox-group :options="options" @change="onoptionsChange"></a-checkbox-group>
        <a-divider/>

      </a-drawer>
      <a-divider/>
    </div>
    <a-spin :spinning="spinning" tip="Loading...">
      <div v-show="havenoresult">
        <h2>No results!Please search again</h2>
      </div>
      <!--data of accommodation-->
      <div style="margin-top: 20px;margin-bottom: 80px" v-show="haveresult">
        <!--<div v-for="item in usermsg.slice((currentpage-1)*2,currentpage*2)">
          <p>{{item.username}}</p>
          <p>{{item.date}}</p>
        </div>
        <div>
          <span v-if="currentpage>1" @click="currentpage&#45;&#45;">pre</span>
          <span>{{currentpage}}</span>/<span>{{pagesum}}</span>
          <span v-if="currentpage<pagesum" @click="currentpage++">next</span>
        </div>-->
        <a-list
          itemLayout="vertical"
          size="large"
          :pagination="pagination"
          :dataSource="data1"
        >
          <a-list-item slot="renderItem" slot-scope="item, index" key="item.name" style="text-align: left"
                       @click="for_detail(item.id)">
            <img slot="extra" width="272" alt="logo" :src="item.image_urls"/>

            <a-list-item-meta
              :description="item.description"
            >
              <a slot="title">{{item.name}}</a>

            </a-list-item-meta>

            ${{item.price}}<br>
            <a-rate :defaultValue="parseInt(item.rating)" disabled allowHalf></a-rate>
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

  const options = ['Kitchen', 'Heating', 'Tv', 'Hangers', 'Iron', 'Washer', 'Dryer', 'Hot water', 'Hair dryer', 'Air conditioning', 'Private bathroom', 'Private living room', 'Private entrance']
  const sortOptions = [
    {label: 'low to high', value: 'increase'},
    {label: 'high to low', value: 'decrease'}
  ]
  const data1 = []

  export default {
    components: {
      LoginHeader: LoginHeader
    },
    data() {
      return {
        startValue: null,
        endValue: null,
        endOpen: false,
        size: 'large',
        visible: false,
        bedroomnumber: 0,
        bednumber: 0,
        bathnumber: 0,
        Amenitylist: null,
        value1: "increase",
        location: this.$store.state.location,
        sortOptions,
        options,
        data1,
        spinning: true,
        pagination: {
          pageSize: 3,
          showTotal: total => total > 1 ? total + ' results' : total +  ' result'

        },
        price_low: 0,
        price_high: 100000,
        havenoresult: false,
        haveresult: false,
        searchDetail: {}
      }
    },
    methods: {
      onsortChange(e) {
        console.log('radio1 checked', e.target.value)
      },
      onoptionsChange(checkedValues) {
        console.log('checked = ', checkedValues.toString())
        this.$store.commit("updateAmenities", checkedValues.toString())
      },
      onrangeChange(value) {
        console.log('changerange: ', value);
      },
      onAfterChange(value) {
        this.price_low = value[0] * 100
        this.price_high = value[1] * 100
      },
      showDrawer() {
        this.visible = true
      },
      onClose() {
        this.visible = false
      },
      /*set the date disabled*/
      disabledStartDate(startValue) {
        const endValue = this.endValue;
        if (!startValue || !endValue) {
          return startValue.valueOf() <= (moment().toDate().valueOf() - 24 * 60 * 60 * 1000)
        }
        if (startValue.valueOf() <= (moment().toDate().valueOf() - 24 * 60 * 60 * 1000)) {
          return true
        }
        return startValue.valueOf() > endValue.valueOf();
      },
      /*set the date disabled*/
      disabledEndDate(endValue) {
        const startValue = this.startValue;
        if (!endValue || !startValue) {
          return endValue.valueOf() <= moment().toDate().valueOf();
        }
        if (endValue.valueOf() <= moment().toDate().valueOf()) {
          return true
        }
        if (endValue.format('YYYY-MM-DD') === startValue.format('YYYY-MM-DD')) {
          return true
        }
        return startValue.valueOf() >= endValue.valueOf();
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
        this.$store.commit("updateGuestNumber", value)
      },
      /*go to detail page*/
      for_detail(id) {
        //this.$router.push('/detailpage')
        this.$router.push({
          name: 'DetailPage',
          params: {accomodation_id: id}
        })
      },
      /*get new result*/
      searchagain() {
        this.spinning = true
        this.haveresult = false
        this.havenoresult = false
        this.$store.commit("updateLocation", this.location)
        let _this = this
        if (typeof (_this.$store.state.check_in_date) === 'string') {
          _this.$store.state.check_in_date = moment(_this.$store.state.check_in_date)
          _this.$store.state.check_out_date = moment(_this.$store.state.check_out_date)
        }
        if (_this.$store.state.amenities === '') {
          _this.axios.get("/api/search", {
            params: {
              location: _this.$store.state.location,
              check_in: _this.$store.state.check_in_date.format("YYYY-MM-DD"),
              check_out: _this.$store.state.check_out_date.format("YYYY-MM-DD"),
              num_guests: _this.$store.state.guest_number,
              price_low: this.price_low,
              price_high: this.price_high,
              num_bedrooms: this.bedroomnumber,
              num_beds: this.bednumber,
              num_bathrooms: this.bathnumber
            }
          }).then((response) => {
            if (response.status === 200) {
              _this.data1 = response.data.msg
              _this.data1.forEach(function (tmp) {
                tmp.price = parseInt(tmp.price) / 100
                tmp.rating = Math.round(parseInt(tmp.rating) / 2)
                tmp.image_urls = tmp.image_urls[0]
              })
              _this.spinning = false
              if (_this.data1.length === 0) {
                _this.haveresult = false
                _this.havenoresult = true
              } else {
                _this.haveresult = true
                _this.havenoresult = false
              }
            }
          }).catch(function (e) {
            _this.spinning = false
            _this.haveresult = false
            _this.havenoresult = true
            if (e.response.data["msg"]) {
              console.log(e.response.data['msg'])
            } else if (e.response.data['errors']) {
              console.log(e.response.data['errors'])
            } else {
              console.log("Bad request")
            }
          })
        } else {
          _this.axios.get("/api/search", {
            params: {
              location: _this.$store.state.location,
              check_in: _this.$store.state.check_in_date.format("YYYY-MM-DD"),
              check_out: _this.$store.state.check_out_date.format("YYYY-MM-DD"),
              num_guests: _this.$store.state.guest_number,
              amenities: _this.$store.state.amenities,
              price_low: _this.price_low,
              price_high: _this.price_high,
              num_bedrooms: _this.bedroomnumber,
              num_beds: _this.bednumber,
              num_bathrooms: _this.bathnumber
            }
          }).then((response) => {
            if (response.status === 200) {
              _this.data1 = response.data.msg
              _this.data1.forEach(function (tmp) {
                tmp.price = parseInt(tmp.price) / 100
                tmp.rating = Math.round(parseInt(tmp.rating) / 2)
                tmp.image_urls = tmp.image_urls[0]
              })
              //tmp.image_urls = tmp.image_urls.replace('/]/g',"").replace('/[/g',"").replace(/'/g,"").split(',')[1]
              _this.spinning = false
              if (_this.data1.length === 0) {
                _this.haveresult = false
                _this.havenoresult = true
              } else {
                _this.haveresult = true
                _this.havenoresult = false
              }
            }
            console.log(response.data)
          }).catch((e) => {
            _this.spinning = false
            _this.haveresult = false
            _this.havenoresult = true
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
      inputRegion() {
        return this.$store.state.location
      },
    },
    mounted() {
      /*get the search result*/
      let _this = this
      if (typeof (_this.$store.state.check_in_date) === 'string') {
        _this.$store.state.check_in_date = moment(_this.$store.state.check_in_date)
        _this.$store.state.check_out_date = moment(_this.$store.state.check_out_date)
      }
      _this.axios.get("/api/search", {
        params: {
          location: _this.$store.state.location,
          check_in: _this.$store.state.check_in_date.format("YYYY-MM-DD"),
          check_out: _this.$store.state.check_out_date.format("YYYY-MM-DD"),
          num_guests: _this.$store.state.guest_number,
        }
      }).then((response) => {
        console.log(response.data)
        if (response.status === 200) {
          _this.data1 = response.data.msg
          _this.data1.forEach(function (tmp) {
            tmp.price = parseInt(tmp.price) / 100
            if (tmp.rating === 'NaN') {
              tmp.rating = 0
            } else {
              tmp.rating = Math.round(parseInt(tmp.rating) / 2)
            }
            if (tmp.image_urls !== 'None') {
              //tmp.image_urls = tmp.image_urls.split(',')[1].replace("'","").replace("'","")
              tmp.image_urls = tmp.image_urls[0]
            }
          })
          _this.spinning = false
          if (_this.data1.length === 0) {
            _this.haveresult = false
            _this.havenoresult = true

          } else {
            _this.haveresult = true
            _this.havenoresult = false
          }
        }

      }).catch(function (e) {
        _this.spinning = false
        _this.haveresult = false
        _this.havenoresult = true
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
  input::placeholder {
    color: black
  }

</style>
