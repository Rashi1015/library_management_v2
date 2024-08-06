const Book = {
  template: `
    <div>
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Book Title</th>
            <th scope="col">Content</th>
            <th scope="col">Author</th>
            <th scope="col">Section</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(book, index) in books" :key="book.id">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ book.name }}</td>
            <td>{{ book.content }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.section.name }}</td>
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
