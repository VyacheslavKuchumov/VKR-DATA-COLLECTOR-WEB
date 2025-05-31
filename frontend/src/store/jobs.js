import instance from "@/middlewares";
import WebSocketService from "@/websocket/WebSocketService"; // Предполагается, что у вас есть такой сервис для работы с WebSocket


export default {
  name: "jobs",
  namespaced: true,
  state: () => ({
    list: [],         // массив заданий
    loading: false,   // индикатор загрузки
    error: null,      // текст ошибки
  }),
  mutations: {
    setJobs(state, jobs) {
      state.list = jobs;
    },
    addJob(state, job) {
      state.list.push(job);
    },
    updateJob(state, updated) {
      const index = state.list.findIndex(j => j.job_id === updated.job_id);
      if (index !== -1) {
        state.list.splice(index, 1, updated);
      }
    },
    removeJob(state, jobId) {
      state.list = state.list.filter(j => j.job_id !== jobId);
    },
    setLoading(state, flag) {
      state.loading = flag;
    },
    setError(state, error) {
      state.error = error;
    },
  },
  actions: {
    // Получить список заданий
    async fetchJobs({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.get("/api/jobs/");
        commit("setJobs", response.data);
      } catch (error) {
        commit("setError", error.message || "Ошибка при получении заданий");
      } finally {
        commit("setLoading", false);
      }
    },

    // Запустить новое задание
    async startJob({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.post("/api/jobs/", payload);
        commit("addJob", response.data);
        return response.data.job_id;
      } catch (error) {
        commit("setError", error.message || "Ошибка при создании задания");
        throw error;
      } finally {
        commit("setLoading", false);
      }
    },

    // Обновить существующее задание
    async fetchJob({ commit }, jobId) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.get(`/api/jobs/${jobId}`);
        commit("updateJob", response.data);
      } catch (error) {
        commit("setError", error.message || "Ошибка при получении задания");
      } finally {
        commit("setLoading", false);
      }
    },

    // Подписка на логи через WebSocket
    subscribeLogs({ commit }, { jobId }) {
        const ws = new WebSocketService(jobId);
        ws.connect()
        .then(() => {
            ws.onMessage(line => {
            // dispatch or commit each log line
            commit("addLogLine", { jobId, line });
            });
            ws.onClose(() => {
            console.log(`Logs stream closed for ${jobId}`);
            });
        })
        .catch(err => console.error("WS connect failed:", err));
        return ws;  // so caller can later call ws.disconnect()
    },

    // Отключить WebSocket
    unsubscribeLogs(_, ws) {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    },
  },
};
