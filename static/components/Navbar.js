const Navbar = {
  template: `
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Library Management System</a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link active" aria-current="page" to="/userlogin">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/userregister">Register</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  `
};

export default Navbar;
