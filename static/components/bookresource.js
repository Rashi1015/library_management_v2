const Book = {
  template: `
    <div>
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Book Title</th>
            <th scope="col">Author</th>
            <th scope="col">Section</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(book, index) in books" :key="book.id">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ book.name }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.section.name }}</td>
            <td><button @click="requestBook(book.id)" class="btn btn-success" type="submit">Request</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  props: {
    books: {
      type: Array,
      required: true,
    }
  },
  methods: {
    async requestBook(bookId) {
      try {
        const res = await fetch(window.location.origin + "/api/request_book", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": sessionStorage.getItem("token"),
          },
          body: JSON.stringify({ book_id: bookId }),
        });

        if (res.ok) {
          alert('Book request submitted successfully.');
        } else {
          const errorData = await res.json();
          alert(`Request failed: ${errorData.message}`);
        }
      } catch (error) {
        alert(`An error occurred: ${error.message}`);
      }
    }
  }
};

export default Book;
