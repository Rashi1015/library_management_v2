import router from "../utils/router.js";

const Navbar = {
    template: `<nav class="navbar navbar-expand-lg bg-body-tertiary">
                    <div class="container-fluid">
                      <a class="navbar-brand" href="#">User Dashboard</a>
                      
                      <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                          <li class="nav-item">
                            <a class="nav-link active" aria-current="page" href="#">Books</a>
                          </li> 
                          <li class="nav-item">
                            <a class="nav-link" href="/userbooks">My Books</a>
                          </li>
                          <li class="nav-item">
                            <a class="nav-link" href="/userstats">Stats</a>
                          </li>
                          
                          <li class="nav-item">
                            <a class="nav-link" href="/logout">Logout</a>
                          </li>
                        </ul>
                        <div class="d-flex align-items-center">
                          <form class="d-flex" role="search" action="/userdashboard" method="GET">
                              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="search_word">
                              <button class="btn btn-outline-info" type="submit">Search</button>
                          </form>
                          <div class="ms-2">{{ username }}</div>
                        </div>
                      </div>
                    </div>
                  </nav>
    `
}

export default Navbar;