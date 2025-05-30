import { createStore } from "vuex";
import test from "@/store/test";
import regions from "./regions";




export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    test: test,
    regions: regions,
  },
});
