<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Статистика количества работников по ОКВЭД
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

        <!-- Карточки с графиками -->
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
            @click="openDialog(group.okved_group)"
            style="cursor: pointer;"
          >
            <v-card-title class="text-subtitle-1 justify-center text-wrap">
              {{ group.okved_group }}
            </v-card-title>

            <v-sparkline
              :model-value="group.workerNums"
              :labels="group.years"
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
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title class="text-wrap">
        Данные по «<strong>{{ selectedGroup }}</strong>»
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
          <!-- Редактирование года -->
          <template #item.year="{ item }">
            <v-edit-dialog
              :return-value.sync="item.year"
              large
              @save="saveRow(item)"
            >
              {{ item.year }}
              <template #input>
                <v-text-field v-model="item.year" type="number" />
              </template>
            </v-edit-dialog>
          </template>

          <!-- Редактирование числа работников -->
          <template #item.worker_num="{ item }">
            <v-edit-dialog
              :return-value.sync="item.worker_num"
              large
              @save="saveRow(item)"
            >
              {{ item.worker_num }}
              <template #input>
                <v-text-field v-model="item.worker_num" type="number" />
              </template>
            </v-edit-dialog>
          </template>

          <!-- 
          <template #item.actions="{ item }">
            <v-icon small class="mr-2" @click="deleteRow(item.id)">
              mdi-delete
            </v-icon>
            
          </template> -->
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
  name: 'StatOtchetDatasetView',
  data() {
    return {
      dialog: false,
      selectedGroup: null,
      tableHeaders: [
        { text: 'Год', value: 'year', align: 'start' },
        { text: 'Число работников', value: 'worker_num' },
        { text: 'Действия', value: 'actions', sortable: false },
      ],
    };
  },
  computed: {
    // Группировка данных для карточек
    groupedData() {
      const groups = {};
      this.workers.forEach(item => {
        const key = item.okved_group;
        if (!groups[key]) groups[key] = [];
        groups[key].push(item);
      });
      return Object.keys(groups).map(key => {
        const entries = groups[key].sort((a, b) => a.year - b.year);
        return {
          okved_group: key,
          years: entries.map(e => e.year.toString()),
          workerNums: entries.map(e => e.worker_num),
        };
      });
    },
    // Все данные из стора
    workers() {
      return this.$store.state.minstat_workers.data || [];
    },
    loading() {
      return this.$store.state.minstat_workers.loading;
    },
    // Только строки выбранной группы
    filteredRows() {
      if (!this.selectedGroup) return [];
      return this.workers
        .filter(item => item.okved_group === this.selectedGroup)
        // Убедимся, что у каждого есть уникальный id
        .map(item => ({ ...item }));
    },
  },
  methods: {
    ...mapActions({
      getMinstatWorkers: 'minstat_workers/getMinstatWorkers',
      updateMinstatWorker: 'minstat_workers/updateMinstatWorker',
      deleteMinstatWorker: 'minstat_workers/deleteMinstatWorker',
    }),

    openDialog(group) {
      this.selectedGroup = group;
      this.dialog = true;
    },

    // Сохраняем изменения: диспатчим экшен updateMinstatWorker
    async saveRow(item) {
      const { id, year, worker_num, okved_group } = item;
      await this.updateMinstatWorker({
        id,
        payload: { year, worker_num, okved_group }
      });
    },

    // Удаляем строку
    async deleteRow(id) {
      await this.deleteMinstatWorker(id);
    },
  },
  async created() {
    await this.getMinstatWorkers();
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
