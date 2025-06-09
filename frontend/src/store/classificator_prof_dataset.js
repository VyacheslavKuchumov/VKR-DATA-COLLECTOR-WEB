import instance from "@/middlewares";

export default {
  name: "classificator_prof_dataset",
  namespaced: true,
  state: () => ({
    data: [], // [{ id, prof_code, prof_name }, …]
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
    // Fetch all profession records
    async getProfDatasets({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.get("/api/classificator-prof-datasets/");
        commit("setData", resp.data.records);
      } catch (e) {
        commit("setError", e.message || "Error fetching profession records");
      } finally {
        commit("setLoading", false);
      }
    },

    // Create a new profession record
    async createProfDataset({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.post("/api/classificator-prof-datasets/", payload);
        commit("addData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Error creating profession record");
      } finally {
        commit("setLoading", false);
      }
    },

    // Update an existing profession record
    async updateProfDataset({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.put(`/api/classificator-prof-datasets/${id}`, payload);
        commit("updateData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Error updating profession record");
      } finally {
        commit("setLoading", false);
      }
    },

    // Delete a profession record
    async deleteProfDataset({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/classificator-prof-datasets/${id}`);
        commit("removeData", id);
      } catch (e) {
        commit("setError", e.message || "Error deleting profession record");
      } finally {
        commit("setLoading", false);
      }
    },
  },
};
