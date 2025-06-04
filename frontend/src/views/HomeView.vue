<template>
  <v-container class="ml-auto mr-auto" max-width="800">
    <v-row>
      <v-col cols="12">
        <h1 class="display-6 font-weight-bold">Главная страница.</h1>

      </v-col>
    </v-row>
  </v-container>
</template>
  
<script>
  import { mapActions } from "vuex";

  export default {
    data() {
      return {

      };
    },
    methods: {
      ...mapActions({
        fetchOkveds: 'test/fetchData',
      }),
      okveds() {
        return this.$store.state.test.data || [];
      },
      fetchData() {
        this.fetchOkveds();
      },
    },
  };
</script>
