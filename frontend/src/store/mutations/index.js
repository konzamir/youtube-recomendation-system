import auth from './auth';
import filters from './filters';
import processes from './processes';
import videos from './videos';


export default {
  initial(state) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (user) {
      state.user = user;
    }
  },
  setLoadingStatus(state, p) {
    state.isLoading = p;
  },
    ...videos,
    ...auth,
    ...filters,
    ...processes
}