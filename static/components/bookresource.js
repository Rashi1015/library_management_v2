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
            <td><button class="btn btn-success" type="submit">Request</button></td>
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
  data() {
    return {};
  }
};

export default Book;
