<template>
  <div id="app">

    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'App',
    watch: {
      '$route': function (to, from) {
        //make sure every page start from top
        document.body.scrollTop = 0
        document.documentElement.scrollTop = 0
      }
    },
    created() {
      window.addEventListener("beforeunload", () => {
        localStorage.setItem("messageStore", JSON.stringify(this.$store.state))
      })
      localStorage.getItem("messageStore") && this.$store.replaceState(Object.assign(this.$store.state, JSON.parse(localStorage.getItem("messageStore"))));

    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 10px;
  }
</style>
