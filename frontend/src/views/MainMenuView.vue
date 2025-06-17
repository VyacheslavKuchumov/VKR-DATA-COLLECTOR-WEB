<template>
      <v-container  max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
        <v-card-title class="text-wrap text-center justify-center">
            <h1 class="text-h4">Главное меню</h1>
        </v-card-title>
    </v-container>
  <v-container class="elevation-0 mt-2 ml-auto mr-auto" max-width="1200">
    <v-card-text>
      <v-row>
        <!-- Пользователи -->
        <v-col cols="12" sm="6" md="6">
          <v-card
            v-if="userRole === 'admin'"
            class="pa-4 rounded-lg d-flex flex-column"
            elevation="3"
            height="100%"
            color="blue-lighten-4"
            @click="$router.push('/users')"
          >
            <v-container v-if="!$vuetify.display.mobile" class="d-flex align-center">
              <v-icon size="64" color="blue-darken-2" class="mr-4">mdi-account-cog</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-wrap">
                Пользователи
              </v-card-title>
            </v-container>
            <v-container v-else class="d-flex align-center justify-center mb-2">
              <v-icon size="42" color="blue-darken-2" class="mb-2">mdi-account-cog</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-center">
                Пользователи
              </v-card-title>
            </v-container>
            <v-card-text class="mt-2 flex-grow-1">
              Управление учетными записями, ролями и правами доступа пользователей системы
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn
                color="white"
                variant="outlined"
                @click.stop="$router.push('/users')"
                append-icon="mdi-arrow-right"
                size="large"
              >
                Перейти
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- Сбор данных -->
        <v-col cols="12" sm="6" md="6">
          <v-card
            v-if="userRole === 'admin'"
            class="pa-4 rounded-lg d-flex flex-column"
            elevation="3"
            height="100%"
            color="orange-lighten-4"
            @click="$router.push('/data-parsing')"
          >
            <v-container class="d-flex align-center">
              <v-icon size="64" color="orange-darken-2" class="mr-4">mdi-cloud-download</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-wrap">
                Сбор данных
              </v-card-title>
            </v-container>

            <v-card-text class="mt-2 flex-grow-1">
              Интеграция данных из внешних источников и систем
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn
                color="white"
                variant="outlined"
                @click.stop="$router.push('/data-parsing')"
                append-icon="mdi-arrow-right"
                size="large"
              >
                Перейти
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- НСИ датасеты -->
        <v-col cols="12" sm="6" md="6">
          <v-card
            class="pa-4 rounded-lg d-flex flex-column"
            elevation="3"
            height="100%"
            color="green-lighten-4"
            @click="$router.push('/datasets')"
          >
            <v-container v-if="!$vuetify.display.mobile" class="d-flex align-center">
              <v-icon size="64" color="green-darken-2" class="mr-4">mdi-database</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-wrap">
                НСИ датасеты
              </v-card-title>
            </v-container>
            <v-container v-else class="d-flex align-center justify-center mb-2">
              <v-icon size="42" color="green-darken-2" class="mb-2">mdi-database</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-center">
                НСИ датасеты
              </v-card-title>
            </v-container>
            <v-card-text class="mt-2 flex-grow-1">
              Просмотр и управление нормативно-справочной информацией
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn
                color="white"
                variant="outlined"
                @click.stop="$router.push('/datasets')"
                append-icon="mdi-arrow-right"
                size="large"
              >
                Перейти
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- Прогнозы -->
        <v-col cols="12" sm="6" md="6">
          <v-card
            class="pa-4 rounded-lg d-flex flex-column"
            elevation="3"
            height="100%"
            color="purple-lighten-4"
            @click="$router.push('/forecast')"
          >
            <v-container v-if="!$vuetify.display.mobile" class="d-flex align-center">
              <v-icon size="64" color="purple-darken-2" class="mr-4">mdi-chart-line</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-wrap">
                Прогнозы
              </v-card-title>
            </v-container>
            <v-container v-else class="d-flex align-center justify-center mb-2">
              <v-icon size="42" color="purple-darken-2" class="mb-2">mdi-chart-line</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-center">
                Прогнозы
              </v-card-title>
            </v-container>
            <v-card-text class="mt-2 flex-grow-1">
              Аналитические отчеты и прогнозные модели
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn
                color="white"
                variant="outlined"
                @click.stop="$router.push('/forecast')"
                append-icon="mdi-arrow-right"
                size="large"
              >
                Перейти
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- Личный кабинет -->
        <v-col cols="12" sm="6" md="6">
          <v-card
            v-if="userRole"
            class="pa-4 rounded-lg d-flex flex-column"
            elevation="3"
            height="100%"
            color="teal-lighten-4"
            @click="$router.push('/profile')"
          >
            <v-container v-if="!$vuetify.display.mobile" class="d-flex align-center">
              <v-icon size="64" color="teal-darken-2" class="mr-4">mdi-account-circle</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-wrap">
                Личный кабинет
              </v-card-title>
            </v-container>
            <v-container v-else class="d-flex align-center justify-center mb-2">
              <v-icon size="42" color="teal-darken-2" class="mb-2">mdi-account-circle</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-center">
                Личный кабинет
              </v-card-title>
            </v-container>
            <v-card-text class="mt-2 flex-grow-1">
              Доступ к персональным настройкам и информации профиля
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn
                color="white"
                variant="outlined"
                @click.stop="$router.push('/profile')"
                append-icon="mdi-arrow-right"
                size="large"
              >
                Перейти
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- Расчет КЦП -->
        <v-col cols="12" sm="6" md="6">
          <v-card
            v-if="userRole"
            class="pa-4 rounded-lg d-flex flex-column"
            elevation="3"
            height="100%"
            color="amber-lighten-4"
            @click="$router.push('/kcp-calculation')"
          >
            <v-container v-if="!$vuetify.display.mobile" class="d-flex align-center">
              <v-icon size="64" color="amber-darken-2" class="mr-4">mdi-calculator</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-wrap">
                Расчет КЦП
              </v-card-title>
            </v-container>
            <v-container v-else class="d-flex align-center justify-center mb-2">
              <v-icon size="42" color="amber-darken-2" class="mb-2">mdi-calculator</v-icon>
              <v-card-title class="text-h6 font-weight-bold text-center">
                Расчет КЦП
              </v-card-title>
            </v-container>
            <v-card-text class="mt-2 flex-grow-1">
              Выполнение расчёта ключевых показателей эффективности
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn
                color="white"
                variant="outlined"
                @click.stop="$router.push('/kcp-calculation')"
                append-icon="mdi-arrow-right"
                size="large"
              >
                Перейти
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

      </v-row>
    </v-card-text>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "HomeView",
  async created() {
    const role = localStorage.getItem("role");
    if (role) {
      this.$store.commit("auth/setUserRole", role);
    }
  },
  computed: {
    ...mapState({
      userRole: (state) => state.auth.user_role,
    }),
  },
};
</script>

<style scoped>
.text-h6 {
  font-size: 1.25rem;
  line-height: 1.6;
}
</style>
