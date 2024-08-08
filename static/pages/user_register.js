import router from "../utils/router.js";

const user_register= {
  template: `
  <div class="container" style="margin-top: 80px;">
      <div class="row justify-content-center">
        <div class="col-md-5">
          <div class="card shadow p-5 border rounded-3">
            <h2 class="card-title text-center">Register Form</h2>
          <form @submit.prevent="register"> 
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input type="text" class="form-control" id="username" placeholder="Username123" v-model="username" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <div style="text-align: center;">
              <button type="submit" class="btn btn-primary">Register</button>
            </div>
          </form>
          <div style="text-align: center; margin-top: 20px;">
            ---Already registered?---<br>
            <router-link to="/userlogin" class="btn btn-warning" style="margin-top:6px;">Login</router-link>
          </div>
        </div>
      </div>
    </div>
    </div>
  `,
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async register() {
      try {
        const response = await fetch('/userregister', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });

        if (response.ok) {
          alert('Registration successful!');
          this.$router.push('/userlogin');
        } else {
          const error = await response.json();
          alert(`Error: ${error.message}`);
        }
      } catch (error) {
        alert(`Error: ${error.message}`);
      }
    }
  }
};

export default user_register;
