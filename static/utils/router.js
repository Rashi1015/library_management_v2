//import user_dashboard from "../pages/user_dashboard.js";
import Home from "../pages/Home.js";

const routes = [
    
    {path: "/", component: Home },
    
];
const router = new VueRouter({
    routes
});

export default router;