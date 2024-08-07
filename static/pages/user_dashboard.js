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
      books : [],
    };
  },
  async mounted() {
    const res = await fetch(window.location.origin + "/api/books", {
      headers: {
        "Authentication-Token": sessionStorage.getItem("token"),
      },
    });
    console.log(res.ok);

    if (res.ok) {
      const data = await res.json();
      this.books = data;
    }
  },
  components: { Book },
};

export default user_dashboard;
