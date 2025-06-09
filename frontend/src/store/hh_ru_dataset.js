import instance from "@/middlewares";

export default {
  name: "hh_ru_dataset",
  namespaced: true,
  state: () => ({
    data: [],      // [{ id, entry_date, professional_role, vacancies_num }, …]
    loading: false,
    error: null,
  }),
  mutations: {
    setData(state, items) {
      state.data = items;
    },
    addData(state, item) {
      state.data.push(item);
    },
    updateData(state, updated) {
      const i = state.data.findIndex(d => d.id === updated.id);
      if (i !== -1) state.data.splice(i, 1, updated);
    },
    removeData(state, id) {
      state.data = state.data.filter(d => d.id !== id);
    },
    setLoading(state, flag) {
      state.loading = flag;
    },
    setError(state, err) {
      state.error = err;
    },
  },
  actions: {
    // Fetch all records
    async getHhRuDatasets({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.get("/api/hh-ru-dataset/");
        // assume API returns { summaries: [...] }
        commit("setData", resp.data.summaries);
      } catch (e) {
        commit("setError", e.message || "Error fetching data");
      } finally {
        commit("setLoading", false);
      }
    },

    // Create a new record
    async createHhRuDataset({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.post("/api/hh-ru-dataset/", payload);
        commit("addData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Error creating record");
      } finally {
        commit("setLoading", false);
      }
    },

    // Update an existing record
    async updateHhRuDataset({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.put(`/api/hh-ru-dataset/${id}`, payload);
        commit("updateData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Error updating record");
      } finally {
        commit("setLoading", false);
      }
    },

    // Delete a record
    async deleteHhRuDataset({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/hh-ru-dataset/${id}`);
        commit("removeData", id);
      } catch (e) {
        commit("setError", e.message || "Error deleting record");
      } finally {
        commit("setLoading", false);
      }
    },
  },
};
