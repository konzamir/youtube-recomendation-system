const { backendHost } = require("../../../config");
import axios from "axios";

const urlEntripoint = backendHost + "/processes";

const defaultHeaders = {
  "Content-Type": "application/json"
};

export default {
  startProcess({ dispatch, commit, state }, payload) {
    const token = state.user.token;

    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "post",
      url: `${urlEntripoint}/`,
      headers: headers,
      data: payload
    });
  },
  getProcess({ dispatch, commit, state }, process_id) {
    const token = state.user.token;

    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "get",
      url: `${urlEntripoint}/${process_id}/`,
      headers: headers
    });
  },
  setProcessActive({ dispatch, commit, state }, process_id) {
    const token = state.user.token;

    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "patch",
      url: `${urlEntripoint}/${process_id}/`,
      headers: headers,
      data: {
        active: true
      }
    });
  }
};
