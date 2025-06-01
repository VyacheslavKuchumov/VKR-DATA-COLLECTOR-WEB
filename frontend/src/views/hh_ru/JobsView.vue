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

        <template #item.see="{ item }">
          <v-btn size="small" color="primary" class="mr-2" @click="viewLogs(item)">
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
        <template #item.delete="{ item }">
          <v-btn
            size="small"
            color="error"
            @click="deleteJob(item.job_id)"
          >
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
        { title: "Статус", key: "status" },
        { title: "", key: "see", sortable: false },
        // { title: "", key: "delete", sortable: false },
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
        fetchJob: "jobs/fetchJob",
        deleteJob: "jobs/deleteJob",
    }),

    async createJob() {
      try {
        await this.startJob();
        await this.fetchJobs();
      } catch (e) {
        console.error("Ошибка при создании задания:", e);
      }
    },
    async deleteJob(jobId) {
      try {
        await this.deleteJob(jobId);
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
  },

};
</script>
