import axios from "axios";

const urlEntripoint = "http://localhost:8000/api";

const defaultHeaders = {
  "Content-Type": "application/json"
};

export default {
  getUser({ dispatch, commit, state }, token) {
    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return axios({
      method: "get",
      url: `${urlEntripoint}/auth/user/`,
      headers: headers
    });
  },
  updateUser({ dispatch, commit, state }, payload) {
    const token = state.user.token;
    const user_id = state.user.id;

    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };
    return axios({
      method: "put",
      url: `${urlEntripoint}/auth/user/${user_id}/`,
      headers: headers,
      data: payload
    });
  },
  registerAction({ dispatch, commit, state }, payload) {
    commit("setLoadingStatus", true);
    return axios({
      method: "post",
      url: `${urlEntripoint}/auth/register/`,
      data: payload,
      headers: defaultHeaders
    }).then(res => {
      dispatch("confirmYoutubeAuth", res.data.data.youtube_link);
      return res;
    });
  },
  loginAction({ dispatch, commit, state }, payload) {
    commit("setLoadingStatus", true);
    return axios({
      method: "post",
      url: `${urlEntripoint}/auth/login/`,
      data: payload,
      headers: defaultHeaders
    }).then(res => {
      dispatch("confirmYoutubeAuth", res.data.data.youtube_link);
      return res;
    });
  },
  logoutAction({ dispatch, commit, state }) {
    commit("setLoadingStatus", true);

    const token = state.user.token;
    let headers = {
      Authorization: `Token ${token}`,
      ...defaultHeaders
    };

    return;

    return axios({
      method: "post",
      url: `${urlEntripoint}/auth/logout/`,
      data: {},
      headers: headers
    });
  },
  confirmYoutubeAuth({ dispatch, commit, state }, youtube_link) {
    if (youtube_link) {
      window.open(youtube_link, "_blank", "width=400, height=450");
    }
    return;
  }
};
