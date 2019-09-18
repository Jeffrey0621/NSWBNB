<template>
  <div>
    <div style="margin-left: 5%;margin-right: 5%">
      <!-- <a-input placeholder="Search" style="float: left;width: 50%">
         <a-icon slot="prefix" type="search"/>
       </a-input>-->
      <login-header style="float: right;width: 50%;"></login-header>
      <!--to clear the float-->
      <div style="clear: both"></div>
    </div>

    <div style="margin-top: 20px">
      <a-layout>
        <a-layout-content style="padding: 50px 200px">
          <a-layout style="padding: 24px 0; background: #fff">
            <a-layout-sider width="200" style="background: #fff">
              <a-menu
                mode="inline"
                :defaultSelectedKeys="['1']"
                style="height: 100%"
                onclick={this.onclick.bind(this)}
              >
                <a-menu-item key="1" @click="changepage('EditProfile')">Edit profile</a-menu-item>
                <a-menu-item key="3" @click="changepage('ChangePassword')">Change Password</a-menu-item>
                <a-menu-item key="2" @click="changepage('Host_order')">Manage Reservations</a-menu-item>
                <a-menu-item key="4" @click="changepage('MyTrip')">My Trips</a-menu-item>
                <a-menu-item key="5" @click="changepage('MyProperty')">My Properties</a-menu-item>
              </a-menu>
            </a-layout-sider>
            <a-layout-content :style="{minHeight: '500px' }" :is="currentPage"></a-layout-content>
          </a-layout>
        </a-layout-content>

      </a-layout>
    </div>

  </div>
</template>

<script>
  import LoginHeader from "./../components/LoginHeader"
  import EditProfile from "../components/EditProfile"
  import Host_order from "../components/Host_order"
  import ChangePassword from "../components/ChangePassword"
  import MyTrip from "../components/MyTrip"
  import MyProperty from "../components/MyProperty"

  export default {
    components: {LoginHeader, EditProfile, Host_order, ChangePassword, MyTrip, MyProperty},
    methods: {
      onCollapse(collapsed, type) {
        console.log(collapsed, type);
      },
      onBreakpoint(broken) {
        console.log(broken);
      },
      changepage(page) {
        this.currentPage = page
      }
    },
    data() {
      return {
        currentPage: EditProfile,
        EditProfile: EditProfile,
        Host_order: Host_order,
        ChangePassword: ChangePassword,
        MyTrip: MyTrip,
        MyProperty: MyProperty
      }
    }
  }
</script>

<style scoped>

</style>
