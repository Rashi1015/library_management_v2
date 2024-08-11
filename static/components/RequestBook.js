const RequestBook = {
    template: `
      <div>
        <h2 class="headings">Requested Books</h2>
        <table class="table table-hover" v-if="requestedBooks.length > 0">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Book Title</th>
              <th scope="col">Author</th>
              <th scope="col">Section</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(request, index) in requestedBooks" :key="request.id">
              <th scope="row">{{ index + 1 }}</th>
              <td>{{ request.book.name }}</td>
              <td>{{ request.book.author }}</td>
              <td>{{ request.book.section.name }}</td>
              <td>{{ request.status }}</td>
            </tr>
          </tbody>
        </table>
        <p class="headings" v-if="requestedBooks.length === 0">No requested books</p>
    
        <h2 class="headings">Current Books</h2>
        <table class="table table-hover" v-if="issuedBooks.length > 0">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Book Title</th>
              <th scope="col">Author</th>
              <th scope="col">Section</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(request, index) in issuedBooks" :key="request.id">
              <th scope="row">{{ index + 1 }}</th>
              <td>{{ request.book.name }}</td>
              <td>{{ request.book.author }}</td>
              <td>{{ request.book.section.name }}</td>
              <td>{{ request.status }}</td>
            </tr>
          </tbody>
        </table>
        <p class="headings" v-if="issuedBooks.length === 0">No books</p>
    
        <h2 class="headings">Downloaded Books</h2>
        <table class="table table-hover" v-if="paidBooks.length > 0">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Book Title</th>
              <th scope="col">Author</th>
              <th scope="col">Section</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(request, index) in paidBooks" :key="request.id">
              <th scope="row">{{ index + 1 }}</th>
              <td>{{ request.book.name }}</td>
              <td>{{ request.book.author }}</td>
              <td>{{ request.book.section.name }}</td>
              <td>{{ request.status }}</td>
            </tr>
          </tbody>
        </table>
        <p class="headings" v-if="paidBooks.length === 0">No downloaded books</p>
      </div>
    `,
    props: {
      requestedBooks: {
        type: Array,
        required: true,
      },
      issuedBooks: {
        type: Array,
        required: true,
      },
      paidBooks: {
        type: Array,
        required: true,
      }
    }
  };
  
  export default RequestBook;
  