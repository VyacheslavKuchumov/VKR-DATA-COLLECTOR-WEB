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

    <!-- История прогнозов -->
    <v-card class="mt-6 pa-4 elevation-0">
      <v-card-title class="text-h6">История прогнозов</v-card-title>

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

        <template #item.period="{ item }">
          {{ item.period }} лет
        </template>

        <template #item.forecast="{ item }">
          {{ formatNumber(item.forecast) }}
          <span v-if="isOkved(item.type)">тыс. ч.</span>
          <span v-else>ч.</span>
        </template>

        <template #item.change="{ item }">
          <span :class="item.change >= 0 ? 'green--text' : 'red--text'">
            {{ item.change >= 0 ? '+' : '' }}{{ item.change.toFixed(1) }}%
          </span>
        </template>

        <template #item.actions="{ item }">
          <v-tooltip text="Просмотр отчета" location="top">
            <template #activator="{ props }">
              <v-icon
                v-bind="props"
                color="primary"
                class="cursor-pointer"
                @click="viewHistory(item)"
              >
                mdi-eye
              </v-icon>
            </template>
          </v-tooltip>
        </template>
      </v-data-table>
    </v-card>
  </v-container>

  <!-- Диалог просмотра отчета -->
  <v-dialog v-model="dialog" max-width="800">
    <v-card>
      <v-card-title class="text-h6">
        {{ dialogData.type }} — {{ dialogData.target }}
      </v-card-title>
      <v-card-text>
        <div class="d-flex align-center justify-space-between">
          <!-- Текущий спрос -->
          <div>
            <div class="text-h4 primary--text">
              {{ formatNumber(dialogData.current) }}
              <span v-if="dialogData.isOkved">тыс. ч.</span>
              <span v-else>ч.</span>
            </div>
            <div class="text-caption">Текущий спрос</div>
          </div>

          <!-- Изменение -->
          <div class="text-center">
            <div
              class="text-h4"
              :class="dialogData.change >= 0 ? 'green--text' : 'red--text'"
            >
              {{ dialogData.change >= 0 ? '+' : '' }}{{ dialogData.change.toFixed(1) }}%
            </div>
            <div class="text-caption">Изменение</div>
          </div>

          <!-- Прогноз -->
          <div>
            <div class="text-h4 blue--text">
              {{ formatNumber(dialogData.forecast) }}
              <span v-if="dialogData.isOkved">тыс. ч.</span>
              <span v-else>ч.</span>
            </div>
            <div class="text-caption">Прогноз через {{ dialogData.period }} лет</div>
            <div class="text-caption">Точность: {{ dialogData.accuracy }}%</div>
          </div>
        </div>

        <v-sparkline
          :model-value="dialogData.sparklineData"
          :labels="dialogData.sparklineLabels"
          :smooth="16"
          padding="24"
          auto-draw
          class="mt-6"
        />
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn text @click="dialog = false">Закрыть</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
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
          type: "Прогноз (ОКВЭД)",
          target: "Обрабатывающие производства",
          period: 2,
          forecast: 108.2,
          change: 4.3
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
          type: "Прогноз (ОКВЭД)",
          target: "Здравоохранение",
          period: 1,
          forecast: 890.3,
          change: -1.1
        }
      ],

      // для диалога просмотра
      dialog: false,
      dialogData: {
        type: "",
        target: "",
        period: 0,
        current: 0,
        forecast: 0,
        change: 0,
        accuracy: 0,
        sparklineData: [],
        sparklineLabels: [],
        isOkved: false
      }
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
    formatNumber(val) {
      return val.toLocaleString("ru-RU");
    },
    isOkved(type) {
      return type.toLowerCase().includes("оквэд");
    },
    viewHistory(item) {
      // наполняем dialogData
      const base = item.forecast / (1 + item.change / 100);
      const accuracy = (80 + Math.random() * 10).toFixed(1);
      const labels = [];
      const data = [];
      const year0 = new Date(new Date(item.date).getFullYear(),0).getFullYear();
      // 5 прошлых точек
      for (let i = 5; i > 0; i--) {
        data.push(Math.round(base * (0.85 + Math.random() * 0.15)));
        labels.push((year0 - i).toString());
      }
      // текущая точка
      data.push(Math.round(base));
      labels.push(year0.toString());
      // прогнозные точки до периода
      for (let i = 1; i <= item.period; i++) {
        data.push(Math.round(base + (item.forecast - base)*(i/item.period)));
        labels.push((year0 + i).toString());
      }

      this.dialogData = {
        type: item.type,
        target: item.target,
        period: item.period,
        current: Math.round(base),
        forecast: item.forecast,
        change: item.change,
        accuracy: parseFloat(accuracy),
        sparklineData: data,
        sparklineLabels: labels,
        isOkved: this.isOkved(item.type)
      };
      this.dialog = true;
    }
  }
};
</script>

<style scoped>
.v-card-title h1 {
  width: 100%;
}
</style>
