import { createRouter, createWebHistory } from "vue-router";
import instance from "@/middlewares";

import WebSocketTest from "@/views/WebsocketTest.vue";
import HomeView from "@/views/HomeView.vue";
import DatasetsView from "@/views/nsi_datasets/DatasetsView.vue";
import DataParsingView from "@/views/data_parsing/DataParsingView.vue";
import UsersView from "@/views/users/UsersView.vue";
import ForecastView from "@/views/forecast/ForecastView.vue";

import ProfStandardParsingView from "@/views/data_parsing/prof_standard/ProfStandardParsingView.vue";
import FgosParsingView from "@/views/data_parsing/fgos/FgosParsingView.vue";

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
 
 
  
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});



export default router;
