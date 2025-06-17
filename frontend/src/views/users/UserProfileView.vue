<template>
  <v-container class="elevation-0 mt-5 ml-auto mr-auto" max-width="800">
    <!-- Заголовок страницы -->
    <v-card-title class="text-wrap text-center justify-center">
      <h1 class="text-h4">Личный кабинет</h1>
    </v-card-title>

    <!-- Профиль пользователя -->
    <v-card class="mt-5 pb-6">
        <v-toolbar flat>
            <v-btn icon="mdi-arrow-left" color="primary" @click="$router.go(-1)" />
            <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
                Назад
            </v-toolbar-title>
            <v-spacer />

        </v-toolbar>

      <v-row>
        <v-col cols="12" md="6">
          <v-list dense>
            <v-list-item>
              <v-list-item-avatar>
                <v-icon large>mdi-account-circle</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>{{ name }}</v-list-item-title>
                <v-list-item-subtitle>{{ email }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>


            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-shield-account</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Роль: {{ role }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>

        
      </v-row>

      <!-- Кнопка выхода -->
      <v-row justify="center" class="mt-6">
        <v-btn color="error" @click="logout" prepend-icon="mdi-logout">
          Выйти
        </v-btn>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "UserProfileView",
  data() {
    return {
      id: null,
      email: '',
      name: '',
      role: ''
    };
  },
  mounted() {
    // Чтение из localStorage при загрузке
    this.id = localStorage.getItem('id');
    this.email = localStorage.getItem('email');
    this.name = localStorage.getItem('name');
    this.role = localStorage.getItem('role');
  },
  methods: {
    logout() {
      
      this.$store.dispatch("auth/logout");
      window.location.href = "/";

    }
  }
};
</script>

<style scoped>
.v-card-title h1 {
  width: 100%;
}
</style>
