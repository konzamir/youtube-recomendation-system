const mutations = {
    initial(state) {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user){
            state.user = user;
        }
    },
    setLoadingStatus(state, p){
        state.isLoading = p;
    },
    removeUser(state) {
        state.user = {
            token:          null,
            username:       '',
            email:          '',
            links:          []
        };
        localStorage.removeItem('user');
    },
    setUser(state, payload) {
        state.user.email    = payload.user.email;
        state.user.username = payload.user.username;
        state.user.id       = payload.user.id;
        state.user.links    = payload.links;
        state.user.token    = payload.token;
        localStorage.setItem('user', JSON.stringify(state.user));
    },
    setRequestData(state, payload) {
        state.setRequestData = {
            currPageToken:  payload.curr_page,
            nextPageToken:  payload.next_page,
            prevPageToken:  payload.prev_page,
            data:           payload.data
        }
    },
    removeFeatured(state, videoId) {
        var arr = state.user.links;
        var index = arr.indexOf(videoId);

        if (index > -1) {
            state.user.links.splice(index, 1);
        }
    },
    addFeatured(state, videoId) {
        if (!state.user.links.includes(videoId)){
            state.user.links.push(videoId);
        }
    }
}

export default mutations;
