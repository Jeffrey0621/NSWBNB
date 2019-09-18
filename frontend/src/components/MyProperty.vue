<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">

    <!--My Property-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">My Properties</h2>
    </div>
    <a-spin :spinning="spinning" tip="Loading...">
      <div v-show="nodata">
        <h2>Sorry you do not have any properties</h2>
      </div>
      <div style="margin-bottom: 20px;text-align: left" v-show="havedata">
        <a-list
          class="demo-loadmore-list"
          itemLayout="horizontal"
          :grid="{ gutter: 16, column: 2 }"
          :dataSource="dataproperty"
          :pagination="pagination"
        >
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-card
              style="width: 300px;margin: 16px"
            >
              <template class="ant-card-actions" slot="actions">
                <a-icon type="edit" @click="edit(item)"/>
                <a-icon type="delete" @click="deleted(item)"/>
                <p @click="detailed(item)">Details</p>
              </template>
              <a-icon type="home" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px;text-overflow:ellipsis;white-space:nowrap;overflow: hidden;width: 70%" >{{item.name}}</p>
              <div style="clear: left"></div>
              <a-icon type="environment" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.suburb}}</p>
              <div style="clear: left"></div>
              <a-icon type="dollar" style="float: left;margin-top: 3px"/>
              <p style="float: left;margin-left: 10px">{{item.price}}$/night</p>
              <div style="clear: left"></div>
            </a-card>

          </a-list-item>
        </a-list>
      </div>
      <div>
        <a-button v-on:click="add_property">Add a property</a-button>
      </div>
    </a-spin>
    <a-modal
      title="Update property information"
      v-model="visible"
      @ok="handleOk"
    >
      <!--host name-->
      <div>
        <div style="width: 49%;float: left;margin-right: 2%;margin-top:30px;text-align: right;">
          <label class="text-left">Host name</label>
        </div>
        <div style="float:left;text-align: left;width: 49%">
          <a-input class="text-right" v-model="name" @change="edited"></a-input>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--number of guest-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">The number of guest can live</label>
        </div>
        <div style="float:left;text-align: left;width: 49%">
          <a-select class="text-right1" v-model="guest_number" @change="edited" :size="size">
            <a-select-option v-for="i in 5" :key="i">{{i}}</a-select-option>
          </a-select>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--number of bedroom-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">The number of bedroom</label>
        </div>
        <div style="float:left;text-align: left;width:49%">
          <a-select class="text-right1" v-model="bedroom_number" @change="edited" :size="size">
            <a-select-option v-for="i in 5" :key="i">{{i}}</a-select-option>
          </a-select>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--number of bed-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">The number of bed</label>
        </div>
        <div style="float:left;text-align: left;width: 49%">
          <a-select class="text-right1" v-model="bed_number" @change="edited" :size="size">
            <a-select-option v-for="i in 5" :key="i">{{i}}</a-select-option>
          </a-select>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--number of bathroom-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">The number of bathroom</label>
        </div>
        <div style="float:left;text-align: left;width: 49%">
          <a-select class="text-right1" v-model="bathroom_number" @change="edited" :size="size">
            <a-select-option v-for="i in 5" :key="i">{{i}}</a-select-option>
          </a-select>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--property type-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">Property type</label>
        </div>
        <div style="float:left;text-align: left;width: 49%">
          <a-select class="text-right1" v-model="property_type" @change="edited" :size="size">
            <a-select-option v-for="type in typedata" :key="type">{{type}}</a-select-option>
          </a-select>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--country-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">Country</label>
        </div>
        <div style="float:left;text-align: left;width: 49%">
          <a-select class="text-right1" @change="handleCountryChange" v-model="country" :size="size"
                    style="width: 50%;height: 40px">
            <a-select-option v-for="countrya in countrydata" :key="countrya">{{countrya}}</a-select-option>
          </a-select>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--city-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">City</label>
        </div>
        <div style="float:left;text-align: left;width: 49%">
          <a-select class="text-right1" v-model="secondcities" @change="handleStateChange" :size="size"
                    style="width: 50%;height: 40px">
            <a-select-option v-for="city in cities" :key="city">{{city}}</a-select-option>
          </a-select>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--suburb-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">Suburb</label>
        </div>
        <div style="float:left;text-align: left;width: 49%">
          <a-select class="text-right1" v-model="secondsuburbs" :size="size" @change="edited"
                    style="width: 50%;height: 40px">
            <a-select-option v-for="suburb in suburbs" :key="suburb">{{suburb}}</a-select-option>

          </a-select>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--price-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">Price</label>
        </div>
        <div style="float:left;text-align: left;width:49%">
          <a-input class="text-right" v-model="property_price" @change="edited"></a-input>
          $/night
        </div>
        <div style="clear: left"></div>
      </div>

      <!--description-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">Description</label>
        </div>
        <div style="float:left;text-align: left;width:49%">
          <textarea class="text-right" :rows="3" v-model="property_description" @change="edited"/>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--amenities-->
      <div>
        <div style="width: 49%;float: left; margin-top: 30px;margin-right:2%;text-align: right;">
          <label class="text-left">Amenities(at least 6)</label>
        </div>
        <div style="float:left;text-align: left;width:49%">
          <a-checkbox-group :options="options" @change="onChange" v-model="amenities_list" style="margin-top: 30px;width: 50%">
          </a-checkbox-group>
        </div>
        <div style="clear: left"></div>
      </div>
    </a-modal>

    <a-modal
      title="Message"
      v-model="visible1"
      @ok="handleOk1"
    >
      <p>Confirm to delete the property?</p>
    </a-modal>
  </div>
