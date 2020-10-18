export default {
  setRequestData(state, payload) {
    state.setRequestData = {
      currPageToken: payload.curr_page,
      nextPageToken: payload.next_page,
      prevPageToken: payload.prev_page,
      data: payload.data
    };
  },
  removeFeatured(state, videoId) {
    var arr = state.user.links;
    var index = arr.indexOf(videoId);

    if (index > -1) {
      state.user.links.splice(index, 1);
    }
  },
  addFeatured(state, videoId) {
    if (!state.user.links.includes(videoId)) {
      state.user.links.push(videoId);
    }
  }
};
