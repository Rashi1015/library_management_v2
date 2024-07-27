import user_dashboard from "../pages/user_dashboard.js";
import Home from "../pages/Home.js";
import user_register from "../pages/user_register.js";
import user_login from "../pages/user_login.js";
import librarian_login from "../pages/librarian_login.js";

const routes = [
    
    {path: "/", component: Home },
    {path: "/userdashboard", component: user_dashboard },
    {path: "/userlogin", component: user_login },
    {path: "/userregister", component: user_register},
    {path: "/librarianlogin", component: librarian_login},



    
];
const router = new VueRouter({
    routes
});

export default router;