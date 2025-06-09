import instance from "@/middlewares";

export default {
  name: "prof_standard_dataset",
  namespaced: true,
  state: () => ({
    data: [],         // Список профессиональных стандартов
    loading: false,   // Состояние загрузки
    error: null,      // Сообщение об ошибке
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
    // Получение всех записей
    async getProfStandardDatasets({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.get("/api/prof-standard-datasets/");
        commit("setData", resp.data.records);
      } catch (e) {
        commit("setError", e.message || "Ошибка при получении данных");
      } finally {
        commit("setLoading", false);
      }
    },

    // Создание новой записи
    async createProfStandardDataset({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.post("/api/prof-standard-datasets/", payload);
        commit("addData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Ошибка при создании записи");
      } finally {
        commit("setLoading", false);
      }
    },

    // Обновление существующей записи
    async updateProfStandardDataset({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const resp = await instance.put(`/api/prof-standard-datasets/${id}`, payload);
        commit("updateData", resp.data);
      } catch (e) {
        commit("setError", e.message || "Ошибка при обновлении записи");
      } finally {
        commit("setLoading", false);
      }
    },

    // Удаление записи
    async deleteProfStandardDataset({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/prof-standard-datasets/${id}`);
        commit("removeData", id);
      } catch (e) {
        commit("setError", e.message || "Ошибка при удалении записи");
      } finally {
        commit("setLoading", false);
      }
    },
  },
};
