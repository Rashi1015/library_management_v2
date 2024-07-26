import router from "./utils/router.js";
import navbar from "./components/navbar.js";


new Vue({
  el: "#app",
  template: `
  <div>
      <Navbar/>
      <router-view/>
  </div>
  `,
  router,
  components: {
      navbar,
  },
});

