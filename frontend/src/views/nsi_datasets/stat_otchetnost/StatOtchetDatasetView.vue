<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Статистика количества работников по ОКВЭД
    </v-card-title>
  </v-container>

  <v-container class="elevation-0 mt-5 ml-auto mr-auto" max-width="1200">
    <v-toolbar flat color="white">
      <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/')" />
      <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
        На главную
      </v-toolbar-title>
      <v-spacer />
    </v-toolbar>

    <v-card-text>
      <v-row>
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
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  name: 'StatOtchetDatasetView',
  data() {
    return {};
  },
  computed: {
   
    groupedData() {
      // Группировка по okved_group
      const groups = {};
      this.workers()?.forEach(item => {
        const key = item.okved_group;
        if (!groups[key]) {
          groups[key] = [];
        }
        groups[key].push(item);
      });
      // Преобразовать в массив с сортировкой по году
      return Object.keys(groups).map(key => {
        const entries = groups[key].sort((a, b) => a.year - b.year);
        return {
          okved_group: key,
          years: entries.map(e => e.year.toString()),
          workerNums: entries.map(e => e.worker_num),
        };
      });
    },
  },

  methods: {
    workers() {
      return this.$store.state.minstat_workers.data || [];
    },
    loading() {
      return this.$store.state.minstat_workers.loading;
    },
    error() {
      return this.$store.state.minstat_workers.error;
    },
    ...mapActions({
      getMinstatWorkers: 'minstat_workers/getMinstatWorkers',
    }),
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
