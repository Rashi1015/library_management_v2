import router from "./utils/router.js";
import Navbar from "./components/Navbar.js";
import store from "./utils/store.js";


new Vue({
  el: "#app",
  template: `
  <div>
      <Navbar/>
      <router-view/>
  </div>
  `,
  router,
  store,
  components: {
      Navbar,
      template: `
        <div class="vw-100 vh-100 ">
        <Navbar/>
        <router-view class = "h-75 w-100 "></router-view>
        </div>
    `,
  },
});

