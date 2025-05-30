import { createRouter, createWebHistory } from "vue-router";
import instance from "@/middlewares";

import HomeView from "@/views/HomeView.vue";




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
    meta: { auth: true },
  },
 
  
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});



export default router;