</template>

<script>
  import Cookies from 'js-cookie'

  const dataproperty = []
  const typedata = ['apartment', 'house', 'unit']
  const options = ['kitchen', 'heating', 'tv', 'hangers', 'iron', 'washer', 'dryer', 'hot water', 'hair dryer', 'air conditioning', 'private bathroom', 'private living room', 'private entrance']
  const countrydata = ['Australia']
  const citydata = {
    Australia: ['Sydney']
  }
  const suburbdata = {
    Sydney:['test','Alexandria','Annandale/Leichhardt','Arncliffe','Artarmon','Ashfield','Auburn','Avalon','Balgowlah','Balmain/Birchgrove','Bardwell Valley','Beaconsfield','Bellevue Hill','Bexley','Bondi','Bondi Beach','Bondi Junction','Botany','Brighton-Le-Sands','Bronte','Burwood','Cammeray','Camperdown','Campsie','Canterbury','Carlton','Castle Cove/Middle Cove','Castlecrag','Central Business District','Chatswood','Chippendale','Clovelly','Coogee','Cremorne','Cronulla','Crows Nest','Croydon Park','Darling Point','Darlinghurst','Darlington','Denpasar','Double Bay','Drummoyne','Dulwich Hill','Earlwood','Eastlakes','Edgecliff','Elizabeth Bay/Rushcutters Bay','Enmore','Erskineville','Fairlight','Forest Lodge','Gladesville','Glebe','Greenwich','Haberfield','Haymarket','Hillsdale/Eastgardens','Homebush','Hunters Hill','Hurlstone Park','Kensington','Killarney Heights','Kingsford','Kirribilli/Milsons Point','Kogarah','Kogarah Bay/Carss Park','Lane Cove','Lewisham','Lilyfield/Rozelle','Little Bay','Longueville','Lugarno','Malabar','Manly','Maroubra','Marrickville','Mascot','Matraville','Millers Point','Mosman','Mosman','Naremburn','Neutral Bay','Newtown','Newtown/Enmore','North Bondi','North Melbourne','North Sydney','Oatley','Paddington','Pagewood','Palm Beach','Peakhurst','Petersham','Phillip Bay','Point Piper','Potts Point','Putney','Pyrmont','Queens Park','Randwick','Redfern','Rockdale','Rose Bay/Dover Heights','Rosebery','Sans Souci','Seaforth','Silverwater/Newington','South Coogee','St Leonards','St Peters','Stanmore','Strathfield','Summer Hill','Surry Hills','Tamarama','The Rocks','Ultimo','Vaucluse/Watsons Bay','Waterloo','Waverly','Whitechapel/Brick Lane','Willoughby','Wollstonecraft/Waverton','Woollahra','Woolloomooloo','Zetland']
  }
  export default {
    data() {
      return {
        pagination: {
          pageSize: 4,
          showTotal: total => total > 1 ? total  + ' properties' : total + ' property'
        },
        spinning: true,
        dataproperty,
        nodata: false,
        havedata: false,
        visible: false,
        edit_info: '',
        edit_flag: false,
        size: 'large',
        countrydata,
        citydata,
        suburbdata,
        typedata,
        options,
        country: countrydata[0],
        cities: citydata[countrydata[0]],
        secondcities: citydata[countrydata[0]][0],
        suburbs: suburbdata[citydata[countrydata[0]][0]],
        secondsuburbs: suburbdata[citydata[countrydata[0]][0]][0],
        name: '',
        guest_number: '',
        bedroom_number: '',
        bed_number: '',
        bathroom_number: '',
        property_type: '',
        property_price: '',
        property_description: '',
        amenities: '',
        amenities_list:'',
        id: '',
        visible1: false,
        checknum:'',
      }
    },
    methods: {
      onChange(checkedValues) {
        console.log('checked = ', checkedValues)
        this.checknum = checkedValues.length
        this.amenities =  checkedValues.toString()
      },
      //delete the property
      handleOk1() {
        this.axios.delete('/api/accommodation/' + this.id, {
          data: {
            token: Cookies.get('token'),
          },
        }).then((response) => {
          alert(response.data.msg)
        }).catch((e) => {
          if (e.response.data["msg"]) {
            alert(e.response.data['msg'])
          } else if (e.response.data['errors']) {
            alert(e.response.data['errors'])
          } else {
            console.log("Bad request")
          }

        })
        this.visible1 = false
      },
      add_property() {
        this.$router.push('/addproperty')
      },
      getData(data) {
        this.dataproperty = data
      },
      /*show no data message*/
      setnodata(flag) {
        this.nodata = flag
      },
      /*show have data message*/
      sethavedata(flag) {
        this.havedata = flag
      },
      /*update property information*/
      edit(item) {
        this.edit_flag = false
        this.edit_info = item
        this.visible = true
        this.name = item.name
        this.guest_number = item.num_guests
        this.bedroom_number = item.num_bedrooms
        this.bed_number = item.num_beds
        this.bathroom_number = item.num_bathrooms
        this.property_type = item.property_type
        this.country = item.country
        this.cities = citydata[item.country]
        this.secondcities = item.city
        this.suburbs = suburbdata[item.city]
        this.secondsuburbs = item.suburb
        this.property_price = item.price
        this.property_description = item.description
        this.amenities_list = item.amenities
        console.log(this.amenities_list )
        this.id = item.id
      },
      /*something then use api to update infomation, otherwise do nothing*/
      handleOk() {
        if (this.edit_flag) {
          if(this.checknum <6){
            alert('At least 6 amenities.')
          }else {
            this.axios.put('/api/accommodation/' + this.id, {
              token: Cookies.get('token'),
              num_guests: this.num_guests,
              num_bedrooms: this.num_bedrooms,
              num_beds: this.num_beds,
              num_bathrooms: this.num_bathrooms,
              description: this.property_description,
              price: this.property_price * 100,
              property_type: this.property_type,
              country: this.country,
              city: this.secondcities,
              amenities:this.amenities,
              suburb: this.secondsuburbs,
              name: this.name,
            }).then((response) => {
              alert(response.data.msg)
            }).catch(function (e) {
              if (e.response.data["msg"]) {
                alert(e.response.data['msg'])
              } else if (e.response.data['errors']) {
                alert(e.response.data['errors'])
              } else {
                console.log("Bad request")
              }
            })
          }
        }
        this.visible = false
      },
      /*determine if it is changed*/
      edited() {
        this.edit_flag = true
      },
      //for more details
      detailed(item) {
        this.$router.push({
          name: 'DetailPage',
          params: {accomodation_id: item.id}
        })
      },
      /*if country changed,city also change*/
      handleCountryChange(value) {
        this.edit_flag = true
        this.cities = citydata[value]
        this.secondcities = citydata[value][0]
      },
      /*if city changed,suburb also change*/
      handleStateChange(value) {
        this.edit_flag = true
        this.suburbs = suburbdata[value]
        this.secondsuburbs = suburbdata[value][0]
      },
      deleted(item) {
        this.id = item.id
        this.visible1 = true
      }
    },
    mounted: function () {
      /*get accommodations information*/
      let _this = this
      _this.axios.get('/api/user/accommodations', {
        params: {
          token: Cookies.get('token'),
        }
      }).then((response) => {
        if (response.status === 200) {
          let res = response.data.msg
          res.forEach(function (c) {
            c.price = c.price / 100
          })
          this.getData(res)
          if (res.length === 0) {
            _this.setnodata(true)
            _this.sethavedata(false)
          } else {
            _this.setnodata(false)
            _this.sethavedata(true)
          }
          console.log(res)
        } else {
          alert(response.data.msg)
        }
        _this.spinning = false
      }).catch((e) => {
        _this.spinning = false
        _this.setnodata(true)
        _this.sethavedata(false)
        if (e.response.data["msg"]) {
          alert(e.response.data['msg'])
        } else if (e.response.data['errors']) {
          alert(e.response.data['errors'])
        } else {
          console.log("Bad request")
        }
      })
    }
  }
</script>

<style scoped>
  .text-right1 {
    width: 50%;
    margin-top: 30px;
    height: 40px;
    font-size: 16px;
  }

  .text-right {
    width: 50%;
    margin-top: 30px;
    height: 40px;
    padding: 8px 10px;
    border: 1px solid #aaa;
    font-size: 16px;
    border-radius: 4px;
  }
</style>
