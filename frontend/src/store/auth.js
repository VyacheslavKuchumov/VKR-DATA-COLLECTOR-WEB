import instance from "@/middlewares";
import router from '@/router'

export default {
  name: "auth",
  namespaced: true,
  state: () => ({
    data: [],          // массив пользователей
    loading: false,    // индикатор загрузки
    error: null,       // текст ошибки
  }),
  mutations: {
    setData(state, data) {
      state.data = data;
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
    async login({ commit }, payload) {
      commit("setLoading", true);
      commit("setError", null);
      try {
        const { email, password } = payload;
        console.log("Logging in with email:", email, "and password:", password);
        const response = await instance.get(`/api/users/auth/${email}`);
        console.log("Response from auth:", response.data);
        localStorage.setItem('id', response.data.id)
        localStorage.setItem('email', response.data.email)
        localStorage.setItem('name', response.data.name)
        localStorage.setItem('role', response.data.role)
        router.push('/')

      } catch (error) {
        commit("setError", error.message || "Error authenticating user");
      } finally {
        commit("setLoading", false);
      }
    },
    logout({ commit }) {
        // Очистка данных пользователя из localStorage
        localStorage.removeItem('id');
        localStorage.removeItem('email');
        localStorage.removeItem('name');
        localStorage.removeItem('role');
    
        // Сброс состояния
        commit("setData", []);
        commit("setLoading", false);
        commit("setError", null);
    }

  },
};
