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
      registerAction({ dispatch, commit, state }, payload) {
        commit("setLoadingStatus", true);
        return axios({
          method: "post",
          url: `${urlEntripoint}/auth/register/`,
          data: payload,
          headers: defaultHeaders
        });
      },
      loginAction({ dispatch, commit, state }, payload) {
        commit('setLoadingStatus', true);
        return axios({
          method: "post",
          url: `${urlEntripoint}/auth/login/`,
          data: payload,
          headers: defaultHeaders
        });
      },
      logoutAction({ dispatch, commit, state }) {
        commit("setLoadingStatus", true);
    
        const token = state.user.token;
        let headers = {
          Authorization: `Token ${token}`,
          ...defaultHeaders
        };
        return {};
    
        return axios({
          method: "post",
          url: `${urlEntripoint}/auth/logout/`,
          data: {},
          headers: headers
        });
      },
}