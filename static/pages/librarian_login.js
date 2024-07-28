const librarian_login = {
  template: `
    <div class="container" style="margin-top: 80px;">
      <div class="row justify-content-center">
        <div class="col-md-5">
          <div class="card">
            <div class="card-body">
              <h1 class="card-title text-center">Librarian Login</h1>
              <form @submit.prevent="login">
                <div class="mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input type="text" class="form-control" id="username" v-model="username" placeholder="username123" required>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" class="form-control" id="password" v-model="password" required>
                </div>
                <div class="text-center">
                  <button type="submit" class="btn btn-primary">Login</button>
                </div>
              </form>
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
    login() {
      // Handle login logic here
      fetch('/librarianlogin', {
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
          // Redirect to the librarian dashboard or handle success
          alert('Login successful');
          // this.$router.push('/librariandashboard');
        } else {
          // Handle error
          alert('Login failed. Please try again.');
        }
      }).catch(error => {
        console.error('Error:', error);
      });
    }
  }
};

export default librarian_login;
