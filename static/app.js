import router from "./utils/router.js";
import Navbar from "./components/Navbar.js";
<<<<<<< HEAD
import store from "./utils/store.js";
=======
///import store from "./utils/store.js";
>>>>>>> 2141b474c42fe16d044c17c353ad8acc9eebfe31

new Vue({
  el: "#app",
  template: `
<<<<<<< HEAD
  <div>
    <Navbar/>
    <router-view/>
    </div>
=======
  <h1> app vue </h1>
>>>>>>> 2141b474c42fe16d044c17c353ad8acc9eebfe31
    `,
  router,
  components: {
    Navbar,
  },
});