import instance from "@/middlewares";

export default {
  name: "kcp_dataset",
  namespaced: true,
  state: () => ({
    data: [], // [{ id, year, study_field_code, study_field_name, kcp_num }, …]
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
    // Fetch all KCP dataset records
    async getKcpDatasets({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.get("/api/kcp-datasets/");
        commit("setData", resp.data.records);
      } catch (e) {
        commit("setError", e.message || "Ошибка при получении данных КЦП");
      } finally {
        commit("setLoading", false);
      }
    },

    // Create a new KCP record
    async createKcpDataset({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.post("/api/kcp-datasets/", payload);
        commit("addData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Ошибка при создании записи КЦП");
      } finally {
        commit("setLoading", false);
      }
    },

    // Update an existing KCP record
    async updateKcpDataset({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.put(`/api/kcp-datasets/${id}`, payload);
        commit("updateData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Ошибка при обновлении записи КЦП");
      } finally {
        commit("setLoading", false);
      }
    },

    // Delete a KCP record
    async deleteKcpDataset({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/kcp-datasets/${id}`);
        commit("removeData", id);
      } catch (e) {
        commit("setError", e.message || "Ошибка при удалении записи КЦП");
      } finally {
        commit("setLoading", false);
      }
    },
  },
};
