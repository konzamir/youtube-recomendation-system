import axios from 'axios';

const urlEntripoint = "http://localhost:8000/api"

const defaultHeaders = {
    "Content-Type": "application/json",
}

const actions = {
    initial({dispatch, commit, state}){
        commit('initial')
        if (state.user.token){
            let token = state.user.token;
            commit('setLoadingStatus', true);
            dispatch('getUser', state.user.token)
            .then((response) => {
                let payload = response.data.data;
                payload['token'] = token;
                commit("setUser", payload);
                commit('setLoadingStatus', false);
            })
            .catch((err) => {
                commit('removeUser');
                commit('setLoadingStatus', false);
            })
        }
    },
    getUser({dispatch, commit, state}, token) {
        let headers = {
            'Authorization': `Token ${token}`,
            ...defaultHeaders
        };

        return axios({
            method: 'get',
            url: `${urlEntripoint}/auth/user/`,
            headers: headers
        })
    },
    registerAction({dispatch, commit, state}, payload){
        commit('setLoadingStatus', true);
        return axios({
            method: 'post',
            url: `${urlEntripoint}/auth/register/`,
            data: payload,
            headers: defaultHeaders
        })
    },
    loginAction({dispatch, commit, state}, payload){
        commit('setLoadingStatus', true);
        return axios({
            method: 'post',
            url: `${urlEntripoint}/auth/login/`,
            data: payload,
            headers: defaultHeaders
        })
    },
    logoutAction({dispatch, commit, state}){
        commit('setLoadingStatus', true);

        const token = state.user.token;
        let headers = {
            'Authorization': `Token ${token}`,
            ...defaultHeaders
        };

        return axios({
            method: 'post',
            url: `${urlEntripoint}/auth/logout/`,
            data: {},
            headers: headers
        })
    },
    getMedia({dispatch, commit, state}, payload){
        // commit('setLoadingStatus', true);

        return axios({
            method: 'post',
            url: `${urlEntripoint}/get-media/`,
            data: payload,
            headers: defaultHeaders
        })
    },
    addFeatured({dispatch, commit, state}, payload) {
        const token = state.user.token;
        let headers = {
            'Authorization': `Token ${token}`,
            ...defaultHeaders
        };

        return axios({
            method: 'post',
            url: `${urlEntripoint}/featured/`,
            data: payload,
            headers: headers
        }).then((response) => {
            // commit('addFeatured', payload.video_id);
        })
    },
    removeFeatured({dispatch, commit, state}, payload) {
        const token = state.user.token;
        let headers = {
            'Authorization': `Token ${token}`,
            ...defaultHeaders
        };

        return axios({
            method: 'delete',
            url: `${urlEntripoint}/featured/`,
            data: payload,
            headers: headers
        }).then((response) => {
            // commit('removeFeatured', payload.video_id);
        })
    },
    getFeaturedList({dispatch, commit, state}) {
        const token = state.user.token;
        let headers = {
            'Authorization': `Token ${token}`,
            ...defaultHeaders
        };

        return axios({
            method: 'get',
            url: `${urlEntripoint}/featured/`,
            headers: headers
        })
    }
}

export default actions;
