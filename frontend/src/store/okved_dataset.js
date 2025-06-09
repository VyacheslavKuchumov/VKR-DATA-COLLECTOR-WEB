import instance from "@/middlewares";

export default {
  name: "okved_dataset",
  namespaced: true,
  state: () => ({
    data: [], // [{ id, okved_code, okved_name }, …]
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
      const index = state.data.findIndex(d => d.id === updated.id);
      if (index !== -1) state.data.splice(index, 1, updated);
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
    // Fetch all OKVED dataset records
    async getOkvedDatasets({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.get("/api/okved-datasets/");
        commit("setData", resp.data.records);
      } catch (e) {
        commit("setError", e.message || "Error fetching OKVED data");
      } finally {
        commit("setLoading", false);
      }
    },

    // Create a new OKVED record
    async createOkvedDataset({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.post("/api/okved-datasets/", payload);
        commit("addData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Error creating OKVED record");
      } finally {
        commit("setLoading", false);
      }
    },

    // Update an existing OKVED record
    async updateOkvedDataset({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.put(`/api/okved-datasets/${id}`, payload);
        commit("updateData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Error updating OKVED record");
      } finally {
        commit("setLoading", false);
      }
    },

    // Delete an OKVED record
    async deleteOkvedDataset({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/okved-datasets/${id}`);
        commit("removeData", id);
      } catch (e) {
        commit("setError", e.message || "Error deleting OKVED record");
      } finally {
        commit("setLoading", false);
      }
    },
  },
};
