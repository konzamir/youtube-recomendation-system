export default {
  removeUser(state) {
    state.user = {
      token: null,
      username: "",
      email: "",
      links: []
    };
  },
  updateUser(state, payload) {
    state.user.email = payload.user.email;
    state.user.username = payload.user.username;
    state.user.id = payload.user.id;
  },
  setUser(state, payload) {
    state.user.email = payload.user.email;
    state.user.username = payload.user.username;
    state.user.id = payload.user.id;
    state.user.links = payload.links;
    state.user.token = payload.token;
  }
};
