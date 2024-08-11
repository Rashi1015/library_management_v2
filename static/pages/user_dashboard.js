import Book from "../components/bookresource.js";

const user_dashboard = {
  template: `
    <div id="main">
      <div id="canvas">
        <Book :books="filteredBooks" />
      </div>
    </div>
  `,
  props: ['searchQuery'], // Receive searchQuery from app.js
  data() {
    return {
      books: [],
      filteredBooks: [],
    };
  },
  async mounted() {
    const res = await fetch(window.location.origin + "/api/books", {
      headers: {
        "Authentication-Token": sessionStorage.getItem("token"),
      },
    });

    if (res.ok) {
      const data = await res.json();
      this.books = data;
      this.filteredBooks = data; // Initially, show all books
      this.$root.updateAllBooks(data); // Update allBooks in app.js
    }
  },
  watch: {
    searchQuery: 'filterBooks' // Watch for changes in searchQuery
  },
  methods: {
    filterBooks(searchQuery) {
      if (searchQuery === "") {
        this.filteredBooks = this.books; // Show all books if search query is empty
      } else {
        const lowerCaseQuery = searchQuery.toLowerCase();
        this.filteredBooks = this.books.filter(book => {
          return (
            book.name.toLowerCase().includes(lowerCaseQuery) ||
            book.author.toLowerCase().includes(lowerCaseQuery) ||
            book.section.name.toLowerCase().includes(lowerCaseQuery)
          );
        });
      }
    }
  },
  components: { Book }
};

export default user_dashboard;
