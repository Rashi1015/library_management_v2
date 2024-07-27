import router from "../utils/router.js";

const Navbar = {
    template: `<nav class="navbar navbar-expand-lg bg-body-tertiary">
                    <div class="container-fluid">
                      <a class="navbar-brand" href="#">Library Management System</a>
                      
                      <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                          <li class="nav-item">
                            <a class="nav-link active" aria-current="page" href="/userlogin">Login</a>
                          </li> 
                          <li class="nav-item">
                            <a class="nav-link" href="/userregister">Register</a>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </nav>
    `
}

export default Navbar;