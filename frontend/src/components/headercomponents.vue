<template>
    <div class="headercom">
      <img class="headimage" src="./../assets/pic/headbg.png"/>
      <a-icon style="z-index: 1;float: right;margin-right: 20px;font-size: 36px" type="home" v-on:click="backhome"></a-icon>
    </div>
</template>

<script>
    export default {
      methods:{
        backhome(){
          this.$router.push('/')
        }
      }
    }
</script>

<style scoped>
  .headercom{
    height: 60px;
    width: 100%;
    background: white;
    float: top;
  }
</style>
