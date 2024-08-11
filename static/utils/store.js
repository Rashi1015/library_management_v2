Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
      loggedIn: false,
      role: "",
      username: ""
    },
    mutations: {
      setLogin(state, { username, role }) {
        console.log("setLogin mutation called with username:", username);
        state.loggedIn = true;
        state.username = username;
        state.role = role;
        console.log("State after setLogin:", state);
      },
      logout(state) {
        state.loggedIn = false;
        state.username = ""; // Clear the username on logout
        state.role="";
      },
      setRole(state, role) {
        state.role = role;
      }
    },
    getters: {
      isLoggedIn(state) {
        return state.loggedIn;
      },
      username(state) {
        return state.username;
      },
      role(state){
        return state.role;
      }
    }
  });
  
  export default store;
  