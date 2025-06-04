import { createRouter, createWebHistory } from "vue-router";
import instance from "@/middlewares";

import WebSocketTest from "@/views/WebsocketTest.vue";
import HomeView from "@/views/HomeView.vue";
import DatasetsView from "@/views/nsi_datasets/DatasetsView.vue";
import DataParsingView from "@/views/data_parsing/DataParsingView.vue";




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

 
 
  
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});



export default router;
