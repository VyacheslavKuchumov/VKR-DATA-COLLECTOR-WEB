import instance from "@/middlewares";

export default {
  name: "users",
  namespaced: true,
  state: () => ({
    data: [],          // массив пользователей
    loading: false,    // индикатор загрузки
    error: null,       // текст ошибки
  }),
  mutations: {
    setData(state, users) {
      state.data = users;
    },
    addUser(state, user) {
      state.data.push(user);
    },
    updateUser(state, updated) {
      const index = state.data.findIndex(u => u.id === updated.id);
      if (index !== -1) {
        state.data.splice(index, 1, updated);
      }
    },
    removeUser(state, id) {
      state.data = state.data.filter(u => u.id !== id);
    },
    setLoading(state, flag) {
      state.loading = flag;
    },
    setError(state, error) {
      state.error = error;
    },
  },
  actions: {
    // Получить список пользователей
    async getUsers({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.get("/api/users/");
        // предполагаем, что сервер возвращает { users: [...] }
        commit("setData", response.data.users);
      } catch (error) {
        commit("setError", error.message || "Error fetching users");
      } finally {
        commit("setLoading", false);
      }
    },

    // Создать нового пользователя
    async createUser({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.post("/api/users/", payload);
        commit("addUser", response.data);
      } catch (error) {
        commit("setError", error.message || "Error creating user");
      } finally {
        commit("setLoading", false);
      }
    },

    // Обновить существующего пользователя
    async updateUser({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.put(`/api/users/${id}`, payload);
        commit("updateUser", response.data);
      } catch (error) {
        commit("setError", error.message || "Error updating user");
      } finally {
        commit("setLoading", false);
      }
    },

    // Удалить пользователя
    async deleteUser({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/users/${id}`);
        commit("removeUser", id);
      } catch (error) {
        commit("setError", error.message || "Error deleting user");
      } finally {
        commit("setLoading", false);
      }
    },
  },
};
