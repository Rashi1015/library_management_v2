import store from "../utils/store.js";

const Navbar = {
  template: `
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Library Management System</a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link v-if="!isLoggedIn" class="nav-link active" to="/userlogin">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link v-if="!isLoggedIn" class="nav-link" to="/userregister">Register</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" v-if="isLoggedIn" :href="url">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  `,
  computed: {
    isLoggedIn() {
      return store.state.loggedIn;
    }
  },
  data(){
    return{
      url: window.location.origin + "/logout",
    };
  }
};

export default Navbar;
