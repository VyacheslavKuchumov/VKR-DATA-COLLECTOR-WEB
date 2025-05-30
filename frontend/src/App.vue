<template>
  <v-app>
    
    <v-app-bar  color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title @click="this.$router.push(`/`);">Admin</v-toolbar-title>

      <v-spacer></v-spacer>

      
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
      location="left"
      app
      temporary
    >
      <v-list>
        
          <v-list-item to="/">
            <v-list-item-title>Главная</v-list-item-title>
          </v-list-item>

          
          <v-list-item 
            to="/"
            title="Реквизиты к hh.ru">
          </v-list-item>
          <v-list-item 
            to="/"
            title="Регионы для сбора данных">
          </v-list-item>
          <v-list-item 
            to="/"
            title="Backend сервера">
          </v-list-item>

      </v-list>
    </v-navigation-drawer>
    <v-main height="100vh">
      <v-container>
        <router-view />
      </v-container>
    </v-main>
    <!-- <v-footer padless color="grey lighten-4">
      <v-col class="text-center py-4" cols="12">
        © {{ new Date().getFullYear() }} Perm HR Forecast 
      </v-col>
    </v-footer> -->
  </v-app>
  
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  data() {
    return {
      drawer: false,
    };
  },
  
  methods: {

  },
};
</script>


