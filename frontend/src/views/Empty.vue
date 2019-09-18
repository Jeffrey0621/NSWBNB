<template>
  <div>

  </div>
</template>

<script>
export default {
  mounted() {
    console.log(this.$route.params.temp_id)
    this.$router.replace({
      name: 'DetailPage',
      params: {accomodation_id: this.$route.params.temp_id}
    })
  }
}
</script>
