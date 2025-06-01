<template>
  <v-card max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Управление заданиями
    </v-card-title>
  </v-card>

  <v-card class="elevation-5 mt-5 ml-auto mr-auto" max-width="800">
    <v-toolbar flat>
      <v-spacer />
      <v-btn icon="mdi-plus" color="primary" @click="openCreateDialog" />
    </v-toolbar>

    <!-- Диалог создания нового задания -->
    <v-dialog v-model="newJobDialog" max-width="600">
      <v-card>
        <v-card-title>Новый Задание</v-card-title>
        <v-card-text>
          <!-- Кнопки открытия таблиц выбора -->
          <v-row>
            <v-col cols="12" sm="6">
              {{ selectedRegion }}
            </v-col>
            <v-col cols="12" sm="6">
              {{ selectedCredential }}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6">
              <v-btn color="primary" @click="openRegionDialog">
                Выбрать Регион
              </v-btn>
            </v-col>
            <v-col cols="12" sm="6">
              <v-btn color="primary" @click="openCredentialDialog">
                Выбрать Credentials
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="cancelCreate">Отмена</v-btn>
          <v-btn color="primary" @click="confirmCreate" :disabled="!selectedRegion || !selectedCredential">
            Создать
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог выбора регионов -->
    <v-dialog v-model="regionDialog" max-width="700">
      <v-card>
        <v-card-title>Выберите Регион</v-card-title>
        <v-card-text>
          <v-data-table-server
            :headers="regionHeaders"
            :items="regions"
            :loading="isLoadingRegions"
            :items-per-page="10"
          >
            <template #item.name="{ item }">
              {{ item.name }}
            </template>
            <template #item.action="{ item }">
              <v-btn icon size="small" @click="selectRegion(item)">
                <v-icon color="primary">mdi-plus</v-icon>
              </v-btn>
            </template>
          </v-data-table-server>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Диалог выбора Credentials -->
    <v-dialog v-model="credentialDialog" max-width="700">
      <v-card>
        <v-card-title>Выберите Credentials</v-card-title>
        <v-card-text>
          <v-data-table-server
            :headers="credentialHeaders"
            :items="credentials"
            :loading="isLoadingCredentials"
            :items-per-page="10"
          >
            <template #item.label="{ item }">
              {{ item.label }}
            </template>
            <template #item.action="{ item }">
              <v-btn icon size="small" @click="selectCredential(item)">
                <v-icon color="primary">mdi-plus</v-icon>
              </v-btn>
            </template>
          </v-data-table-server>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-container>
      <v-data-table-server
        :headers="headers"
        :items="jobs"
        :loading="isLoadingJobs"
        :items-per-page="-1"
        hide-default-footer
      >
        <template #item.job_id="{ item }">
          <span>{{ item.job_id }}</span>
        </template>
        <template #item.status="{ item }">
          <span>{{ item.status }}</span>
        </template>
        <template #item.see="{ item }">
          <v-btn size="small" color="primary" class="mr-2" @click="viewLogs(item)">
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
        <template #item.delete="{ item }">
          <v-btn size="small" color="error" @click="deleteJob(item.job_id)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table-server>
    </v-container>
  </v-card>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  name: "JobsView",
  data() {
    return {
      headers: [
        { title: "ID", key: "job_id" },
        { title: "Регион", key: "region.region_name" },
        { title: "Дата создания", key: "created_at" },
        { title: "Статус", key: "status" },
        { title: "", key: "see", sortable: false },
        { title: "", key: "delete", sortable: false },
      ],
      regionHeaders: [
        { title: "", key: "action", sortable: false },
        { title: "Регион", key: "region_name" },
        { title: "Страна", key: "country" },
        
      ],
      credentialHeaders: [
        { title: "", key: "action", sortable: false },
        { title: "Access Token", key: "HH_RU_ACCESS_TOKEN" },
        { title: "Refresh Token", key: "HH_RU_REFRESH_TOKEN" },
        { title: "Client ID", key: "HH_RU_CLIENT_ID" },
        { title: "Client Secret", key: "HH_RU_CLIENT_SECRET" },
        { title: "Redirect URI", key: "HH_RU_REDIRECT_URI" },
        
      ],
      newJobDialog: false,
      regionDialog: false,
      credentialDialog: false,
      selectedRegion: null,
      selectedCredential: null,
    };
  },
  computed: {
    ...mapState({
      jobs: state => state.jobs.list || [],
      isLoadingJobs: state => state.jobs.loading,
      regions: state => state.regions.data || [],
      isLoadingRegions: state => state.regions.loading,
      credentials: state => state.hh_ru_credentials.data || [],
      isLoadingCredentials: state => state.hh_ru_credentials.loading,
    }),

  },
  methods: {
    ...mapActions({
      fetchJobs: "jobs/fetchJobs",
      startJob: "jobs/startJob",
      removeJob: "jobs/deleteJob",
      getRegions: "regions/getRegions",
      getHhRuCredentials: "hh_ru_credentials/getHhRuCredentials",
    }),
    openCreateDialog() {
      this.selectedRegion = null;
      this.selectedCredential = null;
      this.newJobDialog = true;
    },
    cancelCreate() {
      this.newJobDialog = false;
    },
    openRegionDialog() {
      this.regionDialog = true;
    },
    openCredentialDialog() {
      this.credentialDialog = true;
    },
    selectRegion(item) {
      this.selectedRegion = item;
      this.regionDialog = false;
    },
    selectCredential(item) {
      this.selectedCredential = item;
      this.credentialDialog = false;
    },
    async confirmCreate() {
      try {
        const payload = {
          
            region: this.selectedRegion,
            credentials: this.selectedCredential
          
        };
        await this.startJob(payload);
        this.newJobDialog = false;
        await this.fetchJobs();
      } catch (e) {
        console.error("Ошибка при создании задания:", e);
      }
    },
    async deleteJob(id) {
      try {
        await this.removeJob(id);
        await this.fetchJobs();
      } catch (e) {
        console.error("Ошибка при удалении задания:", e);
      }
    },
    viewLogs(job) {
      this.$router.push(`/job/${job.job_id}`);
    },
  },
  async created() {
    await this.fetchJobs();
    await this.getRegions();
    await this.getHhRuCredentials();
  }
};
</script>
