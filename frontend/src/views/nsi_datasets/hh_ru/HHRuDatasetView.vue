<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Статистика вакансий по профессиональным ролям
    </v-card-title>
  </v-container>

  <v-container class="elevation-0 mt-5 ml-auto mr-auto" max-width="1200">
    <v-toolbar flat color="white">
      <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/datasets')" />
      <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-subtitle-1 font-weight-bold">
        Назад
      </v-toolbar-title>
      <v-spacer />
    </v-toolbar>

    <v-card-text>
      <v-row>
        <!-- Предупреждение при отсутствии данных -->
        <v-col cols="12" v-if="!loading && groupedData.length === 0">
          <v-card color="warning" class="pa-4 text-center">
            <v-card-title class="justify-center">
              Внимание: данных нет
            </v-card-title>
          </v-card>
        </v-col>

        <!-- Карточки с графиками вакансий -->
        <v-col
          v-for="(group, index) in groupedData"
          :key="index"
          cols="12"
          sm="6"
          md="4"
        >
          <v-card
            class="pa-4 text-center rounded-lg d-flex flex-column"
            elevation="3"
            height="100%"
            @click="openDialog(group.role)"
            style="cursor: pointer;"
          >
            <v-card-title class="text-subtitle-1 justify-center text-wrap">
              {{ group.role }}
            </v-card-title>

            <v-sparkline
              :model-value="group.vacanciesNums"
              :labels="group.datesFormatted"
              :smooth="16"
              :auto-draw="true"
              class="mt-4 flex-grow-1"
            >
              <template v-slot:label="item">
                {{ item.value }}
              </template>
            </v-sparkline>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </v-container>

  <!-- Диалог с таблицей -->
  <v-dialog v-model="dialog" max-width="800px">
    <v-card>
      <v-card-title>
        Данные по «<strong>{{ selectedRole }}</strong>»
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="tableHeaders"
          :items="filteredRows"
          :items-per-page="-1"
          item-key="id"
          class="elevation-1"
          hide-default-footer
          hide-default-header
        >
          <!-- Редактирование даты -->
          <template #item.entry_date="{ item }">
            <v-edit-dialog
              :return-value.sync="item.entry_date"
              large
              @save="saveRow(item)"
            >
              {{ formatDate(item.entry_date) }}
              <template #input>
                <v-text-field v-model="item.entry_date" type="date" />
              </template>
            </v-edit-dialog>
          </template>

          <!-- Редактирование числа вакансий -->
          <template #item.vacancies_num="{ item }">
            <v-edit-dialog
              :return-value.sync="item.vacancies_num"
              large
              @save="saveRow(item)"
            >
              {{ item.vacancies_num }}
              <template #input>
                <v-text-field v-model="item.vacancies_num" type="number" />
              </template>
            </v-edit-dialog>
          </template>
        </v-data-table>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="dialog = false">Закрыть</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'HhRuDatasetView',
  data() {
    return {
      dialog: false,
      selectedRole: null,
      tableHeaders: [
        { text: 'Дата записи', value: 'entry_date', align: 'start' },
        { text: 'Число вакансий', value: 'vacancies_num' }
      ],
    };
  },
  computed: {
    datasets() {
      return this.$store.state.hh_ru_dataset.data || [];
    },
    groupedData() {
      const groups = {};
      this.datasets.forEach(item => {
        const key = item.professional_role;
        if (!groups[key]) groups[key] = [];
        groups[key].push(item);
      });
      return Object.keys(groups).map(key => {
        const entries = groups[key].sort((a, b) =>
          new Date(a.entry_date) - new Date(b.entry_date)
        );
        return {
          role: key,
          dates: entries.map(e => e.entry_date),
          datesFormatted: entries.map(e => this.formatDate(e.entry_date)),
          vacanciesNums: entries.map(e => e.vacancies_num),
        };
      });
    },
    filteredRows() {
      if (!this.selectedRole) return [];
      return this.datasets
        .filter(item => item.professional_role === this.selectedRole)
        .map(item => ({ ...item }));
    },
  },
  methods: {
    ...mapActions({
      getHhRuDatasets: 'hh_ru_dataset/getHhRuDatasets',
      updateHhRuDataset: 'hh_ru_dataset/updateHhRuDataset',
      deleteHhRuDataset: 'hh_ru_dataset/deleteHhRuDataset',
    }),
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString('ru-RU');
    },
    openDialog(role) {
      this.selectedRole = role;
      this.dialog = true;
    },
    async saveRow(item) {
      const { id, entry_date, professional_role, vacancies_num } = item;
      await this.updateHhRuDataset({
        id,
        payload: { entry_date, professional_role, vacancies_num }
      });
    },
    async deleteRow(id) {
      await this.deleteHhRuDataset(id);
    },
  },
  async created() {
    await this.getHhRuDatasets();
  },
};
</script>

<style scoped>
.v-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.v-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.12) !important;
}
.v-sparkline {
  height: 150px;
}
</style>