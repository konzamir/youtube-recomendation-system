const { backendHost } = require("../../../config");

import axios from "axios";

const urlEntripoint = backendHost + "/filters";

const defaultHeaders = {
  "Content-Type": "application/json"
};

export default {
  getTags({ dispatch, commit, state }, value) {
    const token = state.user.token;

    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "get",
      url: `${urlEntripoint}/tag/?name=${value}`,
      headers: headers
    });
  },
  getSources({ dispatch, commit, state }, value) {
    const token = state.user.token;

    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "get",
      url: `${urlEntripoint}/source/?name=${value}`,
      headers: headers
    });
  },
  getCategories({ dispatch, commit, state }, value) {
    const token = state.user.token;

    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "get",
      url: `${urlEntripoint}/category/?name=${value}`,
      headers: headers
    });
  }
};
