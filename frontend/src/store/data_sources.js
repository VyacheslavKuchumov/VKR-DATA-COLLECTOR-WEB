import instance from "@/middlewares";

export default {
  name: "data_sources",
  namespaced: true,
  state: () => ({
    data: [],          // массив источников данных
    loading: false,    // индикатор загрузки
    error: null,       // текст ошибки
  }),
  mutations: {
    setData(state, sources) {
      state.data = sources;
    },
    addSource(state, source) {
      state.data.push(source);
    },
    updateSource(state, updated) {
      const index = state.data.findIndex(s => s.id === updated.id);
      if (index !== -1) {
        state.data.splice(index, 1, updated);
      }
    },
    removeSource(state, id) {
      state.data = state.data.filter(s => s.id !== id);
    },
    setLoading(state, flag) {
      state.loading = flag;
    },
    setError(state, error) {
      state.error = error;
    },
  },
  actions: {
    // Получить список всех источников
    async getDataSources({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.get("/api/data-sources/");
        // предполагаем, что сервер возвращает { sources: [...] }
        commit("setData", response.data.sources);
      } catch (error) {
        commit("setError", error.message || "Error fetching data sources");
      } finally {
        commit("setLoading", false);
      }
    },

    // Получить источники по типу
    async getDataSourcesByType({ commit }, sourceType) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.get(`/api/data-sources/type/${sourceType}`);
        commit("setData", response.data.sources);
      } catch (error) {
        commit("setError", error.message || "Error fetching data sources by type");
      } finally {
        commit("setLoading", false);
      }
    },

    // Создать новый источник
    async createDataSource({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.post("/api/data-sources/", payload);
        commit("addSource", response.data);
      } catch (error) {
        commit("setError", error.message || "Error creating data source");
      } finally {
        commit("setLoading", false);
      }
    },

    // Обновить существующий источник
    async updateDataSource({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.put(`/api/data-sources/${id}`, payload);
        commit("updateSource", response.data);
      } catch (error) {
        commit("setError", error.message || "Error updating data source");
      } finally {
        commit("setLoading", false);
      }
    },

    // Удалить источник
    async deleteDataSource({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/data-sources/${id}`);
        commit("removeSource", id);
      } catch (error) {
        commit("setError", error.message || "Error deleting data source");
      } finally {
        commit("setLoading", false);
      }
    },
  },
};
