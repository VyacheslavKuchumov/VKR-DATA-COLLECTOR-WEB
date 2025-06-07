import { createStore } from "vuex";
import test from "@/store/test";
import regions from "@/store/regions";
import hh_ru_credentials from "@/store/hh_ru_credentials";
import jobs from "@/store/jobs";
import users from "@/store/users";
import data_sources from "@/store/data_sources";




export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    test: test,
    regions: regions,
    hh_ru_credentials: hh_ru_credentials,
    jobs: jobs,
    users: users,
    data_sources: data_sources,
  },
});
