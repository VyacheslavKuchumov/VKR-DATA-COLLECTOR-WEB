<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
        <v-card-title class="text-wrap" align="center">
            Личный кабинет
        </v-card-title>
    </v-container>
  <v-container class="elevation-2 mt-5 ml-auto mr-auto bg-white rounded-lg pa-0" max-width="800">
    <v-toolbar flat>
        <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/main-menu')" />
        <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
          Назад
        </v-toolbar-title>
        
        <v-spacer />
        <v-btn color="error" @click="logout" prepend-icon="mdi-logout">
          Выйти
        </v-btn>
      </v-toolbar>
    <!-- Профиль пользователя -->
    <v-card class="mt-5 pa-4 elevation-0">
      

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

            
          </v-list>
        </v-col>
        <v-col cols="12" md="6">
          <v-list dense>
            <v-list-item>
              <v-list-item-avatar>
                <v-icon large>mdi-account-key</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Роль: {{ role }}</v-list-item-title>
                <v-list-item-subtitle>ID: {{ id }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>

      <v-row justify="center" class="mt-8">
        <v-btn color="primary" prepend-icon="mdi-account-edit">
          Редактировать профиль
        </v-btn>
      </v-row>
    </v-card>

    <!-- История расчетов -->
    <v-card class="mt-6 pa-4 elevation-0">
      <v-card-title class="text-h6">История расчетов</v-card-title>

      <v-data-table
        :headers="historyHeaders"
        :items="history"
        class="elevation-0 ma-0"
        dense
        disable-sort
        :items-per-page="-1"
        hide-default-footer
      >
        <template #item.date="{ item }">
          {{ formatDate(item.date) }}
        </template>
        <template #item.actions="{ item }">
          
            <v-icon>mdi-eye</v-icon>
          
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "UserProfileView",
  data() {
    return {
      id: null,
      email: "",
      name: "",
      role: "",

      historyHeaders: [
        { title: "Дата", value: "date" },
        { title: "Тип", value: "type" },
        { title: "Объект", value: "target" },
        { title: "Период", value: "period", align: "end" },
        { title: "Прогноз", value: "forecast", align: "end" },
        { title: "Δ%", value: "change", align: "end" },
        { title: "Действия", value: "actions", sortable: false }
      ],

      history: [
        {
          id: 1,
          date: "2025-06-21T11:30:00",
          type: "Расчет КЦП",
          target: "09.02.07 Информационные системы и программирование",
          period: 2,
          forecast: 108,
          change: 8.0
        },
        {
          id: 2,
          date: "2025-06-20T09:00:00",
          type: "Прогноз (профессия)",
          target: "Аналитик данных",
          period: 3,
          forecast: 470,
          change: 14.6
        },
        {
          id: 3,
          date: "2025-06-18T15:10:00",
          type: "Прогноз (сфера)",
          target: "Здравоохранение",
          period: 1,
          forecast: 890,
          change: -1.1
        }
      ]
    };
  },
  mounted() {
    this.id = localStorage.getItem("id");
    this.email = localStorage.getItem("email");
    this.name = localStorage.getItem("name");
    this.role = localStorage.getItem("role");
  },
  methods: {
    logout() {
      this.$store.dispatch("auth/logout");
      window.location.href = "/";
    },
    formatDate(iso) {
      return new Date(iso).toLocaleString("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      });
    },
    viewHistory(item) {
      this.$toast.info(`Просмотр расчета: ${item.type} — ${item.target}`);
    }
  }
};
</script>

<style scoped>
.v-card-title h1 {
  width: 100%;
}
</style>
