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
      <div><img src="http://dingyue.nosdn.127.net/2yibhtfaEh0H7L8qIkVpYxTghx3vQT7pvgGv6TR3djUJh1524792141605.jpg"></div>
    </a-carousel>
    <h1 style="margin-top: 30px">NSW BNB</h1>
    <h3>Find your ideal hotel in NSW</h3>
    <div id="search-line" style="margin-top: 50px">


      <a-input size="large" placeholder="e.g. Kingsford" style="width: 200px;margin: 0 8px 8px 0;"
               v-model="inputRegion"/>

      <a-date-picker
        :disabledDate="disabledStartDate"
        showTime
        format="YYYY-MM-DD"
        v-model="startValue"
        placeholder="Check-in"
        @openChange="handleStartOpenChange"
        size="large"></a-date-picker>
      <a-date-picker
        :disabledDate="disabledEndDate"
        showTime
        format="YYYY-MM-DD"
        placeholder="Check-out"
        v-model="endValue"
        :open="endOpen"
        @openChange="handleEndOpenChange"
        size="large"
      ></a-date-picker>
      <a-select
        :size="size"
        defaultValue="number of guest"
        style="width: 150px"
        @change="handleChange"
      >
        <a-select-option v-for="i in 5" :key="i">
          {{i}}
        </a-select-option>
      </a-select>
      <a-button type="primary" icon="search" :size="size" v-on:click="search">Search</a-button>

    </div>

    <div style="padding: 20px;margin-top:50px;">
      <a-list
        :grid="{ gutter: 16, column: 4 }"
        :dataSource="data"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <a-card :title="item.title" v-on:click="show_detail">
            <img
              alt="example"
              :src="item.image"
              slot="cover"
            />
            <div style="text-align: left">
              <h3>{{item.name}}</h3>
              <span>{{item.price}}</span><br>
              <a-rate :defaultValue="item.rating" allowHalf disabled/>
            </div>
          </a-card>
        </a-list-item>
      </a-list>
    </div>
    <!--back to top-->
    <a-back-top  :visibilityHeight="200"/>

  </div>

</template>

<script>
  import LoginHeader from '../components/LoginHeader'

  /*const data = [
    {
      title: 'Title 1',
      image: 'https://a0.muscache.com/4ea/air/v2/pictures/6c47e064-b55a-46ce-85ec-c7a15830d69c.jpg',
      name:'name',
      price: '$100'
    },
    {
      title: 'Title 2',
      image: 'https://a0.muscache.com/4ea/air/v2/pictures/7688a6e9-dd4b-4986-a051-e4e6c7fdc2e7.jpg',
      name:'name',
      price: '$200'
    },
    {
      title: 'Title 3',
      image: 'https://a0.muscache.com/im/pictures/101834773/304fe82a_original.jpg?aki_policy=large',
      name:'name',
      price: '$300'
    },
    {
      title: 'Title 4',
      image: 'https://a0.muscache.com/im/pictures/eee320dd-8eeb-4194-8027-85cdb9492065.jpg',
      name:'name',
      price: '$400'
    },
  ]*/
  export default {
    components: {LoginHeader},
    data() {
      return {
        startValue: null,
        endValue: null,
        endOpen: false,
        size: 'large',
        data:'',
        inputRegion: '',
        acc_id:''
      }
    },
    watch: {
      startValue(val) {
        console.log('startValue', val)
        this.$store.commit("updateCheckIn",val)
      },
      endValue(val) {
        console.log('endValue', val)
        this.$store.commit("updateCheckOut",val)
      }
    },
    methods: {
      disabledStartDate(startValue) {
        const endValue = this.endValue;
        if (!startValue || !endValue) {
          return false;
        }
        return startValue.valueOf() > endValue.valueOf();
      },
      disabledEndDate(endValue) {
        const startValue = this.startValue;
        if (!endValue || !startValue) {
          return false;
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
        this.$store.commit("updateGuestNumber",value)
      },
      show_detail() {
        this.$router.push({
          name:'DetailPage',
          params:{accomodation_id:this.acc_id}
        })
      },
      search() {
        this.$router.push('/searchresult')

      }
    },
    computed:{
      guestnumber(){
        return this.$store.state.guest_number
      }
    },
    mounted() {
      let _this = this
      this.axios.get('/api/accommodation/8').then((response)=>{
        if(response.status === 200){
          let res = response.data
          console.log(res.msg)
          _this.acc_id = res.msg.id
          const data = [
            {
              title:res.msg.name,
              image:res.msg.image_urls.split(',')[1].replace("'",""),
              name:res.msg.property_type,
              price:res.msg.price/100,
              rating:res.msg.rating*0.05
            },
            {
              title:res.msg.name,
              image:res.msg.image_urls.split(',')[1].replace("'",""),
              name:res.msg.property_type,
              price:res.msg.price/100,
              rating:res.msg.rating*0.05
            },
            {
              title:res.msg.name,
              image:res.msg.image_urls.split(',')[1].replace("'",""),
              name:res.msg.property_type,
              price:res.msg.price/100,
              rating:res.msg.rating*0.05
            },
            {
              title:res.msg.name,
              image:res.msg.image_urls.split(',')[1].replace("'",""),
              name:res.msg.property_type,
              price:res.msg.price/100,
              rating:res.msg.rating*0.05
            }
          ]
          _this.data = data

        }
      }).catch(function (e) {
        console.log(e)
      })
    }
  }
</script>

<style scoped>
  input::placeholder {
    color: black
  }

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
