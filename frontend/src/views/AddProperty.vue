<template>
  <div>
    <login-header style="margin-bottom: 20px;margin-right: 5%"></login-header>

    <div style="padding: 50px 200px;background: #ececec">

      <div style="background: #fff;border-radius: 4px">
        <a-spin :spinning="spinning" tip="Uploading...">
          <!--host name-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Name of property</label>
            </div>
            <div style="float:left;text-align: left;width: 60%">
              <a-input class="text-right" placeholder="please name your property" v-model="host_name"></a-input>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--number of guest-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Maximum number of guests</label>
            </div>
            <div style="float:left;text-align: left;width: 60%">
              <a-select class="text-right1" v-model="guest_number" :size="size">
                <a-select-option v-for="i in 15" :key="i">{{i}}</a-select-option>
              </a-select>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--number of bedroom-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Number of bedrooms</label>
            </div>
            <div style="float:left;text-align: left;width: 60%">
              <a-select class="text-right1" v-model="bedroom_number" :size="size">
                <a-select-option v-for="i in 10" :key="i">{{i}}</a-select-option>
              </a-select>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--number of bed-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Number of beds</label>
            </div>
            <div style="float:left;text-align: left;width: 60%">
              <a-select class="text-right1" v-model="bed_number" :size="size">
                <a-select-option v-for="i in 10" :key="i">{{i}}</a-select-option>
              </a-select>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--number of bathroom-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Number of bathrooms</label>
            </div>
            <div style="float:left;text-align: left;width: 60%">
              <a-select class="text-right1" v-model="bathroom_number" :size="size">
                <a-select-option v-for="i in 10" :key="i">{{i}}</a-select-option>
              </a-select>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--property type-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Property type</label>
            </div>
            <div style="float:left;text-align: left;width: 60%">
              <a-select class="text-right1" v-model="property_type" :size="size">
                <a-select-option v-for="type in typedata" :key="type">{{type}}</a-select-option>
              </a-select>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--country-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Country</label>
            </div>
            <div style="float:left;text-align: left;width: 60%">
              <a-select class="text-right1" @change="handleCountryChange" v-model="country" :size="size"
                        style="width: 50%;height: 40px">
                <a-select-option v-for="countrya in countrydata" :key="countrya">{{countrya}}</a-select-option>
              </a-select>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--city-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">City</label>
            </div>
            <div style="float:left;text-align: left;width: 60%">
              <a-select class="text-right1" v-model="secondcities" @change="handleStateChange" :size="size"
                        style="width: 50%;height: 40px">
                <a-select-option v-for="city in cities" :key="city">{{city}}</a-select-option>
              </a-select>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--suburb-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Suburb</label>
            </div>
            <div style="float:left;text-align: left;width:60%">
              <a-select class="text-right1" v-model="secondsuburbs" :size="size" style="width: 50%;height: 40px">
                <a-select-option v-for="suburb in suburbs" :key="suburb">{{suburb}}</a-select-option>

              </a-select>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--price-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Price</label>
            </div>
            <div style="float:left;text-align: left;width:60%">
              <a-input class="text-right" placeholder="input price per night" v-model="property_price"></a-input>
              $/night
            </div>
            <div style="clear: left"></div>
          </div>

          <!--description-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Description</label>
            </div>
            <div style="float:left;text-align: left;width:60%">
              <textarea class="text-right" placeholder="please write a short description(at least 30 words)" :rows="3" style="height: 200px"
                        v-model="property_description"/>
            </div>
            <div style="clear: left"></div>
          </div>

          <!--amenities-->
          <div>
            <div style="width: 40%;float: left; margin-top: 30px;text-align: right;">
              <label class="text-left">Amenities (at least 6)</label>
            </div>
            <div style="float:left;text-align: left;width:60%">
              <a-checkbox-group :options="options" @change="onChange"  style="margin-top: 30px;width: 50%">
              </a-checkbox-group>
            </div>
            <div style="clear: left"></div>
          </div>

          <div class="clearfix" style="margin: 10px 5%">
            <a-upload
              action="/imageupload"
              listType="picture-card"
              :fileList="fileList"
              @preview="handlePreview"
              @change="handleChange"
            >
              <div v-if="fileList.length < 5">
                <a-icon type="plus"/>
                <div class="ant-upload-text">Upload 5 images</div>
              </div>
            </a-upload>
            <a-modal :visible="previewVisible" :footer="null" @cancel="handleCancel">
              <img alt="example" style="width: 100%" :src="previewImage"/>
            </a-modal>
          </div>

          <a-button type="primary" style="margin-top: 30px;margin-bottom: 30px" v-on:click="save">Save</a-button>

        </a-spin>

      </div>
    </div>

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
  import LoginHeader from '../components/LoginHeader'
  const options = ['kitchen', 'heating', 'tv', 'hangers', 'iron', 'washer', 'dryer', 'hot water', 'hair dryer', 'air conditioning', 'private bathroom', 'private living room', 'private entrance']
  const countrydata = ['Australia']
  const citydata = {
    Australia: ['Sydney']
  }
  const suburbdata = {
    Sydney:['Alexandria','Annandale/Leichhardt','Arncliffe','Artarmon','Ashfield','Auburn','Avalon','Balgowlah','Balmain/Birchgrove','Bardwell Valley','Beaconsfield','Bellevue Hill','Bexley','Bondi','Bondi Beach','Bondi Junction','Botany','Brighton-Le-Sands','Bronte','Burwood','Cammeray','Camperdown','Campsie','Canterbury','Carlton','Castle Cove/Middle Cove','Castlecrag','Central Business District','Chatswood','Chippendale','Clovelly','Coogee','Cremorne','Cronulla','Crows Nest','Croydon Park','Darling Point','Darlinghurst','Darlington','Denpasar','Double Bay','Drummoyne','Dulwich Hill','Earlwood','Eastlakes','Edgecliff','Elizabeth Bay/Rushcutters Bay','Enmore','Erskineville','Fairlight','Forest Lodge','Gladesville','Glebe','Greenwich','Haberfield','Haymarket','Hillsdale/Eastgardens','Homebush','Hunters Hill','Hurlstone Park','Kensington','Killarney Heights','Kingsford','Kirribilli/Milsons Point','Kogarah','Kogarah Bay/Carss Park','Lane Cove','Lewisham','Lilyfield/Rozelle','Little Bay','Longueville','Lugarno','Malabar','Manly','Maroubra','Marrickville','Mascot','Matraville','Millers Point','Mosman','Mosman','Naremburn','Neutral Bay','Newtown','Newtown/Enmore','North Bondi','North Melbourne','North Sydney','Oatley','Paddington','Pagewood','Palm Beach','Peakhurst','Petersham','Phillip Bay','Point Piper','Potts Point','Putney','Pyrmont','Queens Park','Randwick','Redfern','Rockdale','Rose Bay/Dover Heights','Rosebery','Sans Souci','Seaforth','Silverwater/Newington','South Coogee','St Leonards','St Peters','Stanmore','Strathfield','Summer Hill','Surry Hills','Tamarama','The Rocks','Ultimo','Vaucluse/Watsons Bay','Waterloo','Waverly','Whitechapel/Brick Lane','Willoughby','Wollstonecraft/Waverton','Woollahra','Woolloomooloo','Zetland']
  }
  const typedata = ['apartment', 'house', 'unit']
  export default {
    components: {LoginHeader},
    data() {
      return {
        countrydata,
        citydata,
        suburbdata,
        typedata,
        options,
        host_name: '',
        guest_number: '',
        bedroom_number: '',
        bed_number: '',
        bathroom_number: '',
        property_type: '',
        country: countrydata[0],
        cities: citydata[countrydata[0]],
        secondcities: citydata[countrydata[0]][0],
        suburbs: suburbdata[citydata[countrydata[0]][0]],
        secondsuburbs: suburbdata[citydata[countrydata[0]][0]][0],
        size: 'large',
        property_price: '',
        property_description: '',
        amenities: '',
        spinning: false,
        previewVisible: false,
        previewImage: '',
        fileList: [],
        finalfilelist: [],
        visible:false,
        wrong_msg:'',
        checknum:'',

      }
    },
    methods: {
      handleOk(){
        this.visible = false
      },
      onChange(checkedValues) {
        console.log('checked = ', checkedValues)
        this.checknum = checkedValues.length
        this.amenities =  checkedValues.toString()
      },
      /* if country change, the city also change*/
      handleCountryChange(value) {
        this.cities = citydata[value]
        this.secondcities = citydata[value][0]
      },
      /* if city change, the suburb also change*/
      handleStateChange(value) {
        this.suburbs = suburbdata[value]
        this.secondsuburbs = suburbdata[value][0]
      },
      /* create the new property*/
      save() {
        console.log(this.checknum)
        if(this.property_description.split(" ").length<30){
          alert("Description must at least 30 words")
        }
        else if (this.host_name === '' || this.guest_number === '' || this.bedroom_number === '' || this.bed_number === '' || this.bathroom_number === '' ||
          this.property_type === '' || this.country === '' || this.secondcities === '' || this.secondsuburbs === '' || this.property_price === '' ||
          this.property_description === '' || this.amenities === '' || this.finalfilelist === []) {
          this.visible = true
          this.wrong_msg = 'Nothing can be empty'

        }else if(this.checknum < 6){
          this.visible = true
          this.wrong_msg = 'You must select 6 amenities.'
        } else if(this.finalfilelist.length < 5){
          this.visible = true
          this.wrong_msg = 'You must upload 5 pictures.'
        } else {
          this.spinning = true
          console.log(this.finalfilelist)
          //const userinfo1 = JSON.parse(sessionStorage.getItem('userinfo'))
          this.axios.post('/api/accommodation', {
            token: Cookies.get('token'),
            name: this.host_name,
            num_guests: this.guest_number,
            num_bedrooms: this.bedroom_number,
            num_beds: this.bed_number,
            num_bathrooms: this.bathroom_number,
            property_type: this.property_type,
            country: this.country,
            city: this.secondcities,
            suburb: this.secondsuburbs,
            price: parseInt(this.property_price * 100) / 1,
            description: this.property_description,
            amenities: this.amenities,
            image_urls: this.finalfilelist.toString(),
          }).then((response) => {
            if (response.status === 201) {
              console.log(response.data.msg)
              this.$notification["success"]({
                message: 'Success',
                description: 'Congratulations, successfully uploaded your property!',
                duration: 3,
              });
              this.$router.push({
                name: 'DetailPage',
                params: {accomodation_id: response.data.msg.id}
              })
            } else {
              console.log(response.data.msg)
            }
            this.spinning = false
          }).catch( (e)=> {
            this.spinning = false
            if (e.response.data["msg"]) {
              console.log(e.response.data['msg'])
            } else if (e.response.data['errors']) {
              console.log(e.response.data['errors'])
            } else {
              console.log("Bad request")
            }
          })
        }
      },
      handleCancel() {
        this.previewVisible = false
      },
      handlePreview(file) {
        this.previewImage = file.url || file.thumbUrl
        this.previewVisible = true
      },
      handleChange({fileList}) {
        this.fileList = fileList
        var filelist = []
        fileList.forEach(function (c) {
          if (c.response) {
            filelist.push(c.response['url'])
          }
        })
        this.finalfilelist = filelist
      },
    }
  }
</script>

<style scoped>
  .text-left {
    padding: 0 20px;
    font-size: 16px
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

  .text-right1 {
    width: 50%;
    margin-top: 30px;
    height: 40px;
    font-size: 16px;
  }

  .ant-upload-select-picture-card i {
    font-size: 32px;
    color: #999;
  }

  .ant-upload-select-picture-card .ant-upload-text {
    margin-top: 8px;
    color: #666;
  }
</style>
