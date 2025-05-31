import instance from "@/middlewares";
import axios from "axios";

export default {
  name: "hh_ru_credentials",
  namespaced: true,
  state: () => ({
    data: [],          // массив учетных данных
    loading: false,    // индикатор загрузки
    error: null,       // текст ошибки
  }),
  mutations: {
    setData(state, credentials) {
      state.data = credentials;
    },
    addCredentials(state, credential) {
      state.data.push(credential);
    },
    updateCredentials(state, updated) {
      const index = state.data.findIndex(c => c.id === updated.id);
      if (index !== -1) {
        state.data.splice(index, 1, updated);
      }
    },
    removeCredentials(state, id) {
      state.data = state.data.filter(c => c.id !== id);
    },
    setLoading(state, flag) {
      state.loading = flag;
    },
    setError(state, error) {
      state.error = error;
    },
  },
  actions: {
    // Получить список hh.ru credentials
    async getHhRuCredentials({ commit }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.get("/api/hh-ru-credentials/");
        commit("setData", response.data.credentials);
      } catch (error) {
        commit("setError", error.message || "Error fetching credentials");
      } finally {
        commit("setLoading", false);
      }
    },

    // Создать новые hh.ru credentials
    async createHhRuCredentials({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.post("/api/hh-ru-credentials/", payload);
        commit("addCredentials", response.data);
      } catch (error) {
        commit("setError", error.message || "Error creating credentials");
      } finally {
        commit("setLoading", false);
      }
    },

    // Обновить существующие hh.ru credentials
    async updateHhRuCredentials({ commit }, { id, payload }) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const response = await instance.put(`/api/hh-ru-credentials/${id}`, payload);
        commit("updateCredentials", response.data);
      } catch (error) {
        commit("setError", error.message || "Error updating credentials");
      } finally {
        commit("setLoading", false);
      }
    },

    // Удалить hh.ru credentials
    async deleteHhRuCredentials({ commit }, id) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        await instance.delete(`/api/hh-ru-credentials/${id}`);
        commit("removeCredentials", id);
      } catch (error) {
        commit("setError", error.message || "Error deleting credentials");
      } finally {
        commit("setLoading", false);
      }
    },

    async requestHHRuTokens({ commit }, payload) {
        commit("setLoading", true);
        commit("setError", null);
        try {
        const response = await axios.post(
            "https://hh.ru/oauth/token",

            {
                headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                },
                params: {
                    grant_type:     "authorization_code",
                    client_id:      payload.client_id,
                    client_secret:  payload.client_secret,
                    code:           payload.code,
                    redirect_uri:   payload.redirect_uri,
                },
            }
        );
        return response.data;
        } catch (err) {
        commit("setError", err.message || "Error fetching tokens");
        throw err;
        } finally {
        commit("setLoading", false);
        }
    },

  },
};
