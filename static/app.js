import router from "./utils/router.js";
import Navbar from "./components/Navbar.js";
import store from "./utils/store.js";

new Vue({
  el: "#app",
  template: `
    <div>
      <Navbar @search-performed="handleSearch" @show-all-books="handleShowAllBooks" />
      <router-view :search-query="searchQuery"/>
    </div>
  `,
  router,
  store,
  data() {
    return {
      searchQuery: "",
      allBooks: [], // Store all books here
      
    };
  },
  methods: {
    handleSearch(query) {
      this.searchQuery = query;
    },
    handleShowAllBooks() {
      this.searchQuery = ""; // Clear search query to show all books
    },
    updateAllBooks(books) {
      this.allBooks = books;
    }
  },
  components: { Navbar },
});