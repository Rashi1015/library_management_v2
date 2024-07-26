import router from "./utils/router.js";
import navbar from "./components/navbar.js";
import store from "./utils/store.js";

new Vue({
  el: "#app",
  template: `
  <h1> app vue </h1>
    `,
  router,
  components: {
    navbar,
  },
});