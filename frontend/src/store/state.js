const state = {
  isLoading: false,
  user: {
    id: 5,
    username: "test2",
    email: "test@test.com",
    token: "5f6d135a6d4d92ff8cd9a10ff873aafb3e60cf8aab36a2be684b072d5e280a70",
    links: [21],
    youtube_link:
      "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=203276610183-ekd2kk6mv1jbbnq4160hs4erbu9ouj6g.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fapi%2Fauth%2FyoutubeAuth%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube&state=Ei6INc27emlUkdLjdXzmTw4eDiVLcb&access_type=offline"
  },

  process: {
    id: 1,
    status: 3,
    youtube_video_group: null,
    active: true,
    search_data: "Test search§",
    invalid_msg: null,
    next_process: 2,
    prev_process: null,
    updated_at: "2020-10-20T19:46:24.159578Z",
    created_at: "2020-10-11T19:34:52.138086Z",
    user: 1
  }
};

export default state;
