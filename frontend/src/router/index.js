import { createRouter, createWebHistory } from "vue-router";
import instance from "@/middlewares";

import WebSocketTest from "@/views/WebsocketTest.vue";
import HomeView from "@/views/HomeView.vue";
import DatasetsView from "@/views/nsi_datasets/DatasetsView.vue";
import DataParsingView from "@/views/data_parsing/DataParsingView.vue";
import UsersView from "@/views/users/UsersView.vue";
import ForecastView from "@/views/forecast/ForecastView.vue";

// parsers
import ProfStandardParsingView from "@/views/data_parsing/prof_standard/ProfStandardParsingView.vue";
import FgosParsingView from "@/views/data_parsing/fgos/FgosParsingView.vue";
import StatOtchetParsingView from "@/views/data_parsing/stat_otchetnost/StatOtchetParsingView.vue";
import OkvedParsingView from "@/views/data_parsing/okved/OkvedParsingView.vue";
import ProfClassificatorParsingView from "@/views/data_parsing/classificator_prof/ProfClassificatorParsingView.vue";
import KcpParsingView from "@/views/data_parsing/kcp/KcpParsingView.vue";
import RegionalPlanParsingView from "@/views/data_parsing/region_plan/RegionalPlanParsingView.vue";
import NationalPlanParsingView from "@/views/data_parsing/national_plan/NationalPlanParsingView.vue";

//datasets
import StatOtchetDatasetView from "@/views/nsi_datasets/stat_otchetnost/StatOtchetDatasetView.vue";
import HHRuDatasetView from "@/views/nsi_datasets/hh_ru/HHRuDatasetView.vue";
import FgosDatasetView from "@/views/nsi_datasets/fgos/FgosDatasetView.vue";
import KcpDatasetView from "@/views/nsi_datasets/kcp/KcpDatasetView.vue";
import ProfStandardView from "@/views/nsi_datasets/prof_standard/ProfStandardView.vue";
import ClassificatorProfDatasetView from "@/views/nsi_datasets/classificator_prof/ClassificatorProfDatasetView.vue";
import OkvedDatasetView from "@/views/nsi_datasets/okved/OkvedDatasetView.vue";

// hh.ru data retrival
import JobsView from "@/views/data_parsing/hh_ru/JobsView.vue";
import JobLogsView from "@/views/data_parsing/hh_ru/JobLogsView.vue";

const routes = [
  // {
  //   path: "/test",
  //   name: "websocket-test",
  //   component: WebSocketTest,
  // },
  {
    path: "/",
    name: "home",
    component: HomeView,
    
  },
  // route for datasets
  {
    path: "/datasets",
    name: "datasets",
    component: DatasetsView,
  },
  // route for data parsing
  {
    path: "/data-parsing",
    name: "data-parsing",
    component: DataParsingView,
  },
  // route for users
  {
    path: "/users",
    name: "users",
    component: UsersView,
  },
  // route for forecast
  {
    path: "/forecast",
    name: "forecast",
    component: ForecastView,
  },
  // route for prof standard parsing
  {
    path: "/data-parsing/profstandards",
    name: "prof-standard-parsing",
    component: ProfStandardParsingView,
  },
  // route for fgos parsing
  {
    path: "/data-parsing/fgos",
    name: "fgos-parsing",
    component: FgosParsingView,
  },
  // route for stat otchet parsing
  {
    path: "/data-parsing/statistics",
    name: "stat-otchet-parsing",
    component: StatOtchetParsingView,
  },
  // route for okved parsing
  {
    path: "/data-parsing/okved",
    name: "okved-parsing",
    component: OkvedParsingView,
  },
  // route for hh.ru jobs parsing
  {
    path: "/data-parsing/hh_ru/jobs",
    name: "hh-ru-jobs-parsing",
    component: JobsView,
  },
  // route for prof classificator parsing
  {
    path: "/data-parsing/prof-classificator",
    name: "prof-classificator-parsing",
    component: ProfClassificatorParsingView,
  },
  // route for kcp parsing
  {
    path: "/data-parsing/kcp",
    name: "kcp-parsing",
    component: KcpParsingView,
  },
  // route for regional plan parsing
  {
    path: "/data-parsing/regional-plan",
    name: "regional-plan-parsing",
    component: RegionalPlanParsingView
  },
  // route for national plan parsing
  {
    path: "/data-parsing/national-plan",
    name: "national-plan-parsing",
    component: NationalPlanParsingView
  },

  // route for stat otchet dataset
  {
    path: "/datasets/stat-otchet",
    name: "stat-otchet-dataset",
    component: StatOtchetDatasetView,
  },
  // route for hh.ru dataset
  {
    path: "/datasets/hh-ru",
    name: "hh-ru-dataset",
    component: HHRuDatasetView,
  },
  // route for fgos dataset
  {
    path: "/datasets/fgos",
    name: "fgos-dataset",
    component: FgosDatasetView,
  },
  // route for kcp dataset
  {
    path: "/datasets/kcp",
    name: "kcp-dataset",
    component: KcpDatasetView,
  },
  // route for prof standard dataset
  {
    path: "/datasets/prof-standard",
    name: "prof-standard-dataset",
    component: ProfStandardView,
  },
  // route for classificator prof dataset
  {
    path: "/datasets/classificator-prof",
    name: "classificator-prof-dataset",
    component: ClassificatorProfDatasetView,
  },
  // route for okved dataset
  {
    path: "/datasets/okved",
    name: "okved-dataset",
    component: OkvedDatasetView,
  },

  // route for hh.ru job logs
  {
    path: "/job/:jobId",
    name: "hh-ru-job-logs",
    component: JobLogsView,
    props: true,
  }
 
 
  
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});



export default router;
