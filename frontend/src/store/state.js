const state = {
  isLoading: false,
  user: {
    token: null,
    username: "",
    email: "",
    links: []
  },

  videos: [],

  gettingFeaturedKeyPhrase: "#featured-media",

  process: {
    id: 0,
    status: 0,
    search_data: "",
    next_process: null,
    prev_process: null
  },
  processStatuses: {
    0: "Waiting for fetching base data...",
    1: "Waiting for fetching full data...",
    2: "Waiting for filtering...",
    3: "Success!",
    4: "Failed!"
  }
};

export default state;
