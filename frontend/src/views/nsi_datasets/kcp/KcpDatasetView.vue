<template>
  <v-container max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Статистика КЦП по направлениям подготовки
    </v-card-title>
  </v-container>

  <v-container class="elevation-0 mt-5 ml-auto mr-auto" max-width="1200">
    <v-toolbar flat color="white">
      <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/')" />
      <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-subtitle-1 font-weight-bold">
        На главную
      </v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <v-card-text>
      <v-row>
        <v-col cols="12" v-if="!loading && groupedData.length === 0">
          <v-card color="warning" class="pa-4 text-center">
            <v-card-title class="justify-center">
              Внимание: данных нет
            </v-card-title>
          </v-card>
        </v-col>

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
            @click="openDialog(group.study_field_code)"
            style="cursor: pointer;"
          >
            <v-card-title class="text-subtitle-1 justify-center text-wrap">
              <strong>{{ group.study_field_code }}</strong> - {{ group.study_field_name }}
            </v-card-title>

            <v-sparkline
              :model-value="group.kcpNums"
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

  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title class="text-wrap">
        КЦП по «<strong>{{ selectedFieldName }}</strong>»
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
          <template #item.year="{ item }">
            <v-edit-dialog :return-value.sync="item.year" large @save="saveRow(item)">
              {{ item.year }}
              <template #input>
                <v-text-field v-model="item.year" type="number" />
              </template>
            </v-edit-dialog>
          </template>

          <template #item.kcp_num="{ item }">
            <v-edit-dialog :return-value.sync="item.kcp_num" large @save="saveRow(item)">
              {{ item.kcp_num }}
              <template #input>
                <v-text-field v-model="item.kcp_num" type="number" />
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
  name: 'KcpDatasetView',
  data() {
    return {
      dialog: false,
      selectedFieldCode: null,
      selectedFieldName: '',
      tableHeaders: [
        { text: 'Год', value: 'year', align: 'start' },
        { text: 'КЦП', value: 'kcp_num' },
      ],
    };
  },
  computed: {
    kcpRecords() {
      return this.$store.state.kcp_dataset.data || [];
    },
    loading() {
      return this.$store.state.kcp_dataset.loading;
    },
    groupedData() {
      const groups = {};
      this.kcpRecords.forEach(item => {
        const key = item.study_field_code;
        if (!groups[key]) groups[key] = [];
        groups[key].push(item);
      });
      return Object.entries(groups).map(([code, records]) => {
        const sorted = records.sort((a, b) => a.year - b.year);
        return {
          study_field_code: code,
          study_field_name: sorted[0].study_field_name,
          years: sorted.map(e => e.year.toString()),
          kcpNums: sorted.map(e => e.kcp_num),
        };
      });
    },
    filteredRows() {
      return this.kcpRecords.filter(item => item.study_field_code === this.selectedFieldCode).map(i => ({ ...i }));
    },
  },
  methods: {
    
    ...mapActions({
      getKcpDatasets: 'kcp_dataset/getKcpDatasets',
      updateKcpDataset: 'kcp_dataset/updateKcpDataset',
    }),

    openDialog(code) {
      this.selectedFieldCode = code;
      const entry = this.kcpRecords.find(i => i.study_field_code === code);
      this.selectedFieldName = entry ? entry.study_field_name : '';
      this.dialog = true;
    },

    async saveRow(item) {
      const { id, year, kcp_num, study_field_code, study_field_name } = item;
      await this.updateKcpDataset({
        id,
        payload: { year, kcp_num, study_field_code, study_field_name }
      });
    },
  },
  async created() {
    await this.getKcpDatasets();
  },
};
</script>

<style scoped>
.v-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.v-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.12) !important;
}
.v-sparkline {
  height: 150px;
}
</style>