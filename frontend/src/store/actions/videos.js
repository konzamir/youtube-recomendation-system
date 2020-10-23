const { backendHost } = require("../../../config");
import axios from "axios";

const urlEntripoint = backendHost + "/videos";

const defaultHeaders = {
  "Content-Type": "application/json"
};

export default {
  getVideo({ dispatch, commit, state }, videoId) {
    const token = state.user.token;
    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "get",
      url: `${urlEntripoint}/${videoId}/`,
      headers: headers
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
  },
  markVideo({ dispatch, commit, state }, { videoId, userMarks }) {
    const token = state.user.token;
    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "post",
      url: `${urlEntripoint}/${videoId}/setMark/`,
      data: userMarks,
      headers: headers
    });
  }
};
