import Vue from "vue";
import VueRouter from "vue-router";
import Login from "@/views/Login.vue";
import Dashboard from "@/views/Dashboard.vue";
import Home from "@/views/Home.vue";
import { getCheckLoggedIn } from "@/api";

Vue.use(VueRouter);

/**
 * A list of routes
 */
const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      public: true,
    }
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: {
      public: true,
    }
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "*",
    // When the path entered by the user doesn't match,
    // then he will be redirected to /login
    redirect: "/",
  }
];

/**
 * Creates the VueRouter object.
 */
const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

/**
 * Before redirecting the user to a certain route,
 * the beforeEach method checks if the route is
 * public, otherwise the presence of an access token
 * will be checked. If no access token available, the
 * user will be redirected to the Login view.
 */
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.public)) {
    /**
     * The axios interceptor handles all error responses
     * with the standard Notification handler.
     */
    getCheckLoggedIn(false);
    next();
  } else {
    /**
     * An error response wouldn't be shown as
     * a notificatione by the axios interceptor.
     */
    getCheckLoggedIn(true);
    next();
  }
});

export default router;
