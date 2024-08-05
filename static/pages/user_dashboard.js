const user_dashboard = {
  template: `
    <div id="main">
      <div id="canvas">
        <form @submit.prevent="searchBooks" class="d-flex mb-4">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchWord">
          <button class="btn btn-outline-info" type="submit">Search</button>
        </form>
        <form @submit.prevent="requestBook">
          <input type="hidden" name="user_id" :value="userId">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Book Title</th>
                <th scope="col">Author</th>
                <th scope="col">Section</th>
                <th scope="col">Action</th>
              </tr>
            </thead>
            <tbody class="table-group-divider">
              <tr v-for="(book, index) in books" :key="book.id">
                <th scope="row">{{ index + 1 }}</th>
                <td>{{ book.name }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.section }}</td>
                <td>
                  <button type="button" class="btn btn-success" @click="requestBook(book.id)">Request</button>
                </td>
              </tr>
            </tbody>
          </table>
        </form>
      </div>
    </div>
  `,
  data() {
    return {
      username: '', // Fill in with the actual username data
      userId: '', // Fill in with the actual user ID data
      searchWord: '',
      books: [] // Fill in with the actual book details data
    };
  },
  methods: {
    searchBooks() {
      // Handle search logic here, possibly sending a request to your backend
      fetch(`/userdashboard?search_word=${this.searchWord}`)
        .then(response => response.json())
        .then(data => {
          this.books = data.book_details; // Assuming the response contains a books array
        })
        .catch(error => console.error('Error:', error));
    },
    requestBook(bookId) {
      // Handle book request logic here
      fetch('/userdashboard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': this.csrfToken
        },
        body: JSON.stringify({
          user_id: this.userId,
          book_id: bookId
        })
      }).then(response => {
        if (response.ok) {
          // Handle successful request
          alert('Book requested successfully.');
        } else {
          // Handle error
          alert('Failed to request book. Please try again.');
        }
      }).catch(error => {
        console.error('Error:', error);
      });
    }
  },
  mounted() {
    // Fetch initial book details from the backend
    fetch('/userdashboard')
      .then(response => response.json())
      .then(data => {
        this.books = data.book_details; // Assuming the response contains a books array
        this.username = data.username; // Assuming the response contains the username
        this.userId = data.user_id; // Assuming the response contains the user ID
      })
  }
};

export default user_dashboard;
