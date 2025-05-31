import { createRouter, createWebHistory } from "vue-router";
import instance from "@/middlewares";

import HomeView from "@/views/HomeView.vue";
import RegionsView from "@/views/spravochniki/RegionsView.vue";
import WebSocketTest from "@/views/WebsocketTest.vue";
import HHRuCredentialsView from "@/views/spravochniki/HHRuCredentialsView.vue";


const routes = [
  {
    path: "/test",
    name: "websocket-test",
    component: WebSocketTest,
  },
  {
    path: "/",
    name: "home",
    component: HomeView,
    
  },
  {
    path: "/regions",
    name: "regions",
    component: RegionsView,
  },
  {
    path: "/hh-ru-credentials",
    name: "hh-ru-credentials",
    component: HHRuCredentialsView,
  },
 
  
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});



export default router;
