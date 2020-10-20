import axios from "axios";

const urlEntripoint = "http://localhost:8000/api/videos";

const defaultHeaders = {
  "Content-Type": "application/json"
};

export default {
  getMedia({ dispatch, commit, state }, payload) {
    // commit("setLoadingStatus", true);

    return axios({
      method: "post",
      url: `${urlEntripoint}/get-media/`,
      data: payload,
      headers: defaultHeaders
    });
  },
  addFeatured({ dispatch, commit, state }, videoId) {
    const token = state.user.token;
    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "post",
      url: `${urlEntripoint}/${videoId}/featured/`,
      headers: headers
    }).then(response => {
      commit("addFeatured", videoId);
    });
  },
  removeFeatured({ dispatch, commit, state }, videoId) {
    const token = state.user.token;
    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "delete",
      url: `${urlEntripoint}/${videoId}/featured/`,
      headers: headers
    }).then(response => {
      commit("removeFeatured", videoId);
    });
  },
  getFeaturedList({ dispatch, commit, state }) {
    const token = state.user.token;
    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "get",
      url: `${urlEntripoint}/featured/`,
      headers: headers
    });
  }
};
