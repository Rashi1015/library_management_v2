import RequestBook from "../components/RequestBook.js"; // Import the RequestBook component

const user_books = {
  template: `
    <div id="main">
      <div id="canvas">
        <RequestBook
          :requestedBooks="requestedBooks"
          :issuedBooks="issuedBooks"
          :paidBooks="paidBooks"
        />
      </div>
    </div>
  `,
  data() {
    return {
      requestedBooks: [],
      issuedBooks: [],
      paidBooks: [],
    };
  },
  async mounted() {
    try {
      const res = await fetch(window.location.origin + "/api/request_book", {
        headers: {
          "Authentication-Token": sessionStorage.getItem("token"),
        },
      });

      if (res.ok) {
        const data = await res.json();
        // Assuming the API returns data categorized by status
        this.requestedBooks = data.filter(book => book.status === 'requested');
        this.issuedBooks = data.filter(book => book.status === 'issued');
        this.paidBooks = data.filter(book => book.status === 'paid');
      } else {
        const errorData = await res.json();
        alert(`Failed to fetch requests: ${errorData.message}`);
      }
    } catch (error) {
      alert(`An error occurred: ${error.message}`);
    }
  },
  components: { RequestBook }
};

export default user_books;
