<template>
  <v-card max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Управление заданиями
    </v-card-title>
  </v-card>

  <v-card class="elevation-5 mt-5 ml-auto mr-auto" max-width="800">
    <v-toolbar flat>
      <v-spacer />
      <v-btn icon="mdi-plus" color="primary" @click="createJob" />
    </v-toolbar>

    <v-container>
      <v-data-table-server
        :headers="headers"
        :items="jobs()"
        :loading="isLoading()"
        :items-per-page="-1"
        hide-default-footer
      >
        <template #item.job_id="{ item }">
          <span>{{ item.job_id }}</span>
        </template>

        <template #item.status="{ item }">
          <span>{{ item.status }}</span>
        </template>

        <template #item.actions="{ item }">
          <v-btn size="small" color="primary" class="mr-2" @click="viewLogs(item)">
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
      </v-data-table-server>
    </v-container>
  </v-card>

  <!-- WebSocket Logs Viewer -->
  <v-dialog v-model="logDialog" max-width="800px">
    <v-card>
      <v-card-title class="text-h5">Логи задания #{{ activeJob?.job_id }}</v-card-title>
      <v-card-text>
        <v-textarea v-model="logText" auto-grow readonly rows="10" />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="closeLogs">Закрыть</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  name: "JobsView",
  data() {
    return {
      headers: [
        { title: "ID", key: "job_id" },
        { title: "Статус", key: "status" },
        { title: "Действия", key: "actions", sortable: false },
      ],
      logDialog: false,
      logText: "",
      activeJob: null,
      ws: null,
    };
  },
  computed: {

  },
  methods: {
    jobs() {
      return this.$store.state.jobs.list || [];
    },
    isLoading() {
      return this.$store.state.jobs.loading;
    },
    error() {
      return this.$store.state.jobs.error;
    },
    ...mapActions({
        fetchJobs: "jobs/fetchJobs",
        startJob: "jobs/startJob",
        subscribeLogs: "jobs/subscribeLogs",
        unsubscribeLogs: "jobs/unsubscribeLogs",
    }),

    async createJob() {
      try {
        await this.startJob();
        await this.fetchJobs();
      } catch (e) {
        console.error("Ошибка при создании задания:", e);
      }
    },

    viewLogs(job) {
      this.activeJob = job;
      this.logText = "";
      this.logDialog = true;
      this.ws = this.subscribeLogs({
        jobId: job.job_id,
        onMessage: (data) => {
          this.logText += data + "\n";
        },
      });
    },

    closeLogs() {
      this.logDialog = false;
      if (this.ws) {
        this.unsubscribeLogs(this.ws);
        this.ws = null;
      }
    },
  },
  async created() {
    await this.fetchJobs();
  },
  beforeDestroy() {
    this.closeLogs(); // Clean up WebSocket if still open
  },
};
</script>
