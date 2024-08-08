const user_login = {
  template: `
    <div class="container" style="margin-top: 80px;">
      <div class="row justify-content-center">
        <div class="col-md-5">
          <div class="card shadow p-5 border rounded-3">
            <h2 class="card-title text-center">User Login</h2>
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" class="form-control" id="username" v-model="username" placeholder="Username123" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
              </div>
              <div class="text-center">
                <button type="submit" class="btn btn-primary">Login</button>
              </div>
            </form>
            <div class="text-center mt-3">
              --- New user? ---<br>
              <router-link to="/userregister" class="btn btn-warning" style="margin-top:6px;">Register</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      username: '',
      password: '',
      csrfToken: ''
    };
  },
  methods: {
    async login() {
      
      const url = window.location.origin;
      const res = await fetch(url + '/userlogin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      });

      const data = await res.json();
      if (data.redirect) {
        this.$router.push(data.redirect);
      }
      if (res.ok) {
        console.log(data);
        sessionStorage.setItem('auth_token',data.auth_token);
        sessionStorage.setItem('role',data.role);
    
      } 
      else {
        alert(data.error || 'Login failed. Please check your credentials and try again.');
      }
    }
  }
};

export default user_login;
