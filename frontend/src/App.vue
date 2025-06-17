<template>
  <v-app>
    
    <v-app-bar  color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title @click="this.$router.push(`/`);">{{ userRole }}</v-toolbar-title>

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
          <v-list-item to="/main-menu">
            <v-list-item-title>Меню</v-list-item-title>
          </v-list-item>
          
          

          <v-list-item 
            v-if="userRole === 'admin'"
            to="/users"
            title="Управление пользователями">
          </v-list-item>

          <v-list-item 
            v-if="userRole === 'admin'"
            to="/data-parsing"
            title="Сбор данных">
          </v-list-item>


          <v-list-item 
            to="/datasets"
            title="НСИ датасеты">
          </v-list-item>

          
          <v-list-item 
            to="/forecast"
            title="Прогнозы">
          </v-list-item>

          <v-list-item 
            v-if="!userRole"
            to="/login"
            title="Войти в аккаунт">
          </v-list-item>
          <v-list-item 
            v-if="userRole"
            @click="logout"
            title="Выйти из аккаунта">
          </v-list-item>
<!-- 
          <v-list-item 
            to="/hh-ru-jobs"
            title="Сбор данных с hh.ru">
          </v-list-item>
          
          <v-list-item 
            to="/hh-ru-credentials"
            title="Реквизиты к hh.ru">
          </v-list-item>
          <v-list-item 
            to="/regions"
            title="Регионы для сбора данных">
          </v-list-item> -->
      </v-list>
    </v-navigation-drawer>
    <v-main min-height="100vh" class="background-image">
      <v-container >
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
    logout() {
      this.$store.dispatch("auth/logout");
      window.location.href = "/";
    },
  },
  async created() {
    const role = localStorage.getItem("role");
    if (role) {
      this.$store.commit("auth/setUserRole", role);
      this.$store.commit("auth/setAuth", true);
    }
  },
  computed: {
    ...mapState({
      userRole: (state) => state.auth.user_role,
      isAuth: (state) => state.auth.isAuth,
    }),
  },
};
</script>

<style scoped>
.gradient-background {

  background: linear-gradient(135deg, #ffe0b2 0%, #1e18c050 100%);
  min-height: 100vh; /* чтобы перекрыть всю высоту экрана */
}

.background-image {
  background-image: url('@/assets/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: repeat-y;
  min-height: 100vh;
}

</style>
