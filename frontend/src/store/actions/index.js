import auth from './auth';
import filters from './filters';
import processes from './processes';
import videos from './videos';


const urlEntripoint = "http://localhost:8000/api";

const defaultHeaders = {
  "Content-Type": "application/json"
};

export default {
  initial({ dispatch, commit, state }) {
    commit("initial");
    // if (state.user.token) {
    //   let token = state.user.token;
    //   commit("setLoadingStatus", true);
    //   dispatch("getUser", state.user.token)
    //     .then(response => {
    //       let payload = response.data.data;
    //       payload["token"] = token;
    //       commit("setUser", payload);
    //       commit("setLoadingStatus", false);
    //     })
    //     .catch(err => {
    //       commit("removeUser");
    //       commit("setLoadingStatus", false);
    //     });
    // }
  },
  ...videos,
  ...auth,
  ...filters,
  ...processes
}