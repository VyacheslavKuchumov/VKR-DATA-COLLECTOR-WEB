<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Добро пожаловать в приложение!</h1>
        <p>Это главная страница вашего приложения.</p>

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
