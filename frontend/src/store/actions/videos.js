import axios from "axios";

const urlEntripoint = "http://localhost:8000/api";

const defaultHeaders = {
  "Content-Type": "application/json"
};

export default {
  getMedia({ dispatch, commit, state }, payload) {
    commit("setLoadingStatus", true);

    return axios({
      method: "post",
      url: `${urlEntripoint}/get-media/`,
      data: payload,
      headers: defaultHeaders
    });
  },
  addFeatured({ dispatch, commit, state }, payload) {
    const token = state.user.token;
    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "post",
      url: `${urlEntripoint}/featured/`,
      data: payload,
      headers: headers
    }).then(response => {
      commit("addFeatured", payload.video_id);
    });
  },
  removeFeatured({ dispatch, commit, state }, payload) {
    const token = state.user.token;
    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "delete",
      url: `${urlEntripoint}/featured/`,
      data: payload,
      headers: headers
    }).then(response => {
      commit("removeFeatured", payload.video_id);
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
