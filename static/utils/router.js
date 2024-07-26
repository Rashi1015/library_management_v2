import Home from "../pages/Home.js";
import navbar from "../components/navbar.js";

const routes = [
    { path: "/", component: Home }]

const router = new VueRouter({
        routes,
      });

export default router;    