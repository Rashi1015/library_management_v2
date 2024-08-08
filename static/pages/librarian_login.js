const librarian_login = {
  template: `
 <div class="container" style="margin-top: 80px;">
      <div class="row justify-content-center">
        <div class="col-md-5">
          <div class="card shadow p-5 border rounded-3">
            <h2 class="card-title text-center">Librarian Login</h2>
          <form @submit.prevent="login">
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input type="text" class="form-control" id="username" placeholder="username123" v-model="username" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <div style="text-align: center;">
              <button type="submit" class="btn btn-primary">Login</button>
            </div>
          </form>
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
    async login() {
      try {
        const response = await fetch('/librarianlogin', {
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
          alert('Login successful!');
          // You can navigate to the dashboard or another page after successful login
          this.$router.push('/librariandashboard');
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

  export default librarian_login;