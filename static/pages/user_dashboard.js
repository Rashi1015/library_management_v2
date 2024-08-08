import Book from "../components/bookresource.js";

const user_dashboard = {
  template: `
    <div id="main">
      <div id="canvas">
        <form @submit.prevent="searchBooks" class="d-flex mb-4">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchWord">
          <button class="btn btn-outline-info" type="submit">Search</button>
        </form>
        <Book :books="books"/>
      </div>
    </div>
  `,
  data() {
    return {
      username: '',
      userId: '',
      searchWord: '',
      books: [],
      auth_token: sessionStorage.getItem('auth_token')
    };
  },
  components: {
    Book
  },
  methods: {
    searchBooks() {
      fetch(`/api/books?search_word=${this.searchWord}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          this.books = data.books;
        })
        .catch(error => console.error('Error:', error));
    },
    createBook(book) {
      fetch('/api/books', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + this.auth_token,
        },
        body: JSON.stringify(book)
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.message || 'Failed to create book');
          });
        }
        return response.json();
      })
      .then(data => {
        alert('Book created successfully');
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error.message);
      });
    }
  },
  mounted() {
    fetch('/api/books')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        this.books = data.books;
        this.username = data.username;
        this.userId = data.user_id;
      })
      .catch(error => console.error('Error:', error));
  }
};

export default user_dashboard;
