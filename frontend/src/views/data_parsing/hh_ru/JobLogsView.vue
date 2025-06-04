<template>
  <v-card max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Логи задачи {{ job()?.job_id || "Загрузка..." }}
    </v-card-title>
  </v-card>

  <v-card class="elevation-5 mt-5 ml-auto mr-auto" max-width="800">
    <v-toolbar flat>
        <v-btn icon="mdi-arrow-left" color="primary" @click="$router.go(-1)" />
        <v-spacer />
      
    </v-toolbar>

    <v-container >
        <v-card
            v-for="(log, index) in (job()?.logs || []).slice().reverse()"
            :key="index"
            class="ma-2 pa-2 elevation-1"
            outlined
            max-width="700"
            elevation="0"
            >
            <v-card-title class="text-h6 text-wrap" >{{ log.text }}</v-card-title>
            <v-card-subtitle>{{ log.timestamp }}</v-card-subtitle>
        </v-card>
    </v-container>
  </v-card>

 
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  name: "JobsView",
  data() {
    return {

    };
  },
  computed: {

  },
  methods: {
    job() {
      return this.$store.state.jobs.job || null;
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
    }),

    async createJob() {
      try {
        await this.startJob();
        await this.fetchJobs();
      } catch (e) {
        console.error("Ошибка при создании задания:", e);
      }
    },


  },
  async created() {
    const job_id = this.$route.params.jobId;
    await this.fetchJob(job_id);
  },

};
</script>
