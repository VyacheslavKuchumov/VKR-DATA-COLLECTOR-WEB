import instance from "@/middlewares";


export default {
  name: "test",
  state: () => ({
    data: null,

  }),
  mutations: {
    setData(state, data) {
      state.data = data;
    },

  },
  actions: {
    async fetchData({ commit }) {
      try {
        const response = await instance.get("/api/okved_sections/");
        commit("setData", response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    
  },

  namespaced: true,
};
