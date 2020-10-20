export default {
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
