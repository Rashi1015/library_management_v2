import store from "../utils/store.js";

const Navbar = {
  template: `
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Library Management System</a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item" v-if="isLoggedIn && isAdmin">
              <router-link class="nav-link" to="/librarianbooks">Requests</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn && isAdmin">
              <router-link class="nav-link" to="/addsections">Books</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn && !isAdmin">
              <router-link class="nav-link" to="/userdashboard">All Books</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn && !isAdmin">
              <router-link class="nav-link" to="/userbooks">Your Books</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn && !isAdmin">
              <router-link class="nav-link" to="/userlogin">Login</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn && !isAdmin">
              <router-link class="nav-link" to="/userregister">Register</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <a class="nav-link" :href="url">Logout</a>
            </li>
          </ul>
          <form v-if="isLoggedIn" class="d-flex" role="search" @submit.prevent="performSearch">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
            <button class="btn btn-outline-info" type="submit">Search</button>
          </form>
          <span v-if="isLoggedIn" class="navbar-text ms-2">Welcome, {{ username }}</span>
        </div>
      </div>
    </nav>
  `,
  computed: {
    isLoggedIn() {
      return store.getters.isLoggedIn;
    },
    isAdmin() {
      return store.getters.role === 'admin';
    },
    username() {
      return store.getters.username;
    }
  },
  data() {
    return {
      url: window.location.origin + "/logout",
      searchQuery: "",
    };
  },
  methods: {
    performSearch() {
      this.$emit('search-performed', this.searchQuery);
    }
  }
};

export default Navbar;
