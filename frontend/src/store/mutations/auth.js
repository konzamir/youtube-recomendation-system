export default {
  removeUser(state) {
    state.user = {
      token: null,
      username: "",
      email: "",
      links: []
    };
    localStorage.removeItem("user");
  },
  setUser(state, payload) {
    state.user.email = payload.user.email;
    state.user.username = payload.user.username;
    state.user.id = payload.user.id;
    state.user.links = payload.links;
    state.user.token = payload.token;
    localStorage.setItem("user", JSON.stringify(state.user));
  }
};
