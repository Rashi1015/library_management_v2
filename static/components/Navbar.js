import store from "../utils/store.js";

const Navbar = {
  template: `
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Library Management System</a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link v-if="!loggedIn" class="nav-link active" to="/userlogin">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link v-if="!loggedIn" class="nav-link" to="/userregister">Register</router-link>
            </li>
<<<<<<< HEAD
            <li class="nav-item">
            <a class="nav-link" :href="url">Logout</a>
            </li>
=======
>>>>>>> cb12977f941f54add696c249b534e2d962495bdb
          </ul>
        </div>
      </div>
    </nav>
<<<<<<< HEAD
  `,
  data(){
    return{
      loggedIn : store.state.loggedIn,
      url: window.location.origin + "/logout",
    };
   
  }
=======
  `
>>>>>>> cb12977f941f54add696c249b534e2d962495bdb
};

export default Navbar;
