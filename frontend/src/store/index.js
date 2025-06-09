import { createStore } from "vuex";
import test from "@/store/test";
import regions from "@/store/regions";
import hh_ru_credentials from "@/store/hh_ru_credentials";
import jobs from "@/store/jobs";
import users from "@/store/users";
import data_sources from "@/store/data_sources";
import minstat_workers from "@/store/minstat_workers";
import hh_ru_dataset from "@/store/hh_ru_dataset";
import fgos_dataset from "@/store/fgos_dataset";
import kcp_dataset from "@/store/kcp_dataset";




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
    minstat_workers: minstat_workers,
    hh_ru_dataset: hh_ru_dataset,
    fgos_dataset: fgos_dataset,
    kcp_dataset: kcp_dataset,
  },
});
