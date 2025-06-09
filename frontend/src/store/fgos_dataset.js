import instance from "@/middlewares";

export default {
  name: "fgos_dataset",
  namespaced: true,
  state: () => ({
    data: [], // [{ id, entry_date, okpd_code, okpd_title, vacancy_percent, avg_salary }, …]
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
    // Fetch all FGOS dataset records
    async getFgosDatasets({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.get("/api/fgos-dataset/");
        // assuming API returns { summaries: [...] }
        commit("setData", resp.data.records);
      } catch (e) {
        commit("setError", e.message || "Error fetching FGOS data");
      } finally {
        commit("setLoading", false);
      }
    },

    // Create a new FGOS record
    async createFgosDataset({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.post("/api/fgos-dataset/", payload);
        commit("addData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Error creating FGOS record");
      } finally {
        commit("setLoading", false);
      }
    },

    // Update an existing FGOS record
    async updateFgosDataset({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.put(`/api/fgos-dataset/${id}`, payload);
        commit("updateData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Error updating FGOS record");
      } finally {
        commit("setLoading", false);
      }
    },

    // Delete a FGOS record
    async deleteFgosDataset({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/fgos-dataset/${id}`);
        commit("removeData", id);
      } catch (e) {
        commit("setError", e.message || "Error deleting FGOS record");
      } finally {
        commit("setLoading", false);
      }
    },
  },
};
