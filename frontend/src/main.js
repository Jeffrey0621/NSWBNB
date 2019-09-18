// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
//import BootstrapVue from 'bootstrap-vue'
import Antd from 'ant-design-vue'
import axios from 'axios'
import Cookies from 'js-cookie'
import Vuex from 'vuex'

import './assets/css/login-signup.css'
//import 'bootstrap/dist/css/bootstrap.css'
//import 'bootstrap-vue/dist/bootstrap-vue.css'

import 'ant-design-vue/dist/antd.css'
import VeeValidate from 'vee-validate'

Vue.use(VeeValidate)

//Vue.use(BootstrapVue)
Vue.use(Antd)
Vue.use(Vuex)
Vue.use(Cookies)

Vue.config.productionTip = false
//axios.defaults.baseURL = "http://nswbnb.herokuapp.com/"
axios.defaults.baseURL = "http://127.0.0.1:5000"
Vue.prototype.axios = axios

router.beforeEach((to, from, next) => {
  if (to.meta.isLogin) {
    if (Cookies.get('token')) {
      next();
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      })
    }
  } else {
    next()//do not need login
  }

});

const store = new Vuex.Store({
  state: {
    location: "",
    check_in_date: '2019-06-26',
    check_out_date: '2019-06-26',
    guest_number: 'number of guest',
    amenities: '',
  },
  mutations: {
    updateCheckIn(state, check_in_date) {
      state.check_in_date = check_in_date
    },
    updateCheckOut(state, check_out_date) {
      state.check_out_date = check_out_date
    },
    updateGuestNumber(state, guest_number) {
      state.guest_number = guest_number
    },
    updateLocation(state, location) {
      state.location = location
    },
    updateAmenities(state, amenities) {
      state.amenities = amenities
    }
  }
})


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
})
