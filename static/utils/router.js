import user_dashboard from "../pages/user_dashboard.js";
import Home from "../pages/Home.js";
import user_register from "../pages/user_register.js";
import user_login from "../pages/user_login.js";
import librarian_login from "../pages/librarian_login.js";
import librarian_dashboard from "../pages/librarian_dashboard.js";
import user_books from "../pages/user_books.js";
import section_management from "../pages/section_management.js";


const routes = [
    
    {path: "/", component: Home },
    {path: "/userdashboard", component: user_dashboard },
    {path: "/userlogin", component: user_login },
    {path: "/userregister", component: user_register},
    {path: "/librarianlogin", component: librarian_login},
    {path: "/librariandashboard", component: librarian_dashboard },
    {path: "/userbooks", component: user_books },
    {path: "/sectionmanagement", component: section_management },
];

const router = new VueRouter({
    routes
});

export default router;