import instance from "@/middlewares";

export default {
  name: "minstat_workers",
  namespaced: true,
  state: () => ({
    data: [],          // массив работников Минстата
    loading: false,    // индикатор загрузки
    error: null,       // текст ошибки
  }),
  mutations: {
    setData(state, workers) {
      state.data = workers;
    },
    addWorker(state, worker) {
      state.data.push(worker);
    },
    updateWorker(state, updated) {
      const index = state.data.findIndex(w => w.id === updated.id);
      if (index !== -1) {
        state.data.splice(index, 1, updated);
      }
    },
    removeWorker(state, id) {
      state.data = state.data.filter(w => w.id !== id);
    },
    setLoading(state, flag) {
      state.loading = flag;
    },
    setError(state, error) {
      state.error = error;
    },
  },
  actions: {
    // Получить список работников Минстата
    async getMinstatWorkers({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.get("/api/minstat-workers/");
        // предполагаем, что сервер возвращает { workers: [...] }
        commit("setData", response.data.workers);
      } catch (error) {
        commit("setError", error.message || "Error fetching workers");
      } finally {
        commit("setLoading", false);
      }
    },

    // Создать нового работника Минстата
    async createMinstatWorker({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.post("/api/minstat-workers/", payload);
        commit("addWorker", response.data);
      } catch (error) {
        commit("setError", error.message || "Error creating worker");
      } finally {
        commit("setLoading", false);
      }
    },

    // Обновить работника Минстата
    async updateMinstatWorker({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.put(`/api/minstat-workers/${id}`, payload);
        commit("updateWorker", response.data);
      } catch (error) {
        commit("setError", error.message || "Error updating worker");
      } finally {
        commit("setLoading", false);
      }
    },

    // Удалить работника Минстата
    async deleteMinstatWorker({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/minstat-workers/${id}`);
        commit("removeWorker", id);
      } catch (error) {
        commit("setError", error.message || "Error deleting worker");
      } finally {
        commit("setLoading", false);
      }
    },
  },
};
