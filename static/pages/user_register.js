const user_register = {
  template: `
  <div class="container" style="margin-top: 80px;">
      <div class="row justify-content-center">
        <div class="col-md-5">
           <div class="card shadow p-5 border rounded-3">
         
              <h2 class="card-title text-center">Register Form</h2>
              <form @submit.prevent="register">
                <div class="mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input type="text" class="form-control" id="username" v-model="username" placeholder="Username123" required>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" class="form-control" id="password" v-model="password" required>
                </div>
                <div class="text-center">
                  <button type="submit" class="btn btn-primary">Register</button>
                </div>
              </form>
              <div class="text-center mt-3">
                --- Already registered? ---<br>
                <router-link to="/userlogin" class="btn btn-warning" style="margin-top:5px;">Login</router-link>
              </div>
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
    register() {
      // Handle register logic here
      fetch('/userregister', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      }).then(response => {
        if (response.ok) {
          // Redirect to login page or handle success
          this.$router.push('/userlogin');
        } else {
          // Handle error
          alert('Registration failed. Please try again.');
        }
      }).catch(error => {
        console.error('Error:', error);
      });
    }
  }
};

export default user_register;
