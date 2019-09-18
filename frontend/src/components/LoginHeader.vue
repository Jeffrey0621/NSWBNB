<template>
  <div>
    <a-row class="btn-header" type="flex" justify="end">
      <a-button v-show="!user_show" class="btn-login" v-on:click="login" :size="size">Log in</a-button>
      <a-button v-show="!user_show" v-on:click="signup" :size="size">Sign up</a-button>

      <a-dropdown v-show="user_show">
        <a class="ant-dropdown-link" href="#">
          <span v-text="username"/>
          <a-icon type="down"/>
        </a>
        <a-menu slot="overlay">
          <a-menu-item>
            <a href="javascript:; " v-on:click="myprofile">My profile</a>
          </a-menu-item>
          <a-menu-item>
            <a href="javascript:;" v-on:click="homepage">Homepage</a>
          </a-menu-item>
          <a-menu-item>
            <a href="javascript:;" v-on:click="logout">Log out</a>
          </a-menu-item>
        </a-menu>
      </a-dropdown>
    </a-row>
  </div>
</template>

<script>

  import Cookies from 'js-cookie'

  export default {

    data() {
      return {
        size: 'large',
        username: '',
        user_show: false
      }
    },
    methods: {
      /*go to login page*/
      login() {
        this.$router.push('/login')
      },
      /*go to sign up page*/
      signup() {
        this.$router.push('/signup')
      },
      /*go to home page*/
      homepage() {
        this.$router.push('/')
      },
      /*logout and clear cookies*/
      logout() {
        //const userinfo1 = JSON.parse(sessionStorage.getItem('userinfo'))
        this.axios.post('/api/logout', {
          token: Cookies.get('token')
        }).then((response) => {
        }).catch(function (e) {
          console.log(e)
        })
        Cookies.remove('username')//remove cookies
        Cookies.remove('user_id')
        Cookies.remove('email')
        Cookies.remove('token')
        this.username = ''
        this.user_show = false
        sessionStorage.removeItem('userinfo')//remove user information
        this.$router.push('/')
      },
      /*Determine if it's logged in*/
      isLogin() {
        if (Cookies.get('token') && Cookies.get('username')) {
          this.user_show = true
          this.username = Cookies.get('username')
        } else {
          this.user_show = false
        }
      },
      /*go to profile page*/
      myprofile() {
        this.$router.push('/profile')
      }

    },
    mounted: function () {
      this.isLogin();
    }
  }
</script>

<style scoped>
  .btn-login {
    margin-right: 10px;
  }
</style>
