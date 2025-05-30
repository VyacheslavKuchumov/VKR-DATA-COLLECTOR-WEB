import instance from "@/middlewares";

export default {
  name: "regions",
  namespaced: true,
  state: () => ({
    data: [],          // массив регионов
    loading: false,    // индикатор загрузки
    error: null,       // текст ошибки
  }),
  mutations: {
    setData(state, regions) {
      state.data = regions;
    },
    addRegion(state, region) {
      state.data.push(region);
    },
    updateRegion(state, updated) {
      const index = state.data.findIndex(r => r.id === updated.id);
      if (index !== -1) {
        state.data.splice(index, 1, updated);
      }
    },
    removeRegion(state, id) {
      state.data = state.data.filter(r => r.id !== id);
    },
    setLoading(state, flag) {
      state.loading = flag;
    },
    setError(state, error) {
      state.error = error;
    },
  },
  actions: {
    // Получить список регионов
    async getRegions({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.get("/api/regions/");
        commit("setData", response.data.regions);
      } catch (error) {
        commit("setError", error.message || "Error fetching regions");
      } finally {
        commit("setLoading", false);
      }
    },

    // Создать новый регион
    async createRegion({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.post("/api/regions/", payload);
        commit("addRegion", response.data);
      } catch (error) {
        commit("setError", error.message || "Error creating region");
      } finally {
        commit("setLoading", false);
      }
    },

    // Обновить существующий регион
    async updateRegion({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.put(`/api/regions/${id}`, payload);
        commit("updateRegion", response.data);
      } catch (error) {
        commit("setError", error.message || "Error updating region");
      } finally {
        commit("setLoading", false);
      }
    },

    // Удалить регион
    async deleteRegion({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/regions/${id}`);
        commit("removeRegion", id);
      } catch (error) {
        commit("setError", error.message || "Error deleting region");
      } finally {
        commit("setLoading", false);
      }
    },
  },
  getters: {
    allRegions(state) {
      return state.data;
    },
    isLoading(state) {
      return state.loading;
    },
    errorMessage(state) {
      return state.error;
    },
  },
};
